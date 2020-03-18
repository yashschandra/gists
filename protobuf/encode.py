import struct

# returns encoded dict
# this function assumes data in a particular format: it contains an array of field and values.
# each field is represented as a tuple of size 4 (value, wire type, field number, if field is an array)
# eg. message Msg { int64 id = 1; string text = 2; } => [[1234, 'varint', 1, False], ['hello world', 'string', 1, False]]
# also we can assume that every protobuf message is a dict at start, so this function is an entry point for encoding.
def encode_dict(data):
    encoded_value = b''
    for d in data:
        value, wire_type, field_num, repeated = d[0], d[1], d[2], d[3]
        if not value:
            continue
        if wire_type == 'string':
            encoded_value += encode_string_with_tag(value, field_num, repeated)
        elif wire_type == 'varint':
            encoded_value += encode_varint_with_tag(value, field_num, repeated)
        elif wire_type == 'float':
            encoded_value += encode_float_with_tag(value, field_num, repeated)
        elif wire_type == 'double':
            encoded_value += encode_double_with_tag(value, field_num, repeated)
        elif wire_type == 'dict':
            encoded_value += encode_dict_with_tag(value, field_num, repeated)
    return encoded_value

# returns varint encoded tag based upon field number and wire type
def get_tag(field_num, wire_type):
    if wire_type in ['string', 'dict', 'array']:
        return encode_varint((field_num << 3) | 2)
    elif wire_type in ['varint']:
        return encode_varint((field_num << 3) | 0)
    elif wire_type in ['float']:
        return encode_varint((field_num << 3) | 5)
    elif wire_type in ['double']:
        return encode_varint((field_num << 3) | 1)

# returns encoded array of dict values
def encode_repeated_dict(dict_values, field_num):
    encoded_value = b''
    for d in dict_values:
        encoded_value += encode_dict_with_tag(d, field_num, False)
    return encoded_value

# returns encoded dict value along with its tag
def encode_dict_with_tag(dict_value, field_num, repeated):
    # check if value is an array of dict
    if repeated:
        return encode_repeated_dict(dict_value, field_num)
    tag = get_tag(field_num, 'dict')
    encoded_value = encode_dict(dict_value)
    encoded_len = encode_varint(len(encoded_value))
    return tag + encoded_len + encoded_value

# returns encoded array of int values
def encode_repeated_varint(int_values, field_num):
    encoded_values = b''
    tag = get_tag(field_num, 'array')
    for i in int_values:
        ev = encode_varint(i)
        encoded_values += ev
    encoded_len = encode_varint(len(encoded_values))
    return tag + encoded_len + encoded_values

# returns encoded int value along with its tag
def encode_varint_with_tag(int_value, field_num, repeated):
    # check if value is an array of varint
    if repeated:
        return encode_repeated_varint(int_value, field_num)
    tag = get_tag(field_num, 'varint')
    encoded_value = encode_varint(int_value)
    return tag + encoded_value

# returns encoded int value
def encode_varint(int_value):
    encoded_value = []
    if int_value < 0:
        int_value += (1 << 64)
    while True:
        if (int_value >> 7) > 0:
            encoded_value.append((int_value & 0x7f) | 0x80)
        else:
            encoded_value.append(int_value & 0x7f)
            break
        int_value = int_value >> 7
    return bytes(encoded_value)

# returns encoded array of float values
def encode_repeated_float(float_values, field_num):
    encoded_values = b''
    tag = get_tag(field_num, 'array')
    for f in float_values:
        ev = encode_float(f)
        encoded_values += ev
    encoded_len = encode_varint(len(encoded_values))
    return tag + encoded_len + encoded_values

# returns encoded float value along with its tag
def encode_float_with_tag(float_value, field_num, repeated):
    # check if value is an array of float
    if repeated:
        return encode_repeated_float(float_value, field_num)
    tag = get_tag(field_num, 'float')
    encoded_value = encode_float(float_value)
    return tag + encoded_value

# returns encoded float value
def encode_float(float_value):
    return struct.pack('<f', float_value)

# returns encoded array of double values
def encode_repeated_double(double_values, field_num):
    encoded_values = b''
    tag = get_tag(field_num, 'array')
    for d in double_values:
        ev = encode_double(d)
        encoded_values += ev
    encoded_len = encode_varint(len(encoded_values))
    return tag + encoded_len + encoded_values

# returns encoded double value along with its tag
def encode_double_with_tag(double_value, field_num, repeated):
    # check if value is an array of double
    if repeated:
        return encode_repeated_double(double_value, field_num)
    tag = get_tag(field_num, 'double')
    encoded_value = encode_double(double_value)
    return tag + encoded_value

# returns encoded double value
def encode_double(double_value):
    return struct.pack('<d', double_value)

# returns encoded array of string values
def encode_repeated_string(string_values, field_num):
    encoded_value = b''
    for s in string_values:
        encoded_value += encode_string_with_tag(s, field_num, False)
    return encoded_value

# returns encoded string value along with its tag
def encode_string_with_tag(string_value, field_num, repeated):
    # check if value is an array of string
    if repeated:
        return encode_repeated_string(string_value, field_num)
    tag = get_tag(field_num, 'string')
    encoded_value = encode_string(string_value)
    encoded_len = encode_varint(len(encoded_value))
    return tag + encoded_len + encoded_value

# returns encoded string value
def encode_string(string_value):
    return string_value.encode('utf-8')