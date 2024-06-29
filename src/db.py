import psycopg2
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def create_table():
    """Create the sensor_data table in the database."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS hvac_data (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL,
        temperature FLOAT NOT NULL,
        event_type VARCHAR(50)
    );
    """
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(create_table_query)
        conn.commit()
        cur.close()
        conn.close()
        print("Table hvac_data created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")


if __name__ == "__main__":
    create_table()