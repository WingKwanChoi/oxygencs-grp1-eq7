from signalrcore.hub_connection_builder import HubConnectionBuilder
import logging
import requests
import json
import time
import os
from dotenv import load_dotenv 
import psycopg2
from datetime import datetime


class App:
    def __init__(self):
        load_dotenv()
        self._hub_connection = None
        self.TICKS = 10

        # Load environment variables
        self.HOST = os.getenv('HOST')  # Setup your host here
        self.TOKEN = os.getenv('TOKEN')  # Setup your token here
        self.T_MAX = os.getenv('T_MAX')  # Setup your max temperature here
        self.T_MIN = os.getenv('T_MIN')  # Setup your min temperature here
        self.DATABASE_URL = os.getenv('DATABASE_URL')  # Setup your database here
        
        # Initialize database connection
        self.conn = None
        self.connect_to_database()

    def __del__(self):
        if self._hub_connection != None:
            self._hub_connection.stop()
            
        # Cleanup database connection
        if self.conn:
            self.conn.close()
            
    def connect_to_database(self):
        """Connect to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(self.DATABASE_URL)
            print("Connected to the database.")
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")

    def start(self):
        """Start Oxygen CS."""
        self.setup_sensor_hub()
        self._hub_connection.start()
        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def setup_sensor_hub(self):
        """Configure hub connection and subscribe to sensor data events."""
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )
        self._hub_connection.on("ReceiveSensorData", self.on_sensor_data_received)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(
            lambda data: print(f"||| An exception was thrown closed: {data.error}")
        )

    def on_sensor_data_received(self, data):
        """Callback method to handle sensor data on reception."""
        try:
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            timestamp = data[0]["date"]
            temperature = float(data[0]["data"])
            self.take_action(temperature)
            self.save_event_to_database(timestamp, temperature)
        except Exception as err:
            print(err)

    def take_action(self, temperature):
        """Take action to HVAC depending on current temperature."""
        if float(temperature) >= float(self.T_MAX):
            self.save_event_to_database(timestamp=datetime.now(), temperature=temperature, event_type="AC activated")
            self.send_action_to_hvac("TurnOnAc")
        elif float(temperature) <= float(self.T_MIN):
            self.save_event_to_database(timestamp=datetime.now(), temperature=temperature, event_type="Heater activated")
            self.send_action_to_hvac("TurnOnHeater")


    def send_action_to_hvac(self, action):
        """Send action query to the HVAC service."""
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{self.TICKS}")
        details = json.loads(r.text)
        print(details, flush=True)

    def save_event_to_database(self, timestamp, temperature, event_type=None):
        """Save sensor data into database."""
        try:
            if not self.conn or self.conn.closed:
                self.connect_to_database()
            
            cur = self.conn.cursor()
            insert_query = """
            INSERT INTO hvac_data (timestamp, temperature, event_type) 
            VALUES (%s, %s, %s)
            """
            cur.execute(insert_query, (timestamp, temperature, event_type))
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Database error: {e}")


if __name__ == "__main__":
    app = App()
    app.start()
