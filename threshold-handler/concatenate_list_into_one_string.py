partition_attributes = [
    {
        "partition_attribute": "[1,2,3,4,5]",
        "threshold_value": 0.05 
    },
    {
        "partition_attribute": "[6,7]",
        "threshold_value": 0.05 
    },
    {
        "partition_attribute": "1345",
        "threshold_value": 0.05 
    },
    {
        "partition_attribute": "twoja stara",
        "threshold_value": 0.05 
    }
]

my_list = [f"\'{item['partition_attribute']}\'" for item in partition_attributes if item['partition_attribute'] != 'ELSE']
print(f'MY LIST: {my_list}')


partition_attribute_list = []
for item in partition_attributes:
    if item != 'ELSE':
        partition_attribute = item['partition_attribute']
        if partition_attribute[0] == '[' and partition_attribute[-1] == ']':
            partition_attribute = [f"\'{partition_attribute_element}\'" for partition_attribute_element in partition_attribute.strip('[]').split(',')]
            print(f'PARTITION ATTRIBUTE: {partition_attribute}')
            partition_attribute_list += partition_attribute
        else:
            partition_attribute = f"\'{partition_attribute}\'"
            partition_attribute_list.append(partition_attribute)

print(f'PARTITION ATTRIBUE LIST: {partition_attribute_list}')
