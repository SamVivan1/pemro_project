import tkinter
import customtkinter

app = customtkinter.CTk()
app.geometry("1024x640")  # set window size
app.title("Data Sensor Collector")  # set window title
app.resizable(width=False, height=False)   

right_frame = customtkinter.CTkFrame(master=app, fg_color="light gray")
right_frame.pack(side="right", fill="both", expand=True)

left_frame = customtkinter.CTkFrame(master=app, fg_color="dark gray")
left_frame.pack(side="left", fill="both", expand=True)

tabview = customtkinter.CTkTabview(master=right_frame)
tabview.pack(padx=10, pady=10, fill="both", expand=True)

tab = tabview.add("Tambah")
tab2 = tabview.add("kurang")
tab3 = tabview.add("bagi")


app.mainloop()