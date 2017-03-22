import excel_microbe_directory.spreadsheet

# Load the spreadsheet and convert it to a python dictionary
spreadsheet_path = 'annotations_master 3-14-17.xlsx'
ws = excel_microbe_directory.spreadsheet.Spreadsheet(spreadsheet_path)
ws.export_as_sqlite('microbe_directory.sql')
