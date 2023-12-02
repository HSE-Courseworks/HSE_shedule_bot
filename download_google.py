import gspread
from oauth2client.service_account import ServiceAccountCredentials
from openpyxl import Workbook

credentials = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/Anna/Documents/schedule-401419-59d99eeeb42a.json')

gc = gspread.authorize(credentials)

spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1dIf9TzC_N0-fsHximMNGHXuiYvYRYBWnAGc3pIH0VRQ/edit#gid=0')

workbook = Workbook()

sheets = spreadsheet.worksheets()

for sheet in sheets:
    new_sheet = workbook.create_sheet(title=sheet.title)
    data = sheet.get_all_values()
    for row in data:
        new_sheet.append(row)
workbook.remove(workbook.active)
workbook.save('schedule.xlsx')
