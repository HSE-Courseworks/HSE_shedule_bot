import openpyxl
import pytest

@pytest.mark.parametrize("file_path", [
    "/home/annermolina/bot/HSE_shedule_bot/downloaded_sheet.xlsx",
])
def test_read_excel_data(file_path):
    try:
        wb = openpyxl.load_workbook(file_path)
        assert wb is not None
    except Exception as e:
        pytest.fail(f"Failed to read Excel file: {e}")


