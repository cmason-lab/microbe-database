import microbe_directory.spreadsheet

# Load the spreadsheet and export it as sqlite
# This is the form in which the database will get tossed around--much fater
# than parsing the Excel spreadsheet each time
spreadsheet_path = 'data/annotations_master 3-14-17.xlsx'
ws = microbe_directory.spreadsheet.Spreadsheet(spreadsheet_path)
ws.export_as_sqlite('data/microbe_directory.sql')
