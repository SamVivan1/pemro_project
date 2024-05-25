import customtkinter
from CTkMessagebox import CTkMessagebox
from proses import CRUD

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x550")  # set window size
        self.tabview = customtkinter.CTkTabview(master=self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Add tabs
        self.menu_tambah = MenuTambah(self.tabview)
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
        

class MenuTambah:
    def __init__(self, parent):
        self.tab = parent.add("Tambah")
        self.entry = customtkinter.CTkEntry(master=self.tab, placeholder_text="Masukkan ID")
        self.entry.pack(padx=10, pady=10)
        self.button = customtkinter.CTkButton(master=self.tab, text="Tambah", command=self.tambah)
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
        self.entry = customtkinter.CTkEntry(master=self.tab, placeholder_text="Masukkan ID")
        self.entry.pack(padx=10, pady=10)
        self.button = customtkinter.CTkButton(master=self.tab, text="Tampil", command=self.tampil)
        self.button.pack(padx=10, pady=10)

    def tampil(self):
        proses = CRUD()
        if not self.entry.get().isdigit():
            Messagebox().show_warning(f"ID tidak boleh kosong atau harus berupa angka")
            return
        

class MenuHapus:
    def __init__(self, parent):
        self.tab = parent.add("Hapus")
        self.entry = customtkinter.CTkEntry(master=self.tab, placeholder_text="Masukkan ID")
        self.entry.pack(padx=10, pady=10)
        self.button = customtkinter.CTkButton(master=self.tab, text="Hapus", command=self.hapus)
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
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    app = App()
    app.mainloop()
