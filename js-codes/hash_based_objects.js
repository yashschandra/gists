// get value of a property
function getPropValue(propName) {
    let memoryAddress = calculateMemoryAddressOfPropValue(propName);
    let value = getValueAtMemoryAddress(memoryAddress);
    return value;
}

// set value of a property
function setPropValue(propName, value) {
    let memoryAddress = calculateMemoryAddressOfPropValue(propName);
    setValueAtMemoryAddress(memoryAddress, value);
}

// calculate hash of propName
function calculateMemoryAddressOfPropValue(propName) {
    let memoryAddress = getHashValue(propName);
    return memoryAddress;
}

// hash of a key
function getHashValue(key) {
    // return hash(key);
}

// get value at memoryAddress
function getValueAtMemoryAddress(memoryAddress) {
    // return value
}

// set value at memory address
function setValueAtMemoryAddress(memoryAddress, value) {
    // return
}