import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("database/database.db")
        self.c = self.conn.cursor()

    def createPlantsTable(self):
        self.conn = sqlite3.connect("database/database.db")
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS plants (
                id_tree INTEGER PRIMARY KEY,
                latitude REAL,
                longitude REAL,
                added_timestamp TEXT
            )
        ''')
        self.conn.commit()
        self.conn.close()

    def createSensorDataTable(self):
        self.conn = sqlite3.connect("database/database.db")
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id_tree INTEGER,
                sensors INTEGER,
                value REAL,
                time TEXT,
                PRIMARY KEY (id_tree, sensors, time)
            )
        ''')
        self.conn.commit()
        self.conn.close()

db = Database()
db.createPlantsTable()
db.createSensorDataTable()  