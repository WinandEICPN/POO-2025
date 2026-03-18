"""
Lance l'initialisation de la base de données, puis démarre l'interface graphique.
"""
from database.db_init import initialize_database
from ui.app import App


def main():
    # Initialiser la base de données
    initialize_database()

    # Lancer Tkinter
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()



