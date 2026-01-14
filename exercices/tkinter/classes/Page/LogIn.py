# =========================
# UI Tkinter
# =========================
from tkinter import messagebox

import tkinter as tk

from exercices.tkinter.classes.db.DAO import UserDao


class LogIn:
    def __init__(self, root: tk.Tk, dao: UserDao):
        self.root = root
        self.dao = dao

        self.root.title("Mini Login")
        self.root.geometry("360x160")
        self.root.resizable(False, False)

        # Labels
        tk.Label(root, text="Nom :").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Label(root, text="Mot de passe :").grid(row=1, column=0, padx=10, pady=10, sticky="e")

        # Entries
        self.entry_nom = tk.Entry(root, width=25)
        self.entry_pwd = tk.Entry(root, width=25, show="*")

        self.entry_nom.grid(row=0, column=1, padx=10, pady=10)
        self.entry_pwd.grid(row=1, column=1, padx=10, pady=10)

        # Buttons
        btn_add = tk.Button(root, text="Add", width=12, command=self.on_add)
        btn_connect = tk.Button(root, text="Connect", width=12, command=self.on_connect)

        btn_add.grid(row=2, column=0, padx=10, pady=15)
        btn_connect.grid(row=2, column=1, padx=10, pady=15, sticky="w")

    def _get_inputs(self):
        nom = self.entry_nom.get().strip()
        pwd = self.entry_pwd.get().strip()
        return nom, pwd

    def on_add(self):
        nom, pwd = self._get_inputs()

        if not nom or not pwd:
            messagebox.showerror("Erreur", "Nom et mot de passe obligatoires.")
            return

        ok = self.dao.add_user(nom, pwd)
        if ok:
            messagebox.showinfo("OK", f"Utilisateur '{nom}' ajouté.")
            self.entry_pwd.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", f"Le nom '{nom}' existe déjà.")

    def on_connect(self):
        nom, pwd = self._get_inputs()

        if not nom or not pwd:
            messagebox.showerror("Erreur", "Nom et mot de passe obligatoires.")
            return

        if self.dao.user_exists(nom, pwd):
            messagebox.showinfo("Connexion", "Accès autorisé ✅")
        else:
            messagebox.showerror("Connexion", "Accès refusé ❌")
