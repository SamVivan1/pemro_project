import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import sqlite3
import json
from threading import Thread, Event
import time
import urllib.request
import random
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

NPM = 'NPM_KLEN'
URL_SENSOR_READ = 'https://belajar-python-unsyiah.an.r.appspot.com/sensor/read'

# Event untuk menghentikan pengambilan data sensor
stop_event = Event()
deleted_plants = set()  # Set untuk menyimpan ID tanaman yang telah dihapus

def initialize_db():
    conn = sqlite3.connect('plants.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS plants (
        id_tree INTEGER PRIMARY KEY,
        latitude REAL,
        longitude REAL,
        added_timestamp TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id_tree INTEGER,
        sensor_type INTEGER,
        reading REAL,
        timestamp TEXT,
        PRIMARY KEY (id_tree, sensor_type, timestamp)
    )
    ''')
    conn.commit()
    conn.close()

def format_timestamp_gmt(timestamp):
    """Format the timestamp to GMT format."""
    dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')

# Fungsi utama untuk mengambil data sensor
def fetch_sensor_data(id_tree, sensor_type):
    try:
        full_url = f"{URL_SENSOR_READ}?npm={NPM}&id_tree={id_tree}&sensor_type={sensor_type}"
        print(f"Mengambil data dari URL: {full_url}")
        with urllib.request.urlopen(full_url) as response:
            data = json.loads(response.read().decode('utf-8'))
            reading = data['value']
            timestamp = data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # Ambil timestamp dari data atau gunakan waktu saat ini
            print(f"Data diambil untuk id_tanaman={id_tree}, tipe_sensor={sensor_type}: {data}")
            return reading, timestamp
    except Exception as e:
        print(f"Gagal mengambil data untuk id_tanaman={id_tree}, tipe_sensor={sensor_type}: {e}")
        return None, None

# Fungsi untuk menyimpan data sensor ke dalam database
def save_sensor_data(id_tree, sensor_type, reading, timestamp):
    try:
        conn = sqlite3.connect('plants.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO sensor_data (id_tree, sensor_type, reading, timestamp)
        VALUES (?, ?, ?, ?)
        ''', (id_tree, sensor_type, reading, timestamp))
        conn.commit()
        conn.close()
        print(f"Data disimpan untuk id_tanaman={id_tree}, tipe_sensor={sensor_type}, pembacaan={reading}, waktu={timestamp}")
    except sqlite3.IntegrityError as e:
        print(f"Gagal menyimpan data untuk id_tanaman={id_tree}, tipe_sensor={sensor_type}, waktu={timestamp}: {e}")

def show_sensor_data(id_tree):
    sensor_labels = {
        0: "Suhu udara (°C)",
        1: "Kelembaban udara (%)",
        2: "Curah hujan (mm)",
        3: "Tingkat sinar UV",
        4: "Suhu tanah (°C)",
        5: "Kelembaban tanah (%)",
        6: "pH tanah",
        7: "Kadar N dalam tanah (mg/kg)",
        8: "Kadar P dalam tanah (mg/kg)",
        9: "Kadar K dalam tanah (mg/kg)"
    }

    conn = sqlite3.connect('plants.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT sensor_type, reading, MAX(timestamp) 
    FROM sensor_data 
    WHERE id_tree = ?
    GROUP BY sensor_type
    ''', (id_tree,))
    data = cursor.fetchall()

    cursor.execute('SELECT latitude, longitude, added_timestamp FROM plants WHERE id_tree = ?', (id_tree,))
    plant_info = cursor.fetchone()
    conn.close()

    print(f"Data diambil untuk id_tanaman={id_tree}: {data}")

    if not data:
        messagebox.showinfo("Tidak Ada Data", "Tidak ada data yang ditemukan untuk tanaman yang ditentukan.")
        return

    latitude, longitude, added_timestamp = plant_info if plant_info else (None, None, None)

    result = f"id: {id_tree} | lat: {latitude} | lon: {longitude}\n"
    if added_timestamp:
        result += f"Date: {format_timestamp_gmt(added_timestamp)}\n\n"
    else:
        result += "Date: Tidak Tersedia\n\n"

    # Tampilkan nilai pembacaan sensor dalam satuan SI dan dengan keterangan
    for sensor_type, reading, timestamp in data:
        result += f"{sensor_labels.get(sensor_type, f'Sensor {sensor_type}')}: {reading}\n"

    # Tampilkan hasil dalam widget Text
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, result)
    text_widget.config(state=tk.DISABLED)

def add_plant():
    id_tree = simpledialog.askinteger("Input", "Masukkan ID Tanaman:")
    if id_tree is None:
        return

    latitude = random.uniform(-90, 90)  # Generate random latitude
    longitude = random.uniform(-180, 180)  # Generate random longitude
    added_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Generate current timestamp

    conn = sqlite3.connect('plants.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO plants (id_tree, latitude, longitude, added_timestamp) VALUES (?, ?, ?, ?)', (id_tree, latitude, longitude, added_timestamp))
        conn.commit()
        messagebox.showinfo("Sukses", "Tanaman berhasil ditambahkan")
        print(f"Tanaman ditambahkan dengan id_tanaman={id_tree}, latitude={latitude}, longitude={longitude}, waktu_ditambahkan={added_timestamp}")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "ID Tanaman sudah ada.")
    finally:
        conn.close()

def delete_plant():
    id_tree = simpledialog.askinteger("Input", "Masukkan ID Tanaman yang akan dihapus:")
    if id_tree is None:
        return

    conn = sqlite3.connect('plants.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sensor_data WHERE id_tree = ?', (id_tree,))
    cursor.execute('DELETE FROM plants WHERE id_tree = ?', (id_tree,))
    conn.commit()
    conn.close()

    deleted_plants.add(id_tree)  # Tambahkan ID tanaman yang dihapus ke set
    messagebox.showinfo("Sukses", f"Tanaman dengan ID {id_tree} dan semua data sensornya telah dihapus.")
    print(f"Tanaman dihapus dengan id_tanaman={id_tree} dan semua data sensornya")

def start_sensor_fetching():
    def fetch_data_periodically():
        while not stop_event.is_set():
            conn = sqlite3.connect('plants.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id_tree FROM plants')
            plants = cursor.fetchall()
            conn.close()

            for plant in plants:
                id_tree = plant[0]
                if id_tree in deleted_plants:
                    continue  # Lewati ID tanaman yang telah dihapus
                for sensor_type in range(10):
                    reading, timestamp = fetch_sensor_data(id_tree, sensor_type)
                    if reading is not None and timestamp is not None:
                        save_sensor_data(id_tree, sensor_type, reading, timestamp)

            time.sleep(60)

    thread = Thread(target=fetch_data_periodically)
    thread.daemon = True
    thread.start()

def on_show_data():
    id_tree = simpledialog.askinteger("Input", "Masukkan ID Tanaman:")
    if id_tree is not None:
        show_sensor_data(id_tree)
        
# Fungsi untuk menampilkan semua tanaman yang terdaftar beserta data sensornya
def show_all_plants():
    sensor_labels = {
        0: "Suhu udara (°C)",
        1: "Kelembaban udara (%)",
        2: "Curah hujan (mm)",
        3: "Tingkat sinar UV",
        4: "Suhu tanah (°C)",
        5: "Kelembaban tanah (%)",
        6: "pH tanah",
        7: "Kadar N dalam tanah (mg/kg)",
        8: "Kadar P dalam tanah (mg/kg)",
        9: "Kadar K dalam tanah (mg/kg)"
    }

    conn = sqlite3.connect('plants.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id_tree, latitude, longitude, added_timestamp FROM plants')
    plants = cursor.fetchall()
    conn.close()

    if not plants:
        messagebox.showinfo("Tidak Ada Tanaman", "Tidak ada tanaman yang ditemukan di database.")
        return

    result = ""
    for plant in plants:
        id_tree, latitude, longitude, added_timestamp = plant
        result += f"id: {id_tree} | lat: {latitude} | lon: {longitude}\n"
        if added_timestamp:
            result += f"Date: {format_timestamp_gmt(added_timestamp)}\n"
        else:
            result += "Date: Tidak Tersedia\n"

        conn = sqlite3.connect('plants.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT sensor_type, reading, MAX(timestamp)
        FROM sensor_data
        WHERE id_tree = ?
        GROUP BY sensor_type
        ''', (id_tree,))
        data = cursor.fetchall()
        conn.close()

        for sensor_type, reading, timestamp in data:
            result += f"{sensor_labels.get(sensor_type, f'Sensor {sensor_type}')}: {reading} (Waktu: {timestamp})\n"
        result += "\n"

    # Tampilkan hasil dalam widget Text
    all_plants_text_widget.config(state=tk.NORMAL)
    all_plants_text_widget.delete(1.0, tk.END)
    all_plants_text_widget.insert(tk.END, result)
    all_plants_text_widget.config(state=tk.DISABLED)

def fetch_sensor_data_for_graph(id_tree, sensor_type, start_time, end_time):
    print(f"Mengambil data dari {start_time} hingga {end_time}")  # Debugging print
    conn = sqlite3.connect('plants.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT reading, timestamp
    FROM sensor_data
    WHERE id_tree = ? AND sensor_type = ? AND timestamp BETWEEN ? AND ?
    ORDER BY timestamp
    ''', (id_tree, sensor_type, start_time, end_time))
    data = cursor.fetchall()
    conn.close()
    print(f"Data yang ditemukan: {data}")  # Debugging print
    return data

def interpolate_missing_data(timestamps, readings, start_time, end_time):
    """Interpolasi data untuk mengisi nilai yang hilang di titik awal dan akhir."""
    # Pastikan timestamps dan readings adalah numpy array untuk memudahkan manipulasi
    timestamps = np.array([mdates.date2num(ts) for ts in timestamps])
    readings = np.array(readings)

    # Konversi start_time dan end_time ke datetime dan kemudian ke float
    start_dt = mdates.date2num(datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc))
    end_dt = mdates.date2num(datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc))

    # Jika timestamps tidak memiliki start_dt atau end_dt, tambahkan mereka dengan interpolasi
    if start_dt not in timestamps:
        start_value = np.interp(start_dt, timestamps, readings)
        timestamps = np.insert(timestamps, 0, start_dt)
        readings = np.insert(readings, 0, start_value)

    if end_dt not in timestamps:
        end_value = np.interp(end_dt, timestamps, readings)
        timestamps = np.append(timestamps, end_dt)
        readings = np.append(readings, end_value)

    # Konversi kembali timestamps ke datetime
    timestamps = [mdates.num2date(ts).replace(tzinfo=timezone.utc) for ts in timestamps]

    return timestamps, readings

def plot_sensor_graph(id_tree, sensor_type, sensor_name, start_time, end_time):
    data = fetch_sensor_data_for_graph(id_tree, sensor_type, start_time, end_time)
    if not data:
        messagebox.showinfo("Tidak Ada Data", f"Tidak ada data yang ditemukan untuk sensor {sensor_name} dalam rentang waktu yang diminta.")
        return

    readings, timestamps = zip(*data)
    timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S').astimezone(timezone.utc) for ts in timestamps]

    # Interpolasi data jika diperlukan
    timestamps, readings = interpolate_missing_data(timestamps, readings, start_time, end_time)

    # Daftar warna untuk setiap sensor
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown']

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, readings, marker='o', linestyle='-', label=sensor_name, color=colors[sensor_type % len(colors)])
    plt.title(f'Grafik {sensor_name} untuk ID Tanaman {id_tree}')
    plt.xlabel('Waktu (GMT)')
    plt.ylabel(sensor_name)

    # Atur interval sumbu-x menjadi 1 jam
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M', tz=timezone.utc))

    plt.gcf().autofmt_xdate()
    plt.grid(True)

    plt.legend()
    plt.show()

def show_graph_options(id_tree):
    sensor_labels = {
        0: "Suhu udara (°C)",
        1: "Kelembaban udara (%)",
        2: "Curah hujan (mm)",
        3: "Tingkat sinar UV",
        4: "Suhu tanah (°C)",
        5: "Kelembaban tanah (%)",
        6: "pH tanah",
        7: "Kadar N dalam tanah (mg/kg)",
        8: "Kadar P dalam tanah (mg/kg)",
        9: "Kadar K dalam tanah (mg/kg)"
    }

    def on_sensor_select(sensor_type):
        start_time = simpledialog.askstring("Input", "Masukkan waktu mulai (YYYY-MM-DD HH:MM:SS):")
        end_time = simpledialog.askstring("Input", "Masukkan waktu selesai (YYYY-MM-DD HH:MM:SS):")

        try:
            if start_time and end_time:  # Tambahan pemeriksaan apakah start_time dan end_time tidak None
                # Parsing start_time dan end_time
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

                # Konversi waktu ke UTC
                start_time = start_time.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                end_time = end_time.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

                plot_sensor_graph(id_tree, sensor_type, sensor_labels[sensor_type], start_time, end_time)
            else:
                messagebox.showerror("Error", "Waktu mulai dan waktu selesai harus diisi.")  # Pesan kesalahan jika salah satu waktu tidak diisi
        except ValueError as e:
            messagebox.showerror("Error", f"Format waktu salah: {e}")


    window = tk.Toplevel(root)
    window.title("Pilih Sensor untuk Menampilkan Grafik")

    for sensor_type, label in sensor_labels.items():
        button = tk.Button(window, text=label, command=lambda st=sensor_type: on_sensor_select(st))
        button.pack(pady=5)

def on_show_graphs():
    id_tree = simpledialog.askinteger("Input", "Masukkan ID Tanaman:")
    if id_tree is not None:
        show_graph_options(id_tree)

def fetch_average_sensor_data(start_time, end_time):
    conn = sqlite3.connect('plants.db')
    cursor = conn.cursor()
    average_data = {}

    # Mengambil data rata-rata untuk setiap ID tanaman dalam rentang waktu yang ditentukan
    cursor.execute('''
    SELECT id_tree, AVG(reading)
    FROM sensor_data
    WHERE timestamp BETWEEN ? AND ?
    GROUP BY id_tree
    ''', (start_time, end_time))

    rows = cursor.fetchall()
    for row in rows:
        id_tree, avg_reading = row
        average_data[id_tree] = avg_reading

    conn.close()
    return average_data

def on_show_average_data():
    start_time = simpledialog.askstring("Input", "Masukkan waktu mulai (YYYY-MM-DD HH:MM:SS):")
    end_time = simpledialog.askstring("Input", "Masukkan waktu selesai (YYYY-MM-DD HH:MM:SS):")

    try:
        if start_time and end_time:  # Tambahan pemeriksaan apakah start_time dan end_time tidak None
            
            # Parsing start_time dan end_time
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

            # Konversi waktu ke UTC
            start_time = start_time.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            end_time = end_time.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

            average_data = fetch_average_sensor_data(start_time, end_time)  # Menyertakan start_time dan end_time
            if average_data:
                plot_average_sensor_graph(average_data, start_time, end_time)  # Menyertakan start_time dan end_time
            else:
                messagebox.showinfo("Tidak Ada Data", "Tidak ada data rata-rata sensor yang ditemukan.")
        else:
            messagebox.showerror("Error", "Waktu mulai dan waktu selesai harus diisi.")  # Pesan kesalahan jika salah satu waktu tidak diisi
    except ValueError as e:
        messagebox.showerror("Error", f"Format waktu salah: {e}")

def plot_average_sensor_graph(average_data, start_time, end_time):
    sensor_labels = {
        0: "Suhu udara (°C)",
        1: "Kelembaban udara (%)",
        2: "Curah hujan (mm)",
        3: "Tingkat sinar UV",
        4: "Suhu tanah (°C)",
        5: "Kelembaban tanah (%)",
        6: "pH tanah",
        7: "Kadar N dalam tanah (mg/kg)",
        8: "Kadar P dalam tanah (mg/kg)",
        9: "Kadar K dalam tanah (mg/kg)"
    }

    num_sensors = len(sensor_labels)
    fig, ax = plt.subplots(figsize=(12, 8))

    # Menyiapkan array untuk posisi bar
    bar_positions = np.arange(num_sensors)

    # Menyiapkan array untuk lebar bar
    bar_width = 0.35

    # Menyiapkan array untuk label bar
    bar_labels = [sensor_labels[i] for i in range(num_sensors)]

    # Menyiapkan warna untuk setiap bar
    colors = ['skyblue', 'salmon', 'lightgreen', 'gold', 'lightcoral', 
              'lightskyblue', 'orange', 'mediumseagreen', 'lightpink', 'lightgrey']

    # Plot bar untuk rata-rata pembacaan sensor dengan warna yang berbeda
    bars = ax.bar(bar_positions, average_data.values(), bar_width, label='Rata-rata Nilai Sensor', color=colors)

    # Tambahkan label pada sumbu-x
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(bar_labels, rotation=45, ha='right')

    # Tambahkan label pada sumbu-y
    ax.set_ylabel('Rata-rata Nilai Sensor')

    # Tambahkan judul dengan keterangan rentang waktu
    ax.set_title(f'Rata-rata Sensor untuk Setiap Tipe Sensor Semua Tanaman\nRentang Waktu: {start_time} - {end_time}')

    # Tambahkan grid
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Tambahkan legend
    ax.legend()

    # Tambahkan nilai rata-rata di atas bar
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')

    # Tambahkan keterangan untuk warna bar
    legend_labels = [f"Sensor {i}: {sensor_labels[i]}" for i in range(num_sensors)]
    ax.legend(bars, legend_labels)

    plt.tight_layout()
    plt.show()

def format_time_to_gmt(timestamp):
    """Format timestamp to HH:MM GMT."""
    dt = timestamp.replace(tzinfo=timezone.utc)
    return dt.strftime('%H:%M GMT')

def show_main_menu():
    frame_add_plant.pack_forget()
    frame_show_data.pack_forget()
    frame_delete_plant.pack_forget()
    frame_show_all_plants.pack_forget()
    frame_graph.pack_forget()
    frame_main_menu.pack(pady=10)

    # Hapus konten dari text_widget saat kembali ke menu utama
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    text_widget.config(state=tk.DISABLED)

def show_add_plant():
    frame_main_menu.pack_forget()
    frame_add_plant.pack(pady=10)

def show_show_data():
    frame_main_menu.pack_forget()
    frame_show_data.pack(pady=10)

def show_delete_plant():
    frame_main_menu.pack_forget()
    frame_delete_plant.pack(pady=10)

def show_all_plants_frame():
    frame_main_menu.pack_forget()
    frame_show_all_plants.pack(pady=10)

    # Hapus konten dari all_plants_text_widget saat kembali ke menu utama
    all_plants_text_widget.config(state=tk.NORMAL)
    all_plants_text_widget.delete(1.0, tk.END)
    all_plants_text_widget.config(state=tk.DISABLED)

def show_graph_frame():
    frame_main_menu.pack_forget()
    frame_graph.pack(pady=10)

initialize_db()

root = tk.Tk()
root.title("Plant Monitor App")

frame_main_menu = tk.Frame(root)
frame_main_menu.pack(pady=10)

btn_add_plant = tk.Button(frame_main_menu, text="Tambah Tanaman", command=show_add_plant)
btn_add_plant.grid(row=0, column=0, padx=5, pady=5)

btn_show_data = tk.Button(frame_main_menu, text="Tampilkan Data Sensor", command=show_show_data)
btn_show_data.grid(row=0, column=1, padx=5, pady=5)

btn_delete_plant = tk.Button(frame_main_menu, text="Hapus Tanaman", command=show_delete_plant)
btn_delete_plant.grid(row=0, column=2, padx=5, pady=5)

# Tombol baru untuk menampilkan daftar semua tanaman
btn_show_all_plants = tk.Button(frame_main_menu, text="Daftar Tanaman", command=show_all_plants_frame)
btn_show_all_plants.grid(row=0, column=3, padx=5, pady=5)

# Tombol baru untuk menampilkan grafik sensor
btn_show_graphs = tk.Button(frame_main_menu, text="Grafik Sensor", command=show_graph_frame)
btn_show_graphs.grid(row=0, column=4, padx=5, pady=5)

frame_add_plant = tk.Frame(root)
btn_add_plant_confirm = tk.Button(frame_add_plant, text="Konfirmasi Tambah Tanaman", command=add_plant)
btn_add_plant_confirm.pack(pady=10)
btn_back_to_main_from_add = tk.Button(frame_add_plant, text="Kembali ke Menu Utama", command=show_main_menu)
btn_back_to_main_from_add.pack(pady=10)

frame_show_data = tk.Frame(root)
btn_show_data_confirm = tk.Button(frame_show_data, text="Masukkan ID Tanaman", command=on_show_data)
btn_show_data_confirm.pack(pady=10)
text_widget = tk.Text(frame_show_data, wrap=tk.WORD, state=tk.DISABLED, width=60, height=20)
text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
btn_back_to_main_from_show = tk.Button(frame_show_data, text="Kembali ke Menu Utama", command=show_main_menu)
btn_back_to_main_from_show.pack(pady=10)

frame_delete_plant = tk.Frame(root)
btn_delete_plant_confirm = tk.Button(frame_delete_plant, text="Masukkan ID Tanaman yang Akan Dihapus", command=delete_plant)
btn_delete_plant_confirm.pack(pady=10)
btn_back_to_main_from_delete = tk.Button(frame_delete_plant, text="Kembali ke Menu Utama", command=show_main_menu)
btn_back_to_main_from_delete.pack(pady=10)

# Frame untuk menampilkan semua tanaman yang terdaftar
frame_show_all_plants = tk.Frame(root)

# Scrollbar untuk widget Text
scrollbar = tk.Scrollbar(frame_show_all_plants)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

btn_show_all_plants_confirm = tk.Button(frame_show_all_plants, text="Tampilkan Semua Tanaman", command=show_all_plants)
btn_show_all_plants_confirm.pack(pady=10)

all_plants_text_widget = tk.Text(frame_show_all_plants, wrap=tk.WORD, state=tk.DISABLED, width=60, height=20, yscrollcommand=scrollbar.set)
all_plants_text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

scrollbar.config(command=all_plants_text_widget.yview)

btn_back_to_main_from_show_all = tk.Button(frame_show_all_plants, text="Kembali ke Menu Utama", command=show_main_menu)
btn_back_to_main_from_show_all.pack(pady=10)

# Frame untuk menampilkan grafik sensor
frame_graph = tk.Frame(root)
btn_graph_confirm = tk.Button(frame_graph, text="Masukkan ID Tanaman", command=on_show_graphs)
btn_graph_confirm.pack(pady=10)
btn_back_to_main_from_graph = tk.Button(frame_graph, text="Kembali ke Menu Utama", command=show_main_menu)
btn_back_to_main_from_graph.pack(pady=10)

# Frame untuk menampilkan grafik sensor
frame_graph = tk.Frame(root)
btn_graph_confirm = tk.Button(frame_graph, text="Masukkan ID Tanaman", command=on_show_graphs)
btn_graph_confirm.pack(pady=10)

# Button to show average sensor data
btn_show_average_data = tk.Button(frame_graph, text="Tampilkan Rata-rata Sensor", command=on_show_average_data)
btn_show_average_data.pack(pady=10)

btn_back_to_main_from_graph = tk.Button(frame_graph, text="Kembali ke Menu Utama", command=show_main_menu)
btn_back_to_main_from_graph.pack(pady=10)


start_sensor_fetching()

root.mainloop()
