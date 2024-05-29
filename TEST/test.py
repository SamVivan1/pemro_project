import customtkinter
import tkcalendar

app = customtkinter.CTk()  

def tampil():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    start_datetime = f"{start_date} 00:00:00"
    end_datetime = f"{end_date} 23:59:59"
    print(start_datetime)
    print(end_datetime)

start_date_label = customtkinter.CTkLabel(master=app, text="Tanggal Mulai:")
start_date_label.pack(pady=5)
start_date_entry = tkcalendar.DateEntry(master=app, date_pattern='yyyy-mm-dd')
start_date_entry.pack(pady=5)
end_date_label = customtkinter.CTkLabel(master=app, text="Tanggal Akhir:")
end_date_label.pack(pady=5)
end_date_entry = tkcalendar.DateEntry(master=app, date_pattern='yyyy-mm-dd')
end_date_entry.pack(pady=5)
button = customtkinter.CTkButton(corner_radius=32, master=app, text="Tampilkan", command=tampil)
button.pack(pady=20)
                





app.mainloop()