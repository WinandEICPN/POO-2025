# Import de la bibliothèque Tkinter
# Tkinter est utilisé pour créer l'interface graphique de l'application

import tkinter as tk

# Import de la classe Station
# Cette classe contient la logique métier (gestion des pompes et des ventes)
from station import Station

# Cette classe gère toute l'interface graphique de l'application.
# Elle permet à l'utilisateur de sélectionner un carburant et d'effectuer une vente
class Interface:
    def __init__(self):         # Constructeur de la classe
        self.station = Station()

        self.fenetre = tk.Tk()
        self.fenetre.title("Station d'essence")
        self.fenetre.geometry("300x250")

#Affiche le titre de station en bold et en couleur vert
        tk.Label(
            self.fenetre,
            text="STATION TORAL",
            fg="green",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

# Création d'un label indiquant le choix du carburant
        tk.Label(self.fenetre, text="Type de carburant").pack()

        self.carburant = tk.StringVar()      # Variable Tkinter permettant de stocker la valeur choisie dans le menu
        self.carburant.set("Essence 95")

# Création d'un menu déroulant permettant de choisir le type de carburant
        tk.OptionMenu(
            self.fenetre,
            self.carburant,
            "Essence 95",
            "Essence 98",
            "Diesel"
        ).pack()
# Label indiquant où entrer le nombre de litres
        tk.Label(self.fenetre, text="Nombre de litres", fg="red").pack()

# Champ de saisie permettant à l'utilisateur d'entrer la quantité de carburant
        self.entree_litres = tk.Entry(self.fenetre)
        self.entree_litres.pack()

 # Bouton permettant de lancer l'opération de vente
# Lorsque l'utilisateur clique sur ce bouton, la méthode vendre() est appelée
        tk.Button(
            self.fenetre,
            text="Vendre",
            command=self.vendre
        ).pack(pady=10)

# Label permettant d'afficher un message à l'utilisateur
        self.message = tk.Label(self.fenetre, text="")
        self.message.pack()

# Cette boucle maintient la fenêtre ouverte et attend les actions de l'utilisateur.
        self.fenetre.mainloop()

 # Méthode appelée lorsque l'utilisateur clique sur le bouton "Vendre"
    def vendre(self):
        try:
            litres = float(self.entree_litres.get())         # Récupération du nombre de litres saisi par l'utilisateur
            type_carburant = self.carburant.get()
            resultat = self.station.vendre(type_carburant, litres)
            self.message.config(text=resultat, fg="green")      # Message de succès en vert

# Si l'utilisateur entre une valeur non numérique
# un message d'erreur est affiché
        except ValueError:
            # Message d'erreur en rouge
            self.message.config(text="Veuillez entrer un nombre valide", fg="red")
