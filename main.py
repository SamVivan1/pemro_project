"""
The main entry point of the application. This function sets up the main application window and starts the main event loop.

The `Takedata` class is used to retrieve data, and the `MainApp` class is used to create and display the main application window. The `ambil_data()` method of the `Takedata` class is called to retrieve the data, and the `mainloop()` method of the `MainApp` class is called to start the main event loop.
"""

from tampilan.tampilan import MainApp
from ambil_data import Takedata

def main():
    update = Takedata()
    app = MainApp()
    update.ambil_data()
    app.mainloop()

if __name__ == "__main__":
    main()