import tkinter as tk
from tkinter import messagebox, ttk

class CoursUI:
    #Interface pour gérer les cours
    def __init__(self, manager):
        self.manager = manager
        self.window = tk.Toplevel()
        self.window.title("Gestion des cours")
        self.window.geometry("900x600")
        self.window.configure(bg="#f0f4f7")

        self.create_widgets()
        self.load_cours()

    def create_widgets(self):
        frame = tk.Frame(self.window, bg="#f0f4f7")
        frame.pack(pady=10)

        tk.Label(frame, text="Titre").grid(row=0,column=0,padx=5,pady=5)
        self.titre_entry = tk.Entry(frame)
        self.titre_entry.grid(row=0,column=1,padx=5,pady=5)

        tk.Label(frame, text="Durée (heures)").grid(row=1,column=0,padx=5,pady=5)
        self.duree_entry = tk.Entry(frame)
        self.duree_entry.grid(row=1,column=1,padx=5,pady=5)

        tk.Label(frame, text="Formateur").grid(row=2,column=0,padx=5,pady=5)
        self.formateur_combobox = ttk.Combobox(frame, state="readonly")
        self.formateur_combobox.grid(row=2,column=1,padx=5,pady=5)
        self.load_formateurs_combobox()

        tk.Button(frame, text="Créer cours", command=self.create_course, bg="#ffd6a5").grid(row=3,columnspan=2,pady=10)
        tk.Button(self.window, text="Supprimer cours", command=self.delete_cours, bg="#ffadad").pack(pady=5)

        # Tableau
        columns = ("ID","Titre","Durée","Formateur")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill="both", expand=True)

    def load_formateurs_combobox(self):
        formateurs = self.manager.get_formateurs()
        self.formateur_combobox['values'] = [f"{f[1]} ({f[2]})" for f in formateurs]
        self.formateur_map = {f"{f[1]} ({f[2]})": f[0] for f in formateurs}

    def create_course(self):
        titre = self.titre_entry.get()
        duree = self.duree_entry.get()
        formateur_text = self.formateur_combobox.get()
        if formateur_text not in self.formateur_map:
            messagebox.showerror("Erreur", "Sélectionnez un formateur")
            return
        formateur_id = self.formateur_map[formateur_text]
        try:
            self.manager.creer_cours(titre,duree,formateur_id)
            self.load_cours()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def load_cours(self):
        self.load_formateurs_combobox()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for c in self.manager.get_cours():
            f_nom = self.manager.get_formateurs()
            formateur_name = next((f[1] for f in self.manager.get_formateurs() if f[0]==c[3]),"Inconnu")
            self.tree.insert("", "end", values=(c[0], c[1], c[2], formateur_name))

    def delete_cours(self):
        selected = self.tree.selection()
        if not selected:
            return
        c_id = self.tree.item(selected)["values"][0]
        self.manager.supprimer_cours(c_id)
        self.load_cours()