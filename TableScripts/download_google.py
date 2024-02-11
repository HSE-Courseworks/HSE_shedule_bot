import gspread
from google.oauth2.credentials import Credentials
from openpyxl import Workbook
from googleapiclient.discovery import build
import requests
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Anna\\Documents\\schedule-401419-59d99eeeb42a.json"
def download_sheet(sheet_link):
    from google.oauth2.credentials import Credentials

    # Инициализация объекта Credentials с использованием информации о сервисном аккаунте
    creds = Credentials.from_service_account_info({
        "type": "service_account",
        "project_id": "schedule-401419",
        "private_key_id": "59d99eeeb42a1f57da5eeacb68389387dcbdb156",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC3eHRy60waIyp1\nE9QOy9nrZKmIwkQPbCW5MOqGiHD/emlmEXkgNyy6EreJUdlA3cej+G4JuoGoKdpe\nMFV94HrOm1ZHauHQHfQ1rNoMZxympP2bsgHTKC5wnTbiolnCzTHMKXWxBDzL9QWd\n19I9PD1bBG8WVZZ6LUouZTD8mTeDGHMUMFGfJi8uscD3CmMy4vJ03SE/lCiLHZJt\nj7jfYoI7acnbVfTr9zEtPTUVJ9yFCVjWnNYPbBpavvwZG9umIwmJzyl+C0dAnunG\nkk3jkYO/LJM8mesivWKNHsHQCc3HEVhMIEv6hXA3I2NFJ14YUpn310QCieqrMk+t\nrsQ0FSFjAgMBAAECggEAEr4cb0z4RkdHZBR1ell61qA+7XijCUxMAkIsAzhXCtJP\niBzK2e6pBA07cKzK2+SMK4UKgLXr3uj/pNWdNjHDee3Gf588mE0nEICq+c9izudV\n/RzPMOoO7HQzEi3xq4PYzXmCy2WabF+Ihlpw4M6RmgW273oo2CxeQqUVvwhL8nlV\nmqnLK+CPcaeqN0mxcTXXrk8ITryKNsYGHOkSvqT05x0S3K+fxlHr8mRm9CE3S2fM\nPfaDT/+g4QDRV/z2AL+/ZBXo5+e+z0LoFi3tIOPc8XYzdEo9o14wVwXkxF57KF/K\n/LjLyPyAbdzFkPNRGLeMHzHxWPeswV7faeYG5wvdIQKBgQDjxBDy/0XTzK8zAhYa\nynYCH/4FDdAPuDnCK/sLMfzZITFt7IEGim+5gGFvioR+CUfMuy2/fI8Ps0RnlAYJ\n3Z6u3+GCEgyYV7xQTA3Iz+ZB2b6Ex12s0UADrUZziPsSvMZpmA7+3I+F/xu+TA0W\nRHqlNxIgMxPRApi1JgeebVrrcQKBgQDONre20BDeOSsNjqJZqB5J1vdn1kT/WHuL\nUQWHy3aULw978mhRr5VgL3bjTuebVXBEku96qO3BjudaQNufUiStuNRXUkY8ioag\nA49xqMHctReazxrnMKZ8sQiIAZIOZ0nFgH5VziXjF7/uyDONwzlQm/uvHO38QJHt\nF+f3vEwoEwKBgE26EkKqxMyTtFJG6v43i3AMNObKoO9MYkGWOrTGWVBL2I93v0xZ\nH+mBGz8yWSadyife1KzdOAEWn0htpmXlgIqTEmUN/chbYINSgP2/nQdp5G9xjdE1\nE5BtqHYzD+OEEn3ki3GEGWKT/YbCc1DfC6+oDIJ6i8+vACgJk14IWZexAoGBAIRz\nJMDpF0yEz6BfkuufTgUDa9loCN0xifjLy4+TIdDAAWQNKO/+pSUol2Yc0io1UGzb\nK7JPOpbuIK8ZpXbJngFvDAQiNjbAiwPQBZxtVkdakZS/nXoNB4JjeyVQTO2vbfTL\nOVoHlNIt+Pt335UYZYHfDmNFY554IsJ0bmvyp7+9AoGBAKGM9tJ1k9v6dBOm0SGT\n+rG97I/OV+loLa+4w4k2iyzV90YEUXujFp+JRXfWv1T4HAj+FAU2uwYUdAgjlhK7\ny1nRPiL+H9TFCkYiy0wqPfCmdwDjeBmjWH8AkmjDqNod135cgqKYRgpwF3XBzB/y\n3N5+P2mrf3ZRb/+EX2zwpL+m\n-----END PRIVATE KEY-----\n",
        "client_email": "account-schedule@schedule-401419.iam.gserviceaccount.com",
        "client_id": "116832548773502620058",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/account-schedule%40schedule-401419.iam.gserviceaccount.com",
    })

    service = build('sheets', 'v4', credentials=creds)
    sheet_id = sheet_link.split('/')[-2]
    response = service.spreadsheets().get(spreadsheetId=sheet_id, fields="sheets(properties(sheetId,title))").execute()
    download_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    with open('downloaded_sheet.xlsx', 'wb') as f:
        f.write(requests.get(download_url).content)
    return 'downloaded_sheet.xlsx'
