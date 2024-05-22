import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("700x550")  # set window size

# tabview
def menu():
    tabview = customtkinter.CTkTabview(master=app)
    tabview.pack(padx=20, pady=20, fill="both", expand=True)

    tabview.add("Tambah")  # add tab at the end
    tabview.add("Tampil")  # add tab at the end
    tabview.add("Ubah")
    tabview.add("Hapus")

    # menu tambah
    entry = customtkinter.CTkEntry(master=tabview.tab("Tambah"), placeholder_text="Masukkan ID")
    entry.pack(padx=10, pady=10)
    entry2 = customtkinter.CTkEntry(master=tabview.tab("Tambah"), placeholder_text="Masukkan ID Sensor ")
    entry2.pack(padx=10, pady=10)
    button = customtkinter.CTkButton(master=tabview.tab("Tambah"), text="Tambah", command=lambda: print(f"{entry.get()}\n{entry2.get()}"))
    button.pack(padx=10, pady=10)

    # menu tampil
    entry3 = customtkinter.CTkEntry(master=tabview.tab("Tampil"), placeholder_text="Masukkan ID")
    entry3.pack(padx=10, pady=10)
    button2 = customtkinter.CTkButton(master=tabview.tab("Tampil"), text="Tampil", command=lambda: print(f"{entry3.get()}"))
    button2.pack(padx=10, pady=10)

    # menu ubah
    option = customtkinter.CTkOptionMenu(master=tabview.tab("Ubah"), values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
    option.pack(padx=10, pady=10)
    button3 = customtkinter.CTkButton(master=tabview.tab("Ubah"), text="Ubah", command=lambda: print(f"{option.get()}"))
    button3.pack(padx=10, pady=10)


