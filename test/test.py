# test.py

import os
import sys
import psycopg2
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

# Ensure the src directory is in the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from main import App


@pytest.fixture
def app():
    """Fixture to create an instance of the App class."""
    return App()


@patch("psycopg2.connect")
def test_connect_to_database(mock_connect, app):
    """Test the database connection."""
    mock_connect.return_value = MagicMock()
    app.connect_to_database()
    mock_connect.assert_called_once_with(app.DATABASE_URL)
    assert app.conn is not None


# @patch('psycopg2.connect')
# def test_connect_to_database_failure(mock_connect, app):
#     """Test database connection failure."""
#     mock_connect.side_effect = psycopg2.Error("Connection failed")
#     app.connect_to_database()
#     assert app.conn is None


@patch("requests.get")
def test_send_action_to_hvac(mock_get, app):
    """Test sending action to the HVAC system."""
    mock_get.return_value.text = '{"status": "success"}'
    action = "TurnOnAc"

    app.send_action_to_hvac(action)

    expected_url = f"{app.HOST}/api/hvac/{app.TOKEN}/{action}/{app.TICKS}"
    mock_get.assert_called_once_with(expected_url)


def test_take_action_activates_ac(app):
    """Test that AC is activated when temperature exceeds T_MAX."""
    app.T_MAX = 25
    temperature = 26

    with patch.object(app, "send_action_to_hvac") as mock_send_action, patch.object(
        app, "save_event_to_database"
    ) as mock_save_event:
        app.take_action(temperature)
        mock_send_action.assert_called_once_with("TurnOnAc")
        mock_save_event.assert_called_once()


def test_take_action_activates_heater(app):
    """Test that Heater is activated when temperature is below T_MIN."""
    app.T_MIN = 18
    temperature = 17

    with patch.object(app, "send_action_to_hvac") as mock_send_action, patch.object(
        app, "save_event_to_database"
    ) as mock_save_event:
        app.take_action(temperature)
        mock_send_action.assert_called_once_with("TurnOnHeater")
        mock_save_event.assert_called_once()


# @patch('psycopg2.connect')
# @patch('psycopg2.extensions.connection.cursor')
# def test_save_event_to_database(mock_cursor, mock_connect, app):
#     """Test saving an event to the database."""
#     mock_connect.return_value = MagicMock()
#     mock_connect.return_value.cursor.return_value = mock_cursor

#     timestamp = datetime.now()
#     temperature = 23.5
#     event_type = "Test Event"

#     app.save_event_to_database(timestamp, temperature, event_type)

#     insert_query = """
#     INSERT INTO hvac_data (timestamp, temperature, event_type)
#     VALUES (%s, %s, %s)
#     """
#     mock_cursor.execute.assert_called_once_with(insert_query, (timestamp, temperature, event_type))
#     app.conn.commit.assert_called_once()
#     mock_cursor.close.assert_called_once()

# @patch('psycopg2.connect')
# @patch('psycopg2.extensions.connection.cursor')
# def test_save_event_to_database_failure(mock_cursor, mock_connect, app):
#     """Test saving an event to the database when connection is closed."""
#     mock_connect.return_value = MagicMock()
#     mock_connect.return_value.cursor.return_value = mock_cursor

#     app.conn = None  # Simulate a closed connection

#     timestamp = datetime.now()
#     temperature = 23.5
#     event_type = "Test Event"

#     app.save_event_to_database(timestamp, temperature, event_type)

#     assert mock_connect.called  # Ensure that connection is attempted again
#     mock_cursor.execute.assert_called_once()
#     app.conn.commit.assert_called_once()
#     mock_cursor.close.assert_called_once()


def test_on_sensor_data_received_valid_data(app):
    """Test handling of valid sensor data."""
    data = [{"date": "2023-07-04T12:00:00Z", "data": "22.5"}]

    with patch.object(app, "take_action") as mock_take_action, patch.object(
        app, "save_event_to_database"
    ) as mock_save_event:
        app.on_sensor_data_received(data)
        mock_take_action.assert_called_once_with(22.5)
        mock_save_event.assert_called_once_with("2023-07-04T12:00:00Z", 22.5)


def test_on_sensor_data_received_invalid_data(app):
    """Test handling of invalid sensor data."""
    data = [{"date": "2023-07-04T12:00:00Z", "data": "invalid"}]

    with patch.object(app, "take_action") as mock_take_action, patch.object(
        app, "save_event_to_database"
    ) as mock_save_event:
        app.on_sensor_data_received(data)
        mock_take_action.assert_not_called()
        mock_save_event.assert_not_called()
