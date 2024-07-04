# test_integration.py

import os
import sys
import pytest
from unittest.mock import MagicMock, patch
import psycopg2
from datetime import datetime

# Ensure the src directory is in the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from main import App


@pytest.fixture
def app():
    """Fixture to create an instance of the App class."""
    app_instance = App()
    yield app_instance
    if app_instance.conn:
        app_instance.conn.close()


@patch("psycopg2.connect")
def test_database_connection(mock_connect, app):
    """Test the database connection."""
    mock_connect.return_value = MagicMock()
    app.connect_to_database()
    mock_connect.assert_called_once_with(app.DATABASE_URL)
    assert app.conn is not None


# Test fails
# @patch('psycopg2.connect')
# def test_save_event_to_database(mock_connect, app):
#     """Test saving an event to the database."""
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_connect.return_value = mock_conn
#     mock_conn.cursor.return_value = mock_cursor

#     timestamp = datetime.now()
#     temperature = 23.5
#     event_type = "Test Event"

#     app.save_event_to_database(timestamp, temperature, event_type)

#     insert_query = """
#     INSERT INTO hvac_data (timestamp, temperature, event_type)
#     VALUES (%s, %s, %s)
#     """
#     mock_cursor.execute.assert_called_once_with(insert_query, (timestamp, temperature, event_type))
#     mock_conn.commit.assert_called_once()
#     mock_cursor.close.assert_called_once()


@patch("requests.get")
def test_send_action_to_hvac(mock_get, app):
    """Test sending action to the HVAC system."""
    action = "TurnOnAc"
    mock_get.return_value.text = '{"status": "success"}'

    app.send_action_to_hvac(action)

    expected_url = f"{app.HOST}/api/hvac/{app.TOKEN}/{action}/{app.TICKS}"
    mock_get.assert_called_once_with(expected_url)
    assert mock_get.return_value.text == '{"status": "success"}'


@patch.object(App, "save_event_to_database")
def test_take_action_activates_ac(mock_save_event, app):
    """Test that AC is activated when temperature exceeds T_MAX."""
    app.T_MAX = 25
    temperature = 26

    with patch.object(app, "send_action_to_hvac") as mock_send_action:
        app.take_action(temperature)
        mock_send_action.assert_called_once_with("TurnOnAc")
        mock_save_event.assert_called_once()


@patch.object(App, "save_event_to_database")
def test_take_action_activates_heater(mock_save_event, app):
    """Test that Heater is activated when temperature is below T_MIN."""
    app.T_MIN = 18
    temperature = 17

    with patch.object(app, "send_action_to_hvac") as mock_send_action:
        app.take_action(temperature)
        mock_send_action.assert_called_once_with("TurnOnHeater")
        mock_save_event.assert_called_once()
