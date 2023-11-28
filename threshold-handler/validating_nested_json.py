def validate_data(data, allowed_keys):
    for key in data.keys():
        if key not in allowed_keys:
            return False
        if isinstance(data[key], list):
            for item in data[key]:
                if not validate_data(item, allowed_keys[key]):
                    return False
        elif isinstance(data[key], dict):
            if not validate_data(data[key], allowed_keys[key]):
                return False
    return True

# Sample nested JSON data
data = {
    "key1": [
        {"nested_key1": {"nested_key3": "nested_value3"}},
        {"nested_key2": {"nested_key4": "nested_value4"}}
    ],
    "key2": {
        "nested_key1": {"nested_key3": "nested_value3"},
        "nested_key2": {"nested_key4": "nested_value4"}
    },
    "key3": "value3"
}

# Define the allowed keys
allowed_keys = {
    "key1": {
        "nested_key1": ["nested_key3"],
        "nested_key2": ["nested_key4"]
    },
    "key2": {
        "nested_key1": ["nested_key3"],
        "nested_key2": ["nested_key4"]
    },
    "key3": []
}

# Validate the data
is_valid = validate_data(data, allowed_keys)
print(is_valid)

