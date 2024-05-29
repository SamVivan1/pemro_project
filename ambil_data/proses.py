import sqlite3
import datetime as dt
import random
import numpy as np
import matplotlib.dates as mdates

class DatabaseConnection:
    def __enter__(self):
        self.conn = sqlite3.connect("database/database.db")
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

class CRUD:
    def __init__(self):
        pass

    def id_tree_exists(self, id_tree):
        with DatabaseConnection() as cursor:
            cursor.execute('SELECT 1 FROM plants WHERE id_tree = ?', (id_tree,))
            return cursor.fetchone() is not None

    def tambah_tanaman(self, id_tree):
        lat = random.uniform(-90, 90)
        lon = random.uniform(-180, 180)
        time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with DatabaseConnection() as cursor:
            cursor.execute('''
                INSERT INTO plants (id_tree, latitude, longitude, added_timestamp)
                VALUES (?, ?, ?, ?)
            ''', (id_tree, lat, lon, time))

    def tampilkanSensor(self):
        with DatabaseConnection() as cursor:
            cursor.execute('SELECT id_tree, sensors, value, time FROM sensor_data')
            return cursor.fetchall()

    def tampilkanTanaman(self):
        with DatabaseConnection() as cursor:
            cursor.execute('SELECT id_tree, latitude, longitude, added_timestamp FROM plants')
            return cursor.fetchall()

    def hapus(self, id_tree):
        with DatabaseConnection() as cursor:
            cursor.execute('DELETE FROM plants WHERE id_tree = ?', (id_tree,))
            cursor.execute('DELETE FROM sensor_data WHERE id_tree = ?', (id_tree,))

class Grafik:
    def __init__(self):
        pass

    def ambil_rata_rata_sensor(self, waktu_mulai, waktu_akhir):
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        data_rata_rata = {i: None for i in range(10)}  # Inisialisasi dictionary dengan 10 sensor

        cursor.execute('''
        SELECT sensors, AVG(value)
        FROM sensor_data
        WHERE time BETWEEN ? AND ?
        GROUP BY sensors
        ''', (waktu_mulai, waktu_akhir))

        baris_baris = cursor.fetchall()
        for baris in baris_baris:
            sensor_type, avg_nilai = baris
            data_rata_rata[sensor_type] = avg_nilai

        conn.close()
        return data_rata_rata
    
    def ambil_data_sensor(self, id_tree, sensor_type, waktu_mulai, waktu_akhir):
        print(f"Mengambil data dari {waktu_mulai} hingga {waktu_akhir}")

        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT value, time
        FROM sensor_data
        WHERE id_tree = ? AND sensors = ? AND time BETWEEN ? AND ?
        ORDER BY time
        ''', (id_tree, sensor_type, waktu_mulai, waktu_akhir))
        data = cursor.fetchall()
        conn.close()
        print(f"Data yang ditemukan: {data}")
        return data
    
    def interpolasi_data_hilang(timestamps, nilai, waktu_mulai, waktu_akhir):
        """Interpolasi data untuk mengisi nilai yang hilang di titik awal dan akhir."""
        timestamps = np.array([mdates.date2num(ts) for ts in timestamps])
        nilai = np.array(nilai)

        # Mengonversi string waktu ke objek datetime
        mulai_waktu = mdates.date2num(dt.datetime.strptime(waktu_mulai, '%Y-%m-%d %H:%M:%S'))
        akhir_waktu = mdates.date2num(dt.datetime.strptime(waktu_akhir, '%Y-%m-%d %H:%M:%S'))

        # Jika timestamps tidak memiliki mulai_waktu atau akhir_waktu tambahkan mereka dengan interpolasi
        if mulai_waktu not in timestamps:
            nilai_awal = np.interp(mulai_waktu, timestamps, nilai)
            timestamps = np.insert(timestamps, 0, mulai_waktu)
            nilai = np.insert(nilai, 0, nilai_awal)

        if akhir_waktu not in timestamps:
            nilai_akhir = np.interp(akhir_waktu, timestamps, nilai)
            timestamps = np.append(timestamps, akhir_waktu)
            nilai = np.append(nilai, nilai_akhir)

        # konversi kembali timestamps ke datetime tanpa zona waktu
        timestamps = [mdates.num2date(ts) for ts in timestamps]

        return timestamps, nilai

if __name__ == "__main__":
    db = Grafik()
    data = db.ambil_data_sensor(1, 0, "2024-05-28 00:00:00", "2024-05-29 23:59:59")
    print(data)
