import tkinter as tk

from db import Database
from livre_ui import ouvrir_fenetre_livres
from utilisateur_ui import ouvrir_fenetre_utilisateurs


def main():
    db = Database()
    db.create_tables()

    root = tk.Tk()
    root.title("Bibliotheque")
    root.geometry("760x360")
    root.minsize(760, 360)
    root.configure(bg="#2f6db3")

    container = tk.Frame(root, padx=30, pady=30, bg="#2f6db3")
    container.pack(expand=True, fill="both")
    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)
    container.rowconfigure(0, weight=1)

    btn_livres = tk.Button(
        container,
        text="Livres",
        command=ouvrir_fenetre_livres,
        width=20,
        height=8,
        font=("Arial", 16, "bold"),
        bg="#9a9a9a",
        activebackground="#888888",
    )
    btn_livres.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    btn_utilisateurs = tk.Button(
        container,
        text="Utilisateurs",
        command=ouvrir_fenetre_utilisateurs,
        width=20,
        height=8,
        font=("Arial", 16, "bold"),
        bg="#f39a2b",
        activebackground="#db8620",
    )
    btn_utilisateurs.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    root.mainloop()


if __name__ == "__main__":
    main()
