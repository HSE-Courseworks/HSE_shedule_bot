import pytest
from unittest.mock import MagicMock
from TableScripts.db_out import ScheduleManager
from unittest.mock import patch


@pytest.fixture
def mock_connect():
    with patch('psycopg2.connect') as mock_conn:
        yield mock_conn


def test_get_schedule_for_group(mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [1]
    mock_cursor.fetchall.return_value = [(1, 2, 3, 4, 5, 6, 7, 8)]
    mock_connect.return_value.cursor.return_value = mock_cursor

    manager = ScheduleManager(dbname='test_db', user='test_user', password='test_password', host='test_host')
    schedule = manager.get_schedule_for_group('test_group')
    mock_connect.return_value.cursor.assert_called_once()
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()


def test_switch_actuality_for_lesson(mock_connect):
    manager = ScheduleManager(dbname='test_db', user='test_user', password='test_password', host='test_host')
    mock_cursor = mock_connect.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = (True,)
    lesson_id = 123
    result = manager.switch_actuality_for_lesson(lesson_id)
    assert result == True
    mock_cursor.execute.assert_called_with("UPDATE schedule SET actuality = %s WHERE id = %s", (False, lesson_id))


def test_get_weekdays_with_lessons(mock_connect):
    manager = ScheduleManager(dbname='test_db', user='test_user', password='test_password', host='test_host')
    mock_cursor = mock_connect.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда')]
    group_name = 'test_group'
    result = manager.get_weekdays_with_lessons(group_name)
    expected_result = [(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда')]
    assert result == expected_result




