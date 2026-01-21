# =========================
# UI Tkinter
# =========================
from tkinter import messagebox, ttk

import tkinter as tk

from exercices.tkinter.classes.db.DAO import UserDao


class LogIn:
    def __init__(self, root: tk.Tk, dao: UserDao):
        self.root = root
        self.dao = dao

        self.root.title("Mini Login")
        self.root.geometry("720x200")
        self.root.resizable(False, False)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.frame_add = tk.LabelFrame(root, text="Ajouter un utilisateur", padx=10, pady=10)
        self.frame_add.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_connect = tk.LabelFrame(root, text="Connexion", padx=10, pady=10)
        self.frame_connect.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Labels
        tk.Label(self.frame_add, text="Nom :").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Label(self.frame_add, text="Mot de passe :").grid(row=1, column=0, padx=10, pady=10, sticky="e")

        # Entries
        self.entry_add_nom = tk.Entry(self.frame_add, width=25)
        self.entry_add_pwd = tk.Entry(self.frame_add, width=25, show="*")

        self.entry_add_nom.grid(row=0, column=1, padx=10, pady=10)
        self.entry_add_pwd.grid(row=1, column=1, padx=10, pady=10)

        # Buttons
        btn_add = tk.Button(self.frame_add, text="Add", width=12, command=self.on_add)
        btn_add.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.frame_connect, text="Utilisateur :").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Label(self.frame_connect, text="Mot de passe :").grid(row=1, column=0, sticky="e", padx=5, pady=5)

        self.combo_user = ttk.Combobox(self.frame_connect, width=22, state="readonly")
        self.refresh_users()

        self.entry_connect_pwd = tk.Entry(self.frame_connect, width=25, show="*")
        self.combo_user.grid(row=0, column=1, padx=5, pady=5)
        self.entry_connect_pwd.grid(row=1, column=1, padx=5, pady=5)
        btn_connect = tk.Button(self.frame_connect, text="Connect", width=12, command=self.on_connect)
        btn_connect.grid(row=2, column=1, columnspan=2, pady=10)

    def _get_inputs(self):
        nom = self.entry_add_nom.get().strip()
        pwd = self.entry_add_pwd.get().strip()
        return nom, pwd

    def on_add(self):
        nom, pwd = self._get_inputs()
        if not nom or not pwd:
            messagebox.showerror("Erreur", "Nom et mot de passe obligatoires.")
            return
        ok = self.dao.add_user(nom, pwd)
        if ok:
            messagebox.showinfo("OK", f"Utilisateur '{nom}' ajouté.")
            self.entry_add_pwd.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", f"Le nom '{nom}' existe déjà.")

    def on_connect(self):
        nom = self.combo_user.get().strip()
        pwd = self.entry_connect_pwd.get().strip()
        if not nom or not pwd:
            messagebox.showerror("Erreur", "Nom et mot de passe obligatoires.")
            return
        if self.dao.user_exists(nom, pwd):
            messagebox.showinfo("Connexion", "Accès autorisé ✅")
        else:
            messagebox.showerror("Connexion", "Accès refusé ❌")

    def refresh_users(self):
        users = self.dao.get_all_usernames()
        self.combo_user["values"] = users
        if users:
            self.combo_user.current(0)  # sélectionne le premier
        else:
            self.combo_user.set("")  # vide si aucun user
