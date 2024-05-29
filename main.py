from tampilan.tampilan import App
from ambil_data import Takedata

def main():
    update = Takedata()
    app = App()
    update.ambil_data()
    app.mainloop()

if __name__ == "__main__":
    main()