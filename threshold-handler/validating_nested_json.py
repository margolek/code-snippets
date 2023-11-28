

def validate_data(data, allowed_keys, level=""):
    print(f"DATA KEYS: {data.keys()}")
    for key in data.keys():
        if key not in allowed_keys:
            print(f"Error: Key '{key}' not allowed at level '{level}'")
            return False
        if isinstance(data[key], list) and any(isinstance(value, dict) for value in data[key]):
            for index, item in enumerate(data[key]):
                if not isinstance(item, dict):
                    print(f"Error: Invalid item '{item}' at level '{level}'")
                    return False
                if "ELSE" in item and (index != len(data[key]) - 1):
                    print(f"Error: 'ELSE' key is not the last item in the list at level '{level}.{key}'")
                    return False
                if not validate_data(item, allowed_keys[key], level=f"{level}.{key}"):
                    return False
        elif isinstance(data[key], dict):
            if not validate_data(data[key], allowed_keys[key], level=f"{level}.{key}"):
                return False
    return True


# Sample nested JSON data
data = {
    "key1": [
        {"nested_key1": {"nested_key3": [1, 2, 3, 4]}},
        {"nested_key2": {"nested_key4": "nested_value4"}},
        {"ELSE": "ELSE_VALUE"},
    ],
    "key2": {
        "nested_key1": {"nested_key3": "nested_value3"},
        "nested_key2": {"nested_key4": "nested_value4"},
    },
    "key3": "value3",
}

# Define the allowed keys
allowed_keys = {
    "key1": {
        "nested_key1": ["nested_key3"],
        "nested_key2": ["nested_key4"],
        "ELSE": [],
    },
    "key2": {
        "nested_key1": ["nested_key3"],
        "nested_key2": ["nested_key4"],
    },
    "key3": [],
}

# Validate the data
is_valid = validate_data(data, allowed_keys)
print(is_valid)


