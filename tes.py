import tkinter as tk

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (HomePage, Page1, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(HomePage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Home Page")
        label.pack(pady=10,padx=10)
        
        button1 = tk.Button(self, text="Go to Page 1",
                            command=lambda: controller.show_frame(Page1))
        button1.pack()
        
        button2 = tk.Button(self, text="Go to Page 2",
                            command=lambda: controller.show_frame(Page2))
        button2.pack()

class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page 1")
        label.pack(pady=10,padx=10)
        
        button = tk.Button(self, text="Go to Home",
                           command=lambda: controller.show_frame(HomePage))
        button.pack()

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page 2")
        label.pack(pady=10,padx=10)
        
        button = tk.Button(self, text="Go to Home",
                           command=lambda: controller.show_frame(HomePage))
        button.pack()

app = MyApp()
app.mainloop()
