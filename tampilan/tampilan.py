import customtkinter
from CTkMessagebox import CTkMessagebox
from ambil_data.proses import CRUD
from PIL import Image, ImageTk
import tkinter
from database import Database

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x640")  # set window size
        self.title("Data Sensor Collector")  # set window title
        
        # background images
        self.img1 = ImageTk.PhotoImage(Image.open("assets/images.png"))
        self.l1 = customtkinter.CTkLabel(master=self, image=self.img1)
        self.l1.pack(padx=1, pady=1, fill="both", expand=True)

        # Add GUI input to the right side
        self.tabview = customtkinter.CTkTabview(master=self.l1, corner_radius=32)
        self.tabview.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # Add tabs
        self.menu_tambah = MenuTambah(self.tabview)
        self.menu_daftar = MenuDaftar(self.tabview)
        self.menu_tampil = MenuTampil(self.tabview)
        self.menu_hapus = MenuHapus(self.tabview)

class Messagebox:
    def __init__(self):
        pass

    def show_info(self, message):
        CTkMessagebox(title="Info", message=message)
    
    def show_error(self, message):
        CTkMessagebox(title="Error", message=message)
    
    def show_warning(self, message):
        CTkMessagebox(title="Warning", message=message, icon="warning")

    def show_question(self, message):
        CTkMessagebox(title="Question", message=message, icon="question", option_1="Yes", option_2="No")

    def show_checkmark(self, message):
        CTkMessagebox(title="Checkmark", message=message, icon="check")
        

class MenuDaftar:
    def __init__(self, parent):
        self.tab = parent.add("Daftar ID Tree")
        self.textbox = customtkinter.CTkTextbox(master=self.tab, state="disabled", height=400, width=700)
        self.textbox.pack(padx=10, pady=10)
        proses = Database()
        pesan = Messagebox()
        data = proses.get_all_plants_data()
        if not data:
            pesan.show_info("Tidak ada data")
            return
        textbox_data = ""
        for row in data:
            textbox_data += f"ID Tree: {row[0]:<5}, Latitude: {row[1]:<25}, Longitude: {row[2]:<25}, Waktu: {row[3]:<10}\n\n"
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("0.0", textbox_data)
        self.textbox.configure(state="disabled")

class MenuTambah:
    def __init__(self, parent):
        self.tab = parent.add("Tambah")
        self.entry = customtkinter.CTkEntry(corner_radius=32, master=self.tab, placeholder_text="Masukkan ID")
        self.entry.pack(padx=10, pady=10)
        self.button = customtkinter.CTkButton(corner_radius=32, master=self.tab, text="Tambah", command=self.tambah)
        self.button.pack(padx=10, pady=10)

    def tambah(self):
        data = self.entry.get()
        proses = CRUD()
        pesan = Messagebox()
        if data.strip() and data.isdigit():
            if proses.id_tree_exists(data):
                pesan.show_error(f"ID {data} sudah ada")
                return
            proses.tambah_tanaman(data)
            print(f"Tambah: {data}")
            pesan.show_checkmark(f"Berhasil menambahkan data dengan ID: {data}")
            self.entry.delete(0, 'end')
        else:
            pesan.show_warning(f"ID tidak boleh kosong")

class MenuTampil:
    def __init__(self, parent):
        self.tab = parent.add("Tampil")
        self.button1 = customtkinter.CTkButton(corner_radius=32, master=self.tab, text="Grafik 1 Tanaman", command=self.satu_tanaman)
        self.button1.pack(padx=10, pady=10)
        self.button2 = customtkinter.CTkButton(corner_radius=32, master=self.tab, text="Mean Semua Sensor Tanaman", command=self.show_mean)
        self.button2.pack(padx=10, pady=10)
        self.toplevel = None

    def satu_tanaman(self):
        if self.toplevel is None or not self.toplevel.winfo_exists():
            self.toplevel = satuTanaman()  # create window if its None or destroyed
        else:
            self.toplevel.focus()  # if window exists focus it

    def show_mean(self):
        if self.toplevel is None or not self.toplevel.winfo_exists():
            self.toplevel = meanTanaman()  # create window if its None or destroyed
        else:
            self.toplevel.focus()  # if window exists focus it
        
class satuTanaman(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("440x500")  # set window size
        self.title("Tampilkan")  # set window title
        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.l = customtkinter.CTkLabel(master=self.frame, text="Tampilkan Grafik 1 Tanaman", font=("Arial", 20, "bold"))
        self.l.pack(pady=50)
        self.entry0 = customtkinter.CTkEntry(corner_radius=32, master=self.frame, width=177,placeholder_text="Masukkan ID")
        self.entry0.pack(pady=10, padx=10)
        self.button = customtkinter.CTkButton(corner_radius=32, master=self.frame, text="Tampilkan", command=self.minta_waktu)
        self.button.pack(pady=4, padx=10)
        
    def minta_id(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.l = customtkinter.CTkLabel(master=self.frame, text="Tampilkan Grafik 1 Tanaman", font=("Arial", 20, "bold"))
        self.l.pack(pady=50)
        self.entry0 = customtkinter.CTkEntry(corner_radius=32, master=self.frame, width=177,placeholder_text="Masukkan ID")
        self.entry0.pack(pady=4, padx=10)
        self.button = customtkinter.CTkButton(corner_radius=32, master=self.frame, text="Tampilkan", command=self.minta_waktu)
        self.button.pack(pady=4, padx=10)

    def minta_waktu(self):
        data = self.entry0.get()
        pesan = Messagebox()
        if data.strip() and data.isdigit():
            proses = CRUD()
            if proses.id_tree_exists(data):
                for widget in self.frame.winfo_children():
                    widget.destroy()
                self.l = customtkinter.CTkLabel(master=self.frame, text="Tampilkan Grafik 1 Tanaman", font=("Arial", 20, "bold"))
                self.l.pack(pady=50)
                self.label = customtkinter.CTkLabel(master=self.frame, text="Waktu Mulai (YYYY-MM-DD HH:MM:SS)")
                self.label.pack(pady=4, padx=10)
                self.entry = customtkinter.CTkEntry(corner_radius=32, master=self.frame, width=177,placeholder_text="Masukkan Waktu")
                self.entry.pack(pady=4, padx=10)
                self.label1 = customtkinter.CTkLabel(master=self.frame, text="Waktu Selesai (YYYY-MM-DD HH:MM:SS)")
                self.label1.pack(pady=4, padx=10)
                self.entry1 = customtkinter.CTkEntry(corner_radius=32, master=self.frame, width=177,placeholder_text="Masukkan Waktu")
                self.entry1.pack(pady=4, padx=10)
                self.button = customtkinter.CTkButton(corner_radius=32, master=self.frame, text="Tampilkan")
                self.button1 = customtkinter.CTkButton(corner_radius=32, master=self.frame, text="Kembali", command=self.minta_id)
                self.button.pack(pady=20, side="left", padx=10)
                self.button1.pack(pady=20, side="left", padx=10)
                
            else:
                pesan.show_error(f"ID {data} tidak ditemukan")
        else:
            pesan.show_warning(f"ID tidak boleh kosong")
        
class meanTanaman(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("440x500")  # set window size
        self.title("Tampilkan")  # set window title
        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.l = customtkinter.CTkLabel(master=self.frame, text="Tampilkan Grafik Mean", font=("Arial", 20, "bold"))
        self.l.pack(pady=50)
        self.entry0 = customtkinter.CTkEntry(corner_radius=32, master=self.frame, width=177,placeholder_text="Masukkan ID")
        self.entry0.pack(pady=10, padx=10)
        self.button = customtkinter.CTkButton(corner_radius=32, master=self.frame, text="Tampilkan", command=self.minta_waktu)
        self.button.pack(pady=4, padx=10)

    def minta_waktu(self):
        data = self.entry0.get()
        pesan = Messagebox()
        if data.strip() and data.isdigit():
            proses = CRUD()
            if proses.id_tree_exists(data):
                for widget in self.frame.winfo_children():
                    widget.destroy()
                self.l = customtkinter.CTkLabel(master=self.frame, text="Tampilkan Grafik Mean", font=("Arial", 20, "bold"))
                self.l.pack(pady=50)
                self.label = customtkinter.CTkLabel(master=self.frame, text="Waktu Mulai (YYYY-MM-DD HH:MM:SS)")
                self.label.pack(pady=4, padx=10)
                self.entry = customtkinter.CTkEntry(corner_radius=32, master=self.frame, width=177,placeholder_text="Masukkan Waktu")
                self.entry.pack(pady=4, padx=10)
                self.label1 = customtkinter.CTkLabel(master=self.frame, text="Waktu Selesai (YYYY-MM-DD HH:MM:SS)")
                self.label1.pack(pady=4, padx=10)
                self.entry1 = customtkinter.CTkEntry(corner_radius=32, master=self.frame, width=177,placeholder_text="Masukkan Waktu")
                self.entry1.pack(pady=4, padx=10)
                self.button = customtkinter.CTkButton(corner_radius=32, master=self.frame, text="Tampilkan")
                self.button.pack(pady=20, padx=10)
                
            else:
                pesan.show_error(f"ID {data} tidak ditemukan")
        else:
            pesan.show_warning(f"ID tidak boleh kosong")
    
class MenuHapus:
    def __init__(self, parent):
        self.tab = parent.add("Hapus")
        self.entry = customtkinter.CTkEntry(corner_radius=32, master=self.tab, placeholder_text="Masukkan ID")
        self.entry.pack(padx=10, pady=10)
        self.button = customtkinter.CTkButton(corner_radius=32, master=self.tab, text="Hapus", command=self.hapus)
        self.button.pack(padx=10, pady=10)

    def hapus(self):
        proses = CRUD()
        pesan = Messagebox()
        data = self.entry.get()
        if not data.isdigit():
            pesan.show_warning(f"ID tidak boleh kosong atau harus berupa angka")
            return
        else:
            if not proses.id_tree_exists(data):
                pesan.show_warning(f"ID {data} tidak ditemukan")
                return
            msg = CTkMessagebox(title="Question", message=f"Apakah anda yakin ingin menghapus ID {data}?", icon="question", option_1="Yes", option_2="No")  
        if msg.get() == "Yes":
            proses.hapus(data)
            print(f"Hapus: {data}")
            self.entry.delete(0, 'end')
            pesan.show_checkmark(f"Berhasil menghapus data dengan ID: {data}")


if __name__ == "__main__":
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("blue")
    
        
