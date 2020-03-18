import data_pb2
import json

# read data.json and return it as dict
def get_json_data():
    with open('data.json') as json_file:
        json_str = json_file.read()
    return json.loads(json_str)


if __name__ == '__main__':

    # load json data
    data = get_json_data()

    # using protobuf api to write
    val = data_pb2.Profile(**data).SerializeToString()
    # print encoded bytes
    print(val)

    # convert python dict to json string and print length
    print(len(json.dumps(data)))
    # print encoded bytes length
    print(len(val))