from urllib.request import urlopen
import json
import datetime 

def ambilData(id, sensor_type):
    npm = "2304111010054"
    id = str(id)
    sensor_type = str(sensor_type)
    link = f"https://belajar-python-unsyiah.an.r.appspot.com/sensor/read?npm={npm}&id_tree={id}&sensor_type={sensor_type}"
    url = urlopen(link)
    document = json.loads(url.read().decode("utf-8"))
    return document

def extractPointData(data):

  id_tree = data["id_tree"]
  sensor_type = data["sensor_type"]
  value = data["value"]

  return (id_tree, sensor_type, value)

data = ambilData(1, 1)
(id_tree, sensor_type, value) = extractPointData(data)

print(f"id = {id_tree}\nsensor_type = {sensor_type}\nvalue = {value}")