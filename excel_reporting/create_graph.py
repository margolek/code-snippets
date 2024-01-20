import pandas as pd
from openpyxl import load_workbook
import os

def read_csv_to_dataframe(file_path):
    df = pd.read_csv(file_path)
    return df

a = read_csv_to_dataframe('maps_statistics.csv')
b = read_csv_to_dataframe('top_100_players.csv')
c = read_csv_to_dataframe('weapons_statistics.csv')

def add_dataframes_to_excel(dataframes, file_path, sheet_names):
    if os.path.exists(file_path):
        book = load_workbook(file_path)
        writer = pd.ExcelWriter(file_path, engine='openpyxl') 
        writer.book = book
    else:
        writer = pd.ExcelWriter(file_path, engine='openpyxl')

    for dataframe, sheet_name in zip(dataframes, sheet_names):
        dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

    writer._save()
    writer.close()

# Add all dataframes to the Excel file
add_dataframes_to_excel([a, b, c], 'cs_go_stats.xlsx', ['maps', 'players', 'weapons'])