# Point d'entrée de l'app
#initialisation de la DB et ensuite on lance l'interface graphique.

from database import DBConnection
from init_db import initialiser_base
from ui import Application


def main():
# 1) on ouvre la connexion à la DB via le Singleton
    DBConnection.get_instance("crypto.db")

# 2) on crée les tables et insère les données de départ
    initialiser_base()

# 3) on lance l'interface graphique Tkinter
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()