from tampilan.tampilan import App
from ambil_data import Takedata
from database import Database

update = Takedata()
db = Database()
app = App()
update.ambil_data()
app.mainloop()