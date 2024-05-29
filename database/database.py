import sqlite3
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path="database/database.db"):
        self.db_path = db_path

    def createPlantsTable(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS plants (
                    id_tree INTEGER PRIMARY KEY,
                    latitude REAL,
                    longitude REAL,
                    added_timestamp TEXT
                )
            ''')
            conn.commit()
            logger.info("Plants table created or verified successfully.")

    def createSensorDataTable(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id_tree INTEGER,
                    sensors INTEGER,
                    value REAL,
                    time TEXT,
                    PRIMARY KEY (id_tree, sensors, time)
                )
            ''')
            conn.commit()
            logger.info("Sensor data table created or verified successfully.")

    def get_all_id_trees(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT DISTINCT id_tree FROM plants")
            id_trees = c.fetchall()
            logger.info(f"Retrieved all ID trees: {id_trees}")
            return id_trees
    
    def get_all_plants_data(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM plants")
            plants = c.fetchall()
            logger.info(f"Retrieved all plants data: {plants}")
            return plants

if __name__ == "__main__":
    db = Database()
    db.createPlantsTable()
    db.createSensorDataTable()
    print(db.get_all_id_trees())
