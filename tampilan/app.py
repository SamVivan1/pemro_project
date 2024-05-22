import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1920x1080")  # set window size

# tabview
tabview = customtkinter.CTkTabview(master=app)
tabview.pack(padx=20, pady=20)

tabview.add("Tambah")  # add tab at the end
tabview.add("Tampil")  # add tab at the end
tabview.add("Ubah")
tabview.add("Hapus")

label = customtkinter.CTkLabel(master=tabview.tab("Tambah"), text="ID Tree")
label.pack(padx=10, pady=10)
entry = customtkinter.CTkEntry(master=tabview.tab("Tambah"), placeholder_text="Masukkan ID")
entry.pack(padx=10, pady=10)
button = customtkinter.CTkButton(master=tabview.tab("Tambah"), text="Tambah", command=lambda: print(entry.get()))
button.pack(padx=10, pady=10)

app.mainloop()