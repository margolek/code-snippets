list_to_filter = [
        {
            'partition_name': 'account_category_code', 
            'partition_attributes':[
                {
                    'partition_attribute':'CA',
                    'threshold_value': 0.01
                },
                {
                    'partition_attribute':'MG',
                    'threshold_value': 0.02
                }
            ]
        }
        ]

partition_name = 'account_category_code'
partition_attribute = 'MG'


print(list_to_filter)
def get_threshold(list_to_filter, partition_name, partition_attribute):
    for item in list_to_filter:
        if item['partition_name'] == partition_name:
            for attr in item['partition_attributes']:
                if attr['partition_attribute'] == partition_attribute:
                    return attr['threshold_value']
    return None

threshold_value = get_threshold(list_to_filter, partition_name, partition_attribute)
print(threshold_value)