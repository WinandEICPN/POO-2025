import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

db = Database()


class App:

    def __init__(self, root):

        self.root = root
        root.title("Choix du Local")

        tk.Label(root, text="Choisir le local").pack(pady=10)

        tk.Button(root, text="Local 1", width=20,
                  command=lambda: self.ouvrir_bureau(1)).pack(pady=5)

        tk.Button(root, text="Local 2", width=20,
                  command=lambda: self.ouvrir_bureau(2)).pack(pady=5)


    def ouvrir_bureau(self, local_id):

        fenetre = tk.Toplevel(self.root)
        fenetre.title("Gestion des équipements")

        tk.Label(fenetre, text="Nom Equipement").grid(row=0, column=0)
        tk.Label(fenetre, text="Etat").grid(row=1, column=0)
        tk.Label(fenetre, text="Bureau").grid(row=2, column=0)

        nom = tk.Entry(fenetre)
        etat = tk.Entry(fenetre)

        nom.grid(row=0, column=1)
        etat.grid(row=1, column=1)

        if local_id == 1:
            bureaux = ["Bureau Directeur", "Bureau Secrétaire"]
        else:
            bureaux = ["Bureau Employé 1", "Bureau Employé 2"]

        bureau = ttk.Combobox(fenetre, values=bureaux)
        bureau.current(0)
        bureau.grid(row=2, column=1)

        listbox = tk.Listbox(fenetre, width=70)
        listbox.grid(row=5, column=0, columnspan=3)

        equipement_ids = []


        def nouveau():

            nom.delete(0, tk.END)
            etat.delete(0, tk.END)

        def ajouter():

            db.execute("""
            INSERT INTO equipements(nom,etat,local_id)
            VALUES(?,?,?)
            """, (nom.get(), etat.get(), local_id))

            afficher()

        def supprimer():

            try:

                index = listbox.curselection()[0]

                equipement_id = equipement_ids[index]

                db.execute("DELETE FROM equipements WHERE id=?", (equipement_id,))

                afficher()

            except:
                messagebox.showwarning("Attention", "Sélectionnez un équipement")


        def afficher():

            listbox.delete(0, tk.END)

            equipement_ids.clear()

            rows = db.execute("""

            SELECT equipements.id,
                   equipements.nom,
                   equipements.etat,
                   locaux.nom

            FROM equipements
            JOIN locaux ON equipements.local_id = locaux.id

            """).fetchall()

            for r in rows:

                equipement_ids.append(r[0])

                phrase = f"{r[1]} est {r[2]} et se trouve dans {r[3]}"

                listbox.insert(tk.END, phrase)


        tk.Button(fenetre, text="Nouveau", width=12,
                  command=nouveau).grid(row=3, column=0)

        tk.Button(fenetre, text="Assigner", width=12,
                  command=ajouter).grid(row=3, column=1)

        tk.Button(fenetre, text="Supprimer", width=12,
                  command=supprimer).grid(row=3, column=2)

        tk.Button(fenetre, text="Afficher", width=12,
                  command=afficher).grid(row=4, column=1)

