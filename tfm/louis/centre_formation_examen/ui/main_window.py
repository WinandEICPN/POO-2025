import tkinter as tk
from tkinter import PhotoImage
from ui.etudiant_ui import EtudiantUI
from ui.formateur_ui import FormateurUI
from ui.cours_ui import CoursUI
from ui.inscription_ui import InscriptionUI
from ui.inscriptions_recap_ui import InscriptionsRecapUI
from manager.centre_manager import CentreManager
import os

class MainWindow:
    """
    Fenêtre principale du Centre de Formation
    Avec message de bienvenue, description fine, logo et boutons modernes
    """
    def __init__(self, root):
        self.manager = CentreManager()
        self.window = root
        self.window.title("Centre de Formation")
        self.window.geometry("900x600")
        self.window.configure(bg="#f0f4f7")


        # Message de bienvenue
        tk.Label(self.window,
                 text="Bienvenue au Centre de Formation",
                 font=("Helvetica", 24, "bold"),
                 fg="#333",
                 bg="#f0f4f7").pack(pady=(20, 5))

        # Description 
        description_text = (
            "Cette application vous permet de gérer de manière centralisée "
            "vos étudiants, formateurs et cours.\n\n"
            "Vous pouvez ajouter, modifier ou supprimer les informations, "
            "ainsi que suivre les inscriptions des étudiants pour chaque cours.\n\n"
            "Chaque formateur peut avoir plusieurs cours, et chaque étudiant "
            "peut s’inscrire à différents cours, le tout de façon simple et sécurisée."
        )

        tk.Label(self.window,
                 text=description_text,
                 font=("Helvetica", 12),
                 fg="#555",
                 bg="#f0f4f7",
                 justify="center",
                 wraplength=700).pack(pady=(0, 20))

        # Frame pour boutons
        frame = tk.Frame(self.window, bg="#f0f4f7")
        frame.pack(pady=30)

        # Boutons avec couleurs et espacement
        btn_config = {
            "width": 20,
            "height": 2,
            "font": ("Helvetica", 12, "bold"),
            "bd": 0,
            "relief": "ridge"
        }

        tk.Button(frame, text="Gérer étudiants", command=self.open_etudiants,
                  bg="#4dabf7", fg="white", **btn_config).grid(row=0, column=0, padx=15, pady=10)
        tk.Button(frame, text="Gérer formateurs", command=self.open_formateurs,
                  bg="#51cf66", fg="white", **btn_config).grid(row=0, column=1, padx=15, pady=10)
        tk.Button(frame, text="Gérer cours", command=self.open_cours,
                  bg="#fcc419", fg="white", **btn_config).grid(row=1, column=0, padx=15, pady=10)
        tk.Button(frame, text="Inscrire étudiant", command=self.open_inscription,
                  bg="#ff6b6b", fg="white", **btn_config).grid(row=1, column=1, padx=15, pady=10)
        tk.Button(frame, text="Récap inscriptions", command=self.open_recap,
                  bg="#9775fa", fg="white", **btn_config).grid(row=2, column=0, columnspan=2, pady=15)

    # Méthodes pour ouvrir les fenêtres
    def open_etudiants(self):
        EtudiantUI(self.manager)

    def open_formateurs(self):
        FormateurUI(self.manager)

    def open_cours(self):
        CoursUI(self.manager)

    def open_inscription(self):
        InscriptionUI(self.manager)

    def open_recap(self):
        InscriptionsRecapUI(self.manager)