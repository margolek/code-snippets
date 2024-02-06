import xlsxwriter
import pandas as pd

def create_xlsm_file_with_populated_data(filepath, sheet_name):
    # Create a DataFrame
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [6, 7, 8, 9, 10],
        'C': ['a', 'b', 'c', 'd', 'e']
    })

    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(f'{filepath}', engine='openpyxl')

    # Write the DataFrame to an .xlsm file
    df.to_excel(writer, sheet_name=f'{sheet_name}')

    # Close the Pandas Excel writer
    writer.save()

def add_macro_to_xlsm_file(excel_file_path, excel_file_sheet, macro_bin_filepath):
    # Note the file extension should be .xlsm.
    workbook = xlsxwriter.Workbook(f'{excel_file_path}')
    worksheet = workbook.get_worksheet_by_name(f'{excel_file_sheet}')
    # Add the VBA project binary.
    workbook.add_vba_project(f'{macro_bin_filepath}')
    return workbook, worksheet


def button_with_macro_functinality(worksheet, workbook):

    # Add a button tied to a macro in the VBA project.
    worksheet.insert_button('F3', {'macro':   'CreatePivotTable',
                                   'caption': 'Create Pivot Table and chart',
                                   'width':   200,
                                   'height':  50})
    workbook.close()


if __name__ == '__main__':
    file_path = 'output.xlsm'
    sheet_name = 'Sheet1'
    macro_bin_path = './vbaProject.bin'
    create_xlsm_file_with_populated_data(file_path, sheet_name)
    wb, ws = add_macro_to_xlsm_file(file_path, sheet_name, macro_bin_path)
    button_with_macro_functinality(ws, wb)
