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

    def get_all_id_trees(self):
            self.conn = sqlite3.connect("database/database.db")
            self.c = self.conn.cursor()
            self.c.execute("SELECT DISTINCT id_tree FROM plants")
            id_trees = self.c.fetchall()
            self.conn.close()
            return id_trees
    
    def get_all_plants_data(self):
        self.conn = sqlite3.connect("database/database.db")
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM plants")
        plants = self.c.fetchall()
        self.conn.close()
        return plants

db = Database()
# db.createPlantsTable()
# db.createSensorDataTable()  
# print(db.get_all_id_trees())