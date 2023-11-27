import pandas as pd
import json


def read_json_file(file_path: str) -> dict:
    """
    This function reads json file and returns a dictionary.
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

def change_json_structure(input_data: list, pattern: str) -> dict:
    """
    This function converts list of dictionaries into a json format
    for given pattern.

    Example:
    Input:
        pattern = "variable_with_attributes_and_partition_with_attributes"
        input_sample = [
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

    Output:
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
    """

    df = pd.DataFrame(input_data)

    # group df by variable_name, variable_attribute and partition_name
    grouped_df = df.groupby(["variable_name", "variable_attribute", "partition_name"]).agg(
        {
            "partition_attribute": lambda x: list(x),
            "threshold_value": lambda x: list(x),
        }
    )

    # combine partition_attribute and threshold_value into one column and create list of dictionaries using "partition_attribute" and "threshold_value" as keys
    grouped_df["partition_attributes"] = grouped_df.apply(
        lambda x: [
            {"partition_attribute": attr, "threshold_value": value}
            for attr, value in zip(x["partition_attribute"], x["threshold_value"])
        ],
        axis=1,
    )

    # drop partition_attribute and threshold_value columns
    grouped_df = grouped_df.drop(["partition_attribute", "threshold_value"], axis=1)

    # convert grouped_df into list of dictionaries and include variable_name, variable_attribute and partition_name
    grouped_df = grouped_df.reset_index()

    grouped_df = grouped_df.to_dict(orient="records")
    grouped_df = {pattern: grouped_df}

    return json.dumps(grouped_df, indent=4)


if __name__ == "__main__":
    input_data = read_json_file("sample_input.json")
    print(change_json_structure(input_data["sample_input"], pattern="variable_with_attributes_and_partition_with_attributes"))


