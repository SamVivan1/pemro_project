import sqlite3
import datetime as dt
import random
from CTkMessagebox import CTkMessagebox

class CRUD:
    def __init__(self):
        self.conn = sqlite3.connect("database/database.db")
        self.c = self.conn.cursor()

    def db_connect(self):
        self.conn = sqlite3.connect("database/database.db")
        self.c = self.conn.cursor()

    def db_close(self):
        self.conn.commit()
        self.conn.close()

    def id_tree_exists(self, id_tree):
            self.c.execute('SELECT 1 FROM plants WHERE id_tree = ?', (id_tree,))
            return self.c.fetchone() is not None

    def tambah_tanaman(self, id_tree):
        self.db_connect()
        self.c = self.conn.cursor()
        lat = random.uniform(-90, 90)
        lon = random.uniform(-180, 180)
        time = dt.datetime.now()
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(time)
        self.c.execute('''
            INSERT INTO plants (id_tree, latitude, longitude, added_timestamp)
            VALUES (?, ?, ?, ?)
        ''', (id_tree, lat, lon, time))
        self.db_close()

    def tampilkanSensor(self):
        self.db_connect()
        self.c.execute('''
            SELECT id_tree, sensors, value, time FROM sensor_data
        ''')
        sensor = self.c.fetchall()
        self.db_close() 
        return sensor

    def tampilkanTanaman(self):
        self.db_connect()
        self.c.execute('''
            SELECT id_tree, latitude, longitude, added_timestamp FROM plants
        ''')
        plants = self.c.fetchall()
        self.db_close()
        return plants
    
    def hapus(self, id_tree):
        self.db_connect()
        self.c.execute('''
        DELETE FROM plants WHERE id_tree = ?
    ''', (id_tree,))
        self.c.execute('''
        DELETE FROM sensor_data WHERE id_tree = ?
    ''', (id_tree,))  # Tambahkan koma setelah id_tree untuk membuatnya menjadi tupel
        self.db_close()