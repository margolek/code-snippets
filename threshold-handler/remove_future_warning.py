import pandas as pd
from pandas import json_normalize
from tabulate import tabulate

# Sample DataFrame
data = {'description': [
    {'key1': 'value1', 'key2': 'value2', 'key3':'value3'},
    {'key1': 'value3', 'key2': 'value4'},
    {'key1': 'value5', 'key2': 'value6'}
    ]
}

df_updated = pd.DataFrame(data)
print(f'DATAFRAME BEFORE EXTRACTION:\n {tabulate(df_updated, tablefmt="grid", headers="keys")}')
# Keys to extract
keys_to_extract = ['key1', 'key2']

# Use json_normalize to extract keys
result_df = json_normalize(df_updated['description'])[keys_to_extract]

# Rename columns to match the original DataFrame
# result_df.columns = [f'{key}_extracted' for key in keys_to_extract]
print(f'RESULT DF: {result_df}')
df_updated.loc[:, 'description'] = df_updated['description'].apply(lambda x: {k: v for k, v in x.items() if k not in keys_to_extract})
# Concatenate the result DataFrame with the original DataFrame
df_updated = pd.concat([df_updated, result_df], axis=1)

# Display the result after operations
print(f'DATAFRAME AFTER EXTRACTION:\n {tabulate(df_updated, tablefmt="grid", headers="keys")}')

