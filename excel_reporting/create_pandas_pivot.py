import pandas as pd
import xlsxwriter

# Create a dictionary with the column names and values
data = {
    'ingest_date': ['2021-01-01', '2021-01-02', '2021-01-03',
                    '2021-01-01', '2021-01-02', '2021-01-03',
                    '2021-01-01', '2021-01-02', '2021-01-03'],
    'rating_model_type_code': ['A', 'A', 'A',
                               'B', 'B', 'B',
                               'C', 'C', 'C'],
    'approved_rating': ['1-', '1-', '1-',
                        '2-', '2-', '2-',
                        '3-', '3-', '3-'],
    'cnt': [1, 2, 3,
            4, 5, 6,
            7, 8, 9],
}

# Create the DataFrame
df = pd.DataFrame(data)

# Create the pivot table
pivot_table = df.pivot_table(index=['ingest_date','rating_model_type_code'],columns='approved_rating', values='cnt', aggfunc='sum')

# Write the pivot table to an Excel file
output_file = 'pivot_pandas.xlsx'
pivot_table.to_excel(output_file, sheet_name='Pivot Table')

print(f'Pivot Table written to {output_file}')
