import sqlite3
import json

# Ambil data dari API JSON
data = json.loads('''
{
  "id_tree": 4,
  "sensor_data": {
    "0": 28.1,
    "1": 28.11,
    "2": 28.12,
    "3": 28.12,
    "4": 28.12,
    "5": 28.13,
    "6": 28.13,
    "7": 28.14,
    "8": 28.14,
    "9": 28.15
  }
}
''')

# Buka koneksi ke database
conn = sqlite3.connect('nama_database.db')

# Buat objek cursor
cursor = conn.cursor()

# Buat tabel
cursor.execute('''CREATE TABLE sensor_data (
    id_tree INTEGER,
    sensor_type INTEGER,
    value REAL
)''')

# Simpan data
id_tree = data['id_tree']
for sensor_type, value in data['sensor_data'].items():
    cursor.execute('''INSERT INTO sensor_data (id_tree, sensor_type, value)
                     VALUES (?, ?, ?)''', (id_tree, int(sensor_type), value))

# Simpan perubahan
conn.commit()

# Tutup koneksi
conn.close()