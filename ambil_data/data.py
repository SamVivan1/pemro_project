import datetime as dt
import json
from urllib.request import urlopen
import sqlite3
import time
from threading import Thread
from database import Database
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Takedata:
    def __init__(self):
        self.npm = 2304111010054
        self.sensors = []

    def ambildata(self, id_tree):
        for sensor in range(10):
            try:
                link = f"https://belajar-python-unsyiah.an.r.appspot.com/sensor/read?npm={self.npm}&id_tree={id_tree}&sensor_type={sensor}"
                logger.info(f"Fetching data from {link}")
                with urlopen(link) as url:
                    document = json.loads(url.read().decode("utf-8"))
                
                time_str = document.get("when")
                sensor_type = document.get("sensor_type")
                value = document.get("value")
                
                time = dt.datetime.strptime(time_str, "%a, %d %b %Y %H:%M:%S %Z")
                offset = dt.timedelta(hours=7)
                adjusted_time = time + offset
                
                data = {
                    "id_tree": id_tree,
                    "sensor_type": sensor_type,
                    "value": value,
                    "time": adjusted_time
                }
                self.sensors.append(data)
                logger.info(f"Data fetched: {data}")
                self.save_data2db(data)
            except Exception as e:
                logger.error(f"Failed to fetch or save data for sensor {sensor} of tree {id_tree}: {e}")
        return self.sensors
    
    def ambil_data(self):
        def ambildata_berkala():
            while True:
                try:
                    db = Database()
                    id_trees = db.get_all_id_trees()
                    for id_tree in id_trees:
                        self.ambildata(id_tree[0])
                    time.sleep(60)
                except Exception as e:
                    logger.error(f"Error in periodic data fetch: {e}")
        
        thread = Thread(target=ambildata_berkala)
        thread.daemon = True
        thread.start()

    def save_data2db(self, data):
        try:
            with sqlite3.connect("database/database.db") as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO sensor_data (id_tree, sensors, value, time)
                    VALUES (?, ?, ?, ?)
                ''', (data["id_tree"], data["sensor_type"], data["value"], data["time"]))
                conn.commit()
                logger.info(f"Data saved to database: {data}")
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
        except Exception as e:
            logger.error(f"Error saving data: {e}")

# if __name__ == "__main__":
#     takedata = Takedata()
#     takedata.ambil_data()
