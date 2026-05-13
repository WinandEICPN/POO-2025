import tkinter as tk

from livre_service import (
    ajouter_livre,
    afficher_emprunts_actifs,
    afficher_livres,
    emprunter_livre,
    rendre_livre,
    supprimer_livre,
)
from utilisateur_service import utilisateur_existe


def ouvrir_fenetre_livres():
    win = tk.Toplevel()
    win.title("Gestion des livres")
    win.geometry("900x520")
    win.configure(bg="#4f86c6")

    action_var = tk.StringVar(value="Ajouter un livre")
    couleurs_actions = {
        "Ajouter un livre": "#f4d35e",
        "Supprimer un livre": "#ee964b",
        "Emprunter un livre": "#7bd389",
        "Rendre un livre": "#f28482",
        "Afficher les livres": "#84a59d",
    }

    actions_frame = tk.Frame(win, pady=10, bg="#4f86c6")
    actions_frame.pack(fill="x")

    formulaire = tk.Frame(win, pady=10, bg="#4f86c6")
    formulaire.pack(fill="x")

    label_livre = tk.Label(formulaire, text="Nom du livre", bg="#4f86c6", fg="white")
    entry_livre = tk.Entry(formulaire, width=40)

    label_utilisateur = tk.Label(
        formulaire, text="Nom de l'utilisateur", bg="#4f86c6", fg="white"
    )
    entry_utilisateur = tk.Entry(formulaire, width=40)

    label_duree = tk.Label(formulaire, text="Duree en jours", bg="#4f86c6", fg="white")
    entry_duree = tk.Entry(formulaire, width=40)

    label_message = tk.Label(win, bg="#4f86c6", fg="white")
    label_message.pack()

    text = tk.Text(win, width=90, height=20)
    text.pack(padx=10, pady=10, fill="both", expand=True)

    boutons_action = {}

    def masquer_champs():
        label_livre.grid_forget()
        entry_livre.grid_forget()
        label_utilisateur.grid_forget()
        entry_utilisateur.grid_forget()
        label_duree.grid_forget()
        entry_duree.grid_forget()

    def vider_champs():
        entry_livre.delete(0, tk.END)
        entry_utilisateur.delete(0, tk.END)
        entry_duree.delete(0, tk.END)

    def afficher_liste_livres():
        text.delete("1.0", tk.END)
        text.insert(tk.END, "Liste des livres\n")
        text.insert(tk.END, "-" * 70 + "\n")
        for livre in afficher_livres():
            statut = "Disponible" if livre[2] == 1 else "Emprunte"
            text.insert(tk.END, f"Livre: {livre[1]} | Statut: {statut}\n")

    def afficher_liste_emprunts():
        emprunts = afficher_emprunts_actifs()
        if not emprunts:
            return
        text.insert(tk.END, "\nEmprunts en cours\n")
        text.insert(tk.END, "-" * 70 + "\n")
        for emprunt in emprunts:
            text.insert(
                tk.END,
                f"Livre: {emprunt[1]} | Utilisateur: {emprunt[2]} | "
                f"Duree: {emprunt[3]} jours | Date: {emprunt[4]}\n",
            )

    def executer_action():
        action = action_var.get()
        titre = entry_livre.get().strip()
        utilisateur = entry_utilisateur.get().strip()
        duree = entry_duree.get().strip()

        if action == "Ajouter un livre":
            if not titre:
                label_message.config(text="Nom du livre invalide")
                return
            _, message = ajouter_livre(titre)
            label_message.config(text=message)
            afficher_liste_livres()
            vider_champs()
            return

        if action == "Supprimer un livre":
            if not titre:
                label_message.config(text="Nom du livre invalide")
                return
            _, message = supprimer_livre(titre)
            label_message.config(text=message)
            afficher_liste_livres()
            vider_champs()
            return

        if action == "Emprunter un livre":
            if not titre:
                label_message.config(text="Nom du livre invalide")
                return
            if not utilisateur:
                label_message.config(text="Nom utilisateur invalide")
                return
            if not utilisateur_existe(utilisateur):
                label_message.config(
                    text="Utilisateur non enregistre. Inscrivez-vous d'abord"
                )
                return
            try:
                duree_jours = int(duree)
                if duree_jours <= 0:
                    raise ValueError
            except ValueError:
                label_message.config(text="Duree invalide")
                return
            _, message = emprunter_livre(titre, utilisateur, duree_jours)
            label_message.config(text=message)
            afficher_liste_livres()
            afficher_liste_emprunts()
            vider_champs()
            return

        if action == "Rendre un livre":
            if not titre:
                label_message.config(text="Nom du livre invalide")
                return
            if not utilisateur:
                label_message.config(text="Nom utilisateur invalide")
                return
            _, message = rendre_livre(titre, utilisateur)
            label_message.config(text=message)
            afficher_liste_livres()
            afficher_liste_emprunts()
            vider_champs()
            return

        if action == "Afficher les livres":
            label_message.config(text="")
            afficher_liste_livres()
            afficher_liste_emprunts()

    def choisir_action(action):
        action_var.set(action)
        label_message.config(text="")
        masquer_champs()

        for nom_action, bouton in boutons_action.items():
            relief = "sunken" if nom_action == action else "raised"
            bouton.config(relief=relief, bd=3)

        if action == "Ajouter un livre":
            label_livre.grid(row=0, column=0, sticky="w", padx=10, pady=5)
            entry_livre.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
            entry_livre.focus_set()
        elif action == "Supprimer un livre":
            label_livre.grid(row=0, column=0, sticky="w", padx=10, pady=5)
            entry_livre.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
            entry_livre.focus_set()
        elif action == "Emprunter un livre":
            label_livre.grid(row=0, column=0, sticky="w", padx=10, pady=5)
            entry_livre.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
            label_utilisateur.grid(row=1, column=0, sticky="w", padx=10, pady=5)
            entry_utilisateur.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
            label_duree.grid(row=2, column=0, sticky="w", padx=10, pady=5)
            entry_duree.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
            entry_livre.focus_set()
        elif action == "Rendre un livre":
            label_livre.grid(row=0, column=0, sticky="w", padx=10, pady=5)
            entry_livre.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
            label_utilisateur.grid(row=1, column=0, sticky="w", padx=10, pady=5)
            entry_utilisateur.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
            entry_livre.focus_set()
        elif action == "Afficher les livres":
            executer_action()

    formulaire.columnconfigure(1, weight=1)

    for index, action in enumerate(
        [
            "Ajouter un livre",
            "Supprimer un livre",
            "Emprunter un livre",
            "Rendre un livre",
            "Afficher les livres",
        ]
    ):
        bouton = tk.Button(
            actions_frame,
            text=action,
            width=18,
            height=3,
            bg=couleurs_actions[action],
            activebackground=couleurs_actions[action],
            command=lambda valeur=action: choisir_action(valeur),
        )
        bouton.grid(row=0, column=index, padx=6, pady=6, sticky="nsew")
        actions_frame.columnconfigure(index, weight=1)
        boutons_action[action] = bouton

    entry_livre.bind("<Return>", lambda _event: executer_action())
    entry_utilisateur.bind("<Return>", lambda _event: executer_action())
    entry_duree.bind("<Return>", lambda _event: executer_action())

    choisir_action("Ajouter un livre")
