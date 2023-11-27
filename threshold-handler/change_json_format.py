import json


input_json = {
    "my_list": [
        {
            "partition_attribute": 102,
            "threshold_value": "2.5%",
            "variable_name": "da",
            "variable_attribute": "0",
            "partition_name": "pre_client_id"
        },
        {
            "partition_attribute": 103,
            "threshold_value": "3%",
            "variable_name": "da",
            "variable_attribute": "5",
            "partition_name": "pre_client_id"
        },
        {
            "partition_attribute": 105,
            "threshold_value": "4.5%",
            "variable_name": "da",
            "variable_attribute": "5",
            "partition_name": "pre_client_id"
        }
    ]
}

output_json = {
    "variable_with_attributes_and_partition_with_attributes": [
        {
            "variable_name": "da",
            "variable_attribute": "0",
            "partition_name": "pre_client_id",
            "partition_attributes": [
                {
                    "partition_attribute": 102,
                    "threshold_value": "2.5%"
                }
            ]
        },
        {
            "variable_name": "da",
            "variable_attribute": "5",
            "partition_name": "pre_client_id",
            "partition_attributes": [
                {
                    "partition_attribute": 103,
                    "threshold_value": "3%"
                },
                {
                    "partition_attribute": 105,
                    "threshold_value": "4.5%"
                }
            ]
        }

    ]
}




def convert_json(input_json):
    output_json = {}
    output_json["variable_with_attributes_and_partition_with_attributes"] = []
    for i in input_json["my_list"]:
        if i["variable_name"] not in [j["variable_name"] for j in output_json["variable_with_attributes_and_partition_with_attributes"]]:
            output_json["variable_with_attributes_and_partition_with_attributes"].append({"variable_name": i["variable_name"], "variable_attribute": i["variable_attribute"], "partition_name": i["partition_name"], "partition_attributes": []})
        else:
            for k in output_json["variable_with_attributes_and_partition_with_attributes"]:
                if k["variable_name"] == i["variable_name"]:
                    k["partition_attributes"].append({"partition_attribute": i["partition_attribute"], "threshold_value": i["threshold_value"]})
    return output_json

a = convert_json(input_json)
# Make output more readable with 4 indent
print(json.dumps(a, indent=4))

