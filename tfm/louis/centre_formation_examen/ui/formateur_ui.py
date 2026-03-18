import tkinter as tk
from tkinter import messagebox, ttk

class FormateurUI:
    #Interface pour gérer les formateurs
    def __init__(self, manager):
        self.manager = manager
        self.window = tk.Toplevel()
        self.window.title("Gestion des formateurs")
        self.window.geometry("900x600")
        self.window.configure(bg="#f0f4f7")

        self.create_widgets()
        self.load_formateurs()

    def create_widgets(self):
        frame = tk.Frame(self.window, bg="#f0f4f7")
        frame.pack(pady=10)

        tk.Label(frame, text="Nom").grid(row=0,column=0,padx=5,pady=5)
        self.nom_entry = tk.Entry(frame)
        self.nom_entry.grid(row=0,column=1,padx=5,pady=5)

        tk.Label(frame, text="Email").grid(row=1,column=0,padx=5,pady=5)
        self.email_entry = tk.Entry(frame)
        self.email_entry.grid(row=1,column=1,padx=5,pady=5)

        tk.Button(frame, text="Créer formateur", command=self.create_formateur, bg="#caffbf").grid(row=2,columnspan=2,pady=10)
        tk.Button(self.window, text="Supprimer formateur", command=self.delete_formateur, bg="#ffadad").pack(pady=5)

        # Tableau
        columns = ("ID","Nom","Email")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill="both", expand=True)

    def create_formateur(self):
        nom = self.nom_entry.get()
        email = self.email_entry.get()
        try:
            self.manager.ajouter_formateur(nom,email)
            self.load_formateurs()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def load_formateurs(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for f in self.manager.get_formateurs():
            self.tree.insert("", "end", values=(f[0], f[1], f[2]))

    def delete_formateur(self):
        selected = self.tree.selection()
        if not selected:
            return
        f_id = self.tree.item(selected)["values"][0]
        self.manager.supprimer_formateur(f_id)
        self.load_formateurs()