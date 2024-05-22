from urllib.request import urlopen
import json
import datetime 

def ambilData(id):
    npm = "2304111010054"
    id = str(id)
    sensors_type = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    sensors = []
    for sensor in sensors_type:
        link = f"https://belajar-python-unsyiah.an.r.appspot.com/sensor/read?npm={npm}&id_tree={id}&sensor_type={sensor}"
        url = urlopen(link)
        document = json.loads(url.read().decode("utf-8"))
        sensors.append(document)
    return sensors

def extractPointData(data):
  id_tree = data[0]["id_tree"]
  sensor = []
  nilai = []

  for satuData in data:
    tmp = int(satuData["sensor_type"])
    sensor.append(tmp)

    tmp = float(satuData["value"])
    nilai.append(tmp)

  return (id_tree, sensor, nilai)

data = ambilData(4)
(id_tree, sensor_type, value) = extractPointData(data)

print(f"\nID Tree : {id_tree}")
for i in range (len(sensor_type)):
  print(f"Sensor Type {sensor_type[i]}: {value[i]}")