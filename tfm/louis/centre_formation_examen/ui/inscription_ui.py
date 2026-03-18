import tkinter as tk
from tkinter import messagebox, ttk

class InscriptionUI:
    #Interface pour inscrire un étudiant à un cours
    def __init__(self, manager):
        self.manager = manager
        self.window = tk.Toplevel()
        self.window.title("Inscrire étudiant à un cours")
        self.window.geometry("900x600")
        self.window.configure(bg="#f0f4f7")

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.window, bg="#f0f4f7")
        frame.pack(pady=20)

        tk.Label(frame, text="Étudiant").grid(row=0,column=0,padx=5,pady=5)
        self.etudiant_combobox = ttk.Combobox(frame, state="readonly")
        self.etudiant_combobox.grid(row=0,column=1,padx=5,pady=5)

        tk.Label(frame, text="Cours").grid(row=1,column=0,padx=5,pady=5)
        self.cours_combobox = ttk.Combobox(frame, state="readonly")
        self.cours_combobox.grid(row=1,column=1,padx=5,pady=5)

        tk.Button(frame, text="Inscrire", command=self.inscrire, bg="#a0c4ff").grid(row=2,columnspan=2,pady=10)

        self.load_comboboxes()

    def load_comboboxes(self):
        etudiants = self.manager.get_etudiants()
        self.etudiant_combobox['values'] = [f"{e[1]} ({e[2]})" for e in etudiants]
        self.etudiant_map = {f"{e[1]} ({e[2]})": e[0] for e in etudiants}

        cours = self.manager.get_cours()
        self.cours_combobox['values'] = [c[1] for c in cours]
        self.cours_map = {c[1]: c[0] for c in cours}

    def inscrire(self):
        etu_text = self.etudiant_combobox.get()
        cours_text = self.cours_combobox.get()
        if etu_text not in self.etudiant_map or cours_text not in self.cours_map:
            messagebox.showerror("Erreur","Sélectionnez étudiant et cours")
            return
        etu_id = self.etudiant_map[etu_text]
        cours_id = self.cours_map[cours_text]

        try:
            self.manager.inscrire(etu_id,cours_id)
            messagebox.showinfo("Succès","Étudiant inscrit avec succès")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))