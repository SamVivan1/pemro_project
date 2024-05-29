"""
The main entry point of the application. This function is responsible for creating an instance of the `Takedata` class to fetch data, and an instance of the `App` class to run the main application loop.
"""
from tampilan.tampilan import App
from ambil_data import Takedata

def main():
    update = Takedata()
    app = App()
    update.ambil_data()
    app.mainloop()

if __name__ == "__main__":
    main()