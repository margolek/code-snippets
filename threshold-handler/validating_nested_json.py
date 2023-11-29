import json
from typing import Union





def validate_data(data:dict, allowed_keys:dict, level="") -> dict:
    for key in data.keys():
        if key not in allowed_keys:
            error = f"Error: Key '{key}' not allowed at level '{level}'"
            return {"result": "error", "reason": error, "value": data}
        if isinstance(data[key], list) and any(isinstance(value, dict) for value in data[key]):
            for index, item in enumerate(data[key]):
                if not isinstance(item, dict):
                    error = f"Error: Invalid item '{item}' at level '{level}'"
                    return {"result": "error", "reason": error, "value": data}
                if "ELSE" in item and (index != len(data[key]) - 1):
                    error = f"Error: 'ELSE' key is not the last item in the list at level '{level}.{key}'"
                    return {"result": "error", "reason": error, "value": data}
                result = validate_data(item, allowed_keys[key], level=f"{level}.{key}")
                if "result" and "reason" in result:
                    return result
        elif isinstance(data[key], dict):
            result = validate_data(data[key], allowed_keys[key], level=f"{level}.{key}")
            if "result" and "reason" in result:
                return result
        elif key == "threshold_value":
            threshold_validated = validate_threshold_and_convert_to_value_to_float(data[key])
            if not threshold_validated:
                error = f"Error: Invalid threshold value '{data[key]}' at level '{level}.{key}'"
                return error
            else:
                data[key] = threshold_validated
    return {"result": "success", "value": data}


def validate_threshold_and_convert_to_value_to_float(value: Union[str,float,int]) -> Union[float,bool]:
    if isinstance(value, int) or isinstance(value, float):
        return True
    elif isinstance(value, str):
        try:
            if value.endswith("%"):
                float_value = float(value[:-1]) / 100
                return float_value
            else:
                float_value = float(value)
                return float_value
        except ValueError:
            return False
    else:
        return False


# Sample nested JSON data
data = {
    "key1": [
        {
            "nested_key1": [
                {
                    "partition_value": [1, 2, 3, 4],
                    "threshold_value": "50%"
                }
            ]
        },
        {
            "nested_key2": {
                "nested_key4": "nested_value4"
            }
        },
        {
            "ELSE": {
                "threshold_value": "2.5%"
            }
        }
    ],
    "key2": {
        "nested_key1": {
            "nested_key7": "nested_value3"
        },
        "nested_key2": {
            "nested_key4": "nested_value4"
        }
    },
    "key3": "value3"
}

# Define the allowed keys
allowed_keys = {
    "key1": {
        "nested_key1": ["partition_value", "threshold_value"],
        "nested_key2": ["nested_key4"],
        "ELSE": ["threshold_value"]
    },
    "key2": {
        "nested_key1": ["nested_key7"],
        "nested_key2": ["nested_key4"]
    },
    "key3": []
}

# Validate the data
is_valid = validate_data(data, allowed_keys)
if isinstance(is_valid, str):
    print(is_valid)
else:
    print(json.dumps(is_valid, indent=4))
