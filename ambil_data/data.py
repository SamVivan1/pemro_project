import datetime as dt
import json
from urllib.request import urlopen
import sqlite3
import time
from threading import Thread
from database import Database

class Takedata:
    def __init__(self):
        self.npm = 2304111010054
        self.sensors = []
        self.data = []

    def ambildata(self, id_tree):
        for sensor in range(10):
            print (sensor)
            link = f"https://belajar-python-unsyiah.an.r.appspot.com/sensor/read?npm={self.npm}&id_tree={id_tree}&sensor_type={sensor}"
            print(link)
            url = urlopen(link)
            document = json.loads(url.read().decode("utf-8"))
            time_str = document.get("when")
            print(time_str)
            sensor = document.get("sensor_type")
            value = document.get("value")
            time = dt.datetime.strptime(time_str, "%a, %d %b %Y %H:%M:%S %Z")
            offset = dt.timedelta(hours=7)
            adjusted_time = time + offset
            data = {
                "id_tree": id_tree,
                "sensor_type": sensor,
                "value": value,
                "time": adjusted_time
                }
            self.sensors.append(data)
            print(data)
            self.save_data2db(data)
        return self.sensors
    
    def ambil_data(self):
        def ambildata_berkala():
            while True:
                db = Database()
                update = Takedata() 
                id_tree = db.get_all_id_trees()
                for id in id_tree:
                    update.ambildata(id[0])
                time.sleep(60)
        thread = Thread(target=ambildata_berkala)
        thread.daemon = True
        thread.start()

    def save_data2db(self, data):
        conn = sqlite3.connect("database/database.db")
        c = conn.cursor()
        c.execute('''
            INSERT INTO sensor_data (id_tree, sensors, value, time)
            VALUES (?, ?, ?, ?)
        ''', (data["id_tree"], data["sensor_type"], data["value"], data["time"]))
        conn.commit()
        conn.close()