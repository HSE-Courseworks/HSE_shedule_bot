import gspread
from google.oauth2.service_account import Credentials
from openpyxl import Workbook
from googleapiclient.discovery import build
import requests
import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/schedule-401419-59d99eeeb42a.json"

def download_sheet(sheet_link):
    creds = Credentials.from_service_account_file(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

    service = build('sheets', 'v4', credentials=creds)
    sheet_id = sheet_link.split('/')[-2]
    response = service.spreadsheets().get(spreadsheetId=sheet_id, fields="sheets(properties(sheetId,title))").execute()
    download_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"

    with open('downloaded_sheet.xlsx', 'wb') as f:
        f.write(requests.get(download_url).content)
    return 'downloaded_sheet.xlsx'
