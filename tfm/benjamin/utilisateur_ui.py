import tkinter as tk

from utilisateur_service import (
    ajouter_utilisateur,
    afficher_utilisateurs,
    modifier_utilisateur,
    supprimer_utilisateur,
)


def ouvrir_fenetre_utilisateurs():
    win = tk.Toplevel()
    win.title("Utilisateurs")
    win.geometry("820x500")
    win.configure(bg="#4f86c6")

    action_var = tk.StringVar(value="Ajouter un utilisateur")
    couleurs_actions = {
        "Ajouter un utilisateur": "#b8e1ff",
        "Modifier un utilisateur": "#ffd6a5",
        "Supprimer un utilisateur": "#ffadad",
        "Afficher les utilisateurs": "#caffbf",
    }

    actions_frame = tk.Frame(win, pady=10, bg="#4f86c6")
    actions_frame.pack(fill="x")

    formulaire = tk.Frame(win, pady=10, bg="#4f86c6")
    formulaire.pack(fill="x")

    label_nom = tk.Label(formulaire, text="Nom", bg="#4f86c6", fg="white")
    entry_nom = tk.Entry(formulaire, width=40)

    label_nouveau_nom = tk.Label(
        formulaire, text="Nouveau nom", bg="#4f86c6", fg="white"
    )
    entry_nouveau_nom = tk.Entry(formulaire, width=40)

    label_message = tk.Label(win, bg="#4f86c6", fg="white")
    label_message.pack()

    text = tk.Text(win, width=80, height=20)
    text.pack(padx=10, pady=10, fill="both", expand=True)

    boutons_action = {}

    def masquer_champs():
        label_nom.grid_forget()
        entry_nom.grid_forget()
        label_nouveau_nom.grid_forget()
        entry_nouveau_nom.grid_forget()

    def vider_champs():
        entry_nom.delete(0, tk.END)
        entry_nouveau_nom.delete(0, tk.END)

    def afficher():
        text.delete("1.0", tk.END)
        utilisateurs = afficher_utilisateurs()
        if not utilisateurs:
            text.insert(tk.END, "Aucun utilisateur enregistre\n")
            return
        for utilisateur in utilisateurs:
            text.insert(tk.END, f"Nom: {utilisateur[1]}\n")

    def executer_action():
        action = action_var.get()
        nom = entry_nom.get().strip()
        nouveau_nom = entry_nouveau_nom.get().strip()

        if action == "Ajouter un utilisateur":
            if not nom:
                label_message.config(text="Nom invalide")
                return
            _, message = ajouter_utilisateur(nom)
            label_message.config(text=message)
            afficher()
            vider_champs()
            return

        if action == "Modifier un utilisateur":
            if not nom:
                label_message.config(text="Nom actuel invalide")
                return
            if not nouveau_nom:
                label_message.config(text="Nouveau nom invalide")
                return
            _, message = modifier_utilisateur(nom, nouveau_nom)
            label_message.config(text=message)
            afficher()
            vider_champs()
            return

        if action == "Supprimer un utilisateur":
            if not nom:
                label_message.config(text="Nom invalide")
                return
            _, message = supprimer_utilisateur(nom)
            label_message.config(text=message)
            afficher()
            vider_champs()
            return

        if action == "Afficher les utilisateurs":
            label_message.config(text="")
            afficher()

    def choisir_action(action):
        action_var.set(action)
        label_message.config(text="")
        masquer_champs()

        for nom_action, bouton in boutons_action.items():
            relief = "sunken" if nom_action == action else "raised"
            bouton.config(relief=relief, bd=3)

        if action == "Ajouter un utilisateur":
            label_nom.grid(row=0, column=0, sticky="w", padx=10, pady=5)
            entry_nom.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
            entry_nom.focus_set()
        elif action == "Modifier un utilisateur":
            label_nom.grid(row=0, column=0, sticky="w", padx=10, pady=5)
            entry_nom.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
            label_nouveau_nom.grid(row=1, column=0, sticky="w", padx=10, pady=5)
            entry_nouveau_nom.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
            entry_nom.focus_set()
        elif action == "Supprimer un utilisateur":
            label_nom.grid(row=0, column=0, sticky="w", padx=10, pady=5)
            entry_nom.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
            entry_nom.focus_set()
        elif action == "Afficher les utilisateurs":
            executer_action()

    formulaire.columnconfigure(1, weight=1)

    for index, action in enumerate(
        [
            "Ajouter un utilisateur",
            "Modifier un utilisateur",
            "Supprimer un utilisateur",
            "Afficher les utilisateurs",
        ]
    ):
        bouton = tk.Button(
            actions_frame,
            text=action,
            width=20,
            height=3,
            bg=couleurs_actions[action],
            activebackground=couleurs_actions[action],
            command=lambda valeur=action: choisir_action(valeur),
        )
        bouton.grid(row=0, column=index, padx=6, pady=6, sticky="nsew")
        actions_frame.columnconfigure(index, weight=1)
        boutons_action[action] = bouton

    entry_nom.bind("<Return>", lambda _event: executer_action())
    entry_nouveau_nom.bind("<Return>", lambda _event: executer_action())

    choisir_action("Ajouter un utilisateur")
