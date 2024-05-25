import datetime as dt
import json
from urllib.request import urlopen
import sqlite3
import time

class Takedata:
    def __init__(self, id_tree):
        self.npm = 2304111010054
        self.id_tree = id_tree
        self.sensors = []
        self.data = []

    def ambildata(self, id_tree, sensors):
        link = f"https://belajar-python-unsyiah.an.r.appspot.com/sensor/read?npm={self.npm}&id_tree={id_tree}&sensor_type={sensors}"
        while True:
            url = urlopen(link)
            document = json.loads(url.read().decode("utf-8"))
            time_str = document.get("when")
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
            self.save_data2db(data)
            return self.sensors
            

    def save_data2db(self, data):
        conn = sqlite3.connect("database/database.db")
        c = conn.cursor()
        c.execute('''
            INSERT INTO sensor_data (id_tree, sensors, value, time)
            VALUES (?, ?, ?, ?)
        ''', (data["id_tree"], data["sensor_type"], data["value"], data["time"]))
        conn.commit()
        conn.close()

# Buat instance dari Ambildata dan panggil ambildata untuk setiap sensor
id_tree = input('Masukkan ID:')  # Misalnya
ambildata_instance = Takedata(id_tree)

while True:
    for sensors in range(10):
        ambildata_instance.ambildata(id_tree, sensors)
        # Print data yang telah diambil
    print(f"Data yang telah diambil untuk id_tanaman={id_tree}: {ambildata_instance.sensors}")

    # time.sleep(2)

