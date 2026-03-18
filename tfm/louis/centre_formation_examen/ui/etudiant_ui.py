import tkinter as tk
from tkinter import messagebox, ttk

class EtudiantUI:
    #Interface pour gérer les étudiants
    def __init__(self, manager):
        self.manager = manager
        self.window = tk.Toplevel()
        self.window.title("Gestion des étudiants")
        self.window.geometry("900x600")
        self.window.configure(bg="#f0f4f7")

        self.create_widgets()
        self.load_etudiants()

    def create_widgets(self):
        frame = tk.Frame(self.window, bg="#f0f4f7")
        frame.pack(pady=10)

        tk.Label(frame, text="Nom").grid(row=0,column=0,padx=5,pady=5)
        self.nom_entry = tk.Entry(frame)
        self.nom_entry.grid(row=0,column=1,padx=5,pady=5)

        tk.Label(frame, text="Email").grid(row=1,column=0,padx=5,pady=5)
        self.email_entry = tk.Entry(frame)
        self.email_entry.grid(row=1,column=1,padx=5,pady=5)

        tk.Button(frame, text="Créer étudiant", command=self.create_etudiant, bg="#a0c4ff").grid(row=2,columnspan=2,pady=10)
        tk.Button(self.window, text="Supprimer étudiant", command=self.delete_etudiant, bg="#ffadad").pack(pady=5)

        # Tableau
        columns = ("ID","Nom","Email")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill="both", expand=True)

    def create_etudiant(self):
        nom = self.nom_entry.get()
        email = self.email_entry.get()
        try:
            self.manager.ajouter_etudiant(nom,email)
            self.load_etudiants()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def load_etudiants(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for e in self.manager.get_etudiants():
            self.tree.insert("", "end", values=(e[0], e[1], e[2]))

    def delete_etudiant(self):
        selected = self.tree.selection()
        if not selected:
            return
        etu_id = self.tree.item(selected)["values"][0]
        self.manager.supprimer_etudiant(etu_id)
        self.load_etudiants()