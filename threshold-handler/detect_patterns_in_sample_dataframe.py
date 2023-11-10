import numpy as np
import pandas as pd
from tabulate import tabulate
import re
from robot.api import logger
my_dataframe = {
        'table': ['table_1', 'table_1', 'table_1', 'table_1', 'table_1', 'table_1', 'table_1'],
        'column': ['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7'],
        'th_sum': [
            'pre_client_id:[102:1810.5%, 201:3100.0%, 202:3100.0%, ELSE:3100.0% ]',
            np.NaN,
            'S',
            'pr294[10]da:[1509:2.5%, [1599 ,6034]:5%, 6016:20%]',
            np.NaN,
            'pr294[10]da:[1509:2.5%, [1599, 6034]:5%, 6016:20%', #Lack of ']' at the end
            'pr294[10]da:[1509:2.5%, [1599, 6034]:5%, 6016:20%],' # Comma as the last character
        ],
        'th_null': [
            np.NaN, 
            'pre_client_id:[107:111.5%, 21:3.0%, 2:1.0%, ELSE:6.0% ]',
            'Y',
            np.NaN,
            '[block_code[20]client_id:[102:70%, 202:45%, 302:55%], block_code[50]client_id:[102:15%, 202:35%, 302:35%]]',
            '[block_code[]client_id:[102:70%, 202:45%, 302:55%], block_code[50]client_id:[102:15%, 202:35%, 302:35%]]', #empty variable attribute
            '[block_code[ad]client_id:[102:70%, 202:45%, 302:55%], block_code[50]client_id:[102:15%, 202:35%, 302:35%],]' #Comma after the last item
        ]
}


threshold_variable_json_output_ezxample = {
        'col_1':{
            'th_sum_dist': [
                        {
                            'partition': 'pre_client_id',
                            'partition_attribute': 102,
                            'threshold_value': 0.02
                        },
                        {
                            'partition': 'pre_client_id',
                            'partition_attribute': [105,20,1],
                            'threshold_value': 0.06
                        }
            ]
        }
    }

threshold_variable_partition_json_output_example = {
        'col_1':{
            'th_sum_dist': [
                        {
                            'partition': 'client_id',
                            'partition_attribute': 102,
                            'variable': 'col_1',
                            'variable_attribute': 20,
                            'threshold_value': 0.02
                        },
                        {
                            'partition': 'client_id',
                            'partition_attribute': [105,20,1],
                            'variable': 'col_1',
                            'variable_attribute': 50,
                            'threshold_value': 0.06
                        }
            ]
        }
    }
my_dataframe = pd.DataFrame(my_dataframe)

def recognize_threshold_var_partition(input_string):
    var_with_value_and_partition_pattern = r'(?P<variable>\w+)\[(?P<variable_att>\w+)\](?P<partition>\w+)'
    match = re.match(var_with_value_and_partition_pattern, input_string)
    if match:
        return (True, match)
    else:
        return (False, None)

def recognize_threshold_var(input_string):
    partition_pattern = r'^[^[\]]+$'
    match = re.match(partition_pattern,input_string)
    if match:
        return (True, match)
    else:
        return (False, None)

def validate_partition_attributes(partition_attributes):
    #Regex match values followed by percentage or defimal value e.x: 120:5%, BU:0.04
    partition_attributes_with_values_pattern = r'(\w ?\w*):(\d+(\.\d+)?%?)'
    partition_attributes_with_values_pattern_named = r'(?P<partition_attribute>\w ?\w*):(?P<threshold_value>\d+(\.\d+)?%?)'
    # Regex match when partition attributes are provided as a list e.x [102,105,106]:5%
    partition_attribute_with_values_list_pattern = r'(\[[\w\s,]+\]):(\d+(\.\d+)?%?)'
    partition_attribute_with_values_list_pattern_named = r'(?P<partition_attribute_list>\[[\w\s,]+\]):(?P<threshold_value_2>\d+(\.\d+)?%?)'
    string_beginning = r'^\['
    string_content = f'(?:(?:{partition_attributes_with_values_pattern}|{partition_attribute_with_values_list_pattern})(?:, (?:{partition_attributes_with_values_pattern}|{partition_attribute_with_values_list_pattern}))*)(?![\w,]) ?'
    string_end = r'\]$'
    combined_pattern = string_beginning + string_content + string_end
    # combined_pattern_2 = re.compile(rf""" 
    #     ^\[                                                                                                     # Part 1
    #     (?:(?:{partition_attributes_with_values_pattern}|{partition_attribute_with_values_list_pattern})        # Part 2
    #     (?:, (?:{partition_attributes_with_values_pattern}|{partition_attribute_with_values_list_pattern}))*)   # Part 3
    #     (?![\w\s,])                                                                                             # Part 4
    #     \]$                                                                                                     # Part 5
    # """, re.VERBOSE) # TODO - Try to use this approach when it will be possible
    match = re.match(combined_pattern, partition_attributes)
    partition_details_list = []
    if match:
        # Extract detected values
        partition_value_with_th_matches = re.finditer(partition_attributes_with_values_pattern_named, partition_attributes)
        for partition_value_with_th_match in partition_value_with_th_matches:
            partition_details_list.append({
                'partition_attribute': partition_value_with_th_match.group('partition_attribute'), 
                'threshold_value': partition_value_with_th_match.group('threshold_value')
        })
        partition_value_with_th_list_matches = re.finditer(partition_attribute_with_values_list_pattern_named, partition_attributes) 
        for partition_value_with_th_list_match in partition_value_with_th_list_matches:
            partition_details_list.append({
                'partition_attribute': partition_value_with_th_list_match.group('partition_attribute_list'), 
                'threshold_value': partition_value_with_th_list_match.group('threshold_value_2')
        })
        return (True, partition_details_list)
    else:
        return (False, partition_details_list)

def combine_partition_with_attributes_and_th(partition, partition_attributes_converted):
    return [{**partition_attribute, 'partition_name': partition} for partition_attribute in partition_attributes_converted]

def combine_partition_with_attributes_and_variable_th(partition, variable, variable_att, partition_attributes_converted):
    return [
            {**partition_attribute, 'variable_name': variable, 'variable_attribute': variable_att,'partition_name': partition}
            for partition_attribute in partition_attributes_converted
    ]

def extract_details_threshold_var_partition(th_logic): 
    if not isinstance(th_logic,list):
        th_logic = [th_logic]
    partition_with_variable_list = []
    for th_logic_item in th_logic:
        # Divide string based on 1st occurance of ':'
        try:
            var_with_value_and_partition, partition_attributes = th_logic_item.split(':',1)
        except ValueError:
            return 'Invalid logic in partition attributes section!'
        # Verify if 1st part meet requirements
        match_exists, match = recognize_threshold_var_partition(var_with_value_and_partition)
        if match_exists:
            variable = match.group('variable')
            variable_att = match.group('variable_att')
            partition = match.group('partition')
        else:
            return 'Invalid logic in section with partition, variable and variable attribute!'
        # Verify with partition attributes have correct logic and values
        partition_attributes_logic_valid, partition_attributes_converted = validate_partition_attributes(partition_attributes)
        if partition_attributes_logic_valid:
            partition_with_attributes_variable_combined = combine_partition_with_attributes_and_variable_th(partition, variable, variable_att, partition_attributes_converted)
            partition_with_variable_list += partition_with_attributes_variable_combined
        else:
            return 'Invalid logic in partition attributes section!'
    return ('partition_with_variable_att', partition_with_variable_list)

def extract_details_threshold_var(partition, partition_attributes):
    partition_attributes_logic_valid, partition_attributes_converted = validate_partition_attributes(partition_attributes)
    if partition_attributes_logic_valid:
        partition_with_attributes_combined = combine_partition_with_attributes_and_th(partition,partition_attributes_converted)
        return ('partition_without_variable_att', partition_with_attributes_combined)
    else:
        return 'Invalid logic in partition attributes section!'

def detect_variable_level_logic(value):
    # THRESHOLD PROVIDED AS A LIST
    try:
        # Regular expression pattern to check if the string resembles a Python list
        list_pattern = r'^\s*\[.*\]\s*$'
        if re.match(list_pattern,value):
            list_element_split_pattern = r'(?<=\])(?:,|\s*,)\s*'
            # Use the re.split() function to split the string based on the pattern
            th_logic_list = re.split(list_element_split_pattern, value[1:-1])
            # Use function to verify correctness of variable
            converted_content = extract_details_threshold_var_partition(th_logic_list)
            return converted_content
    except TypeError:
        return value
    except ValueError:
        return f'No matching pattern for: {value}'
    except Exception as err:
        warning = f'Unexpected error occur: {err}, please report a BUG'
        logger.warn(warning)
    # THRESHOLD SHOULD NOT BE A LIST
    try:
        partition_with_variable, partition_attributes = value.split(':',1)
        var_with_partition_match_exists, match = recognize_threshold_var_partition(partition_with_variable)
        if var_with_partition_match_exists:
            # Variable level logic: variable + partition
            converted_content = extract_details_threshold_var_partition(value)
            return converted_content
        partition_match_exists, partition_match = recognize_threshold_var(partition_with_variable)
        if partition_match_exists:
            # Variable level logic: partition
            converted_content = extract_details_threshold_var(partition_with_variable, partition_attributes)
            return converted_content
    except TypeError:
        return value
    except ValueError:
        return f'No matching pattern for: {value}'
    except Exception as err:
        warning = f'Unexpected error occur: {err}, please report a BUG'
        logger.warn(warning)
        return warning
    return f'No matching pattern for: {value}'




print('---Input dataframe---')
print(tabulate(my_dataframe,tablefmt='grid',headers='keys', maxcolwidths=40))
columns_to_check = ['th_sum','th_null']
print('---Detect variable level logic masking---')
# map detect_variable level logic element-wise
mask = my_dataframe[columns_to_check].map(detect_variable_level_logic)
print('---table with applyied logic---')
my_dataframe[columns_to_check] = mask
print(tabulate(my_dataframe,tablefmt='grid',headers='keys', maxcolwidths=40))
