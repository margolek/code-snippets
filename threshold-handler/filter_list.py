my_list = [
        {
            'partition_attribute': '2240',
            'threshold_value': 0.045
        }, 
        {
            'partition_attribute': '2250',
            'threshold_value': 0.055
        },
        {
            'partition_attribute': 'ELSE',
            'threshold_value': 0.065
        },
]
filtered_attributes = [item['partition_attribute'] for item in my_list if item['partition_attribute'] != 'ELSE']

print(filtered_attributes)

