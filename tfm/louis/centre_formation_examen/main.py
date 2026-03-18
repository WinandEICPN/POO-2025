import tkinter as tk
from ui.main_window import MainWindow
from database.database import Database

    # Point d'entrée principal du programme
if __name__ == "__main__":
    
    # Création de la fenêtre principale Tkinter
    root = tk.Tk()

    # Instanciation de la fenêtre principale avec le root
    app = MainWindow(root)

    # Fonction pour fermer proprement l'application
    def on_close():
        # Fermer la base de données pour éviter les corruptions
        Database().close()
        # Détruire la fenêtre principale
        root.destroy()

    # Lier la fermeture de la fenêtre à on_close
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Lancer la boucle principale Tkinter
    root.mainloop()