
# Interface graphique Tkinter de la plateforme de cryptomonnaies.
# L'interface appelle uniquement le service, jamais la base de données directement.


import tkinter as tk
from tkinter import messagebox

from services import CryptoService


class Application(tk.Tk):
   #fenetre principale plateforme crypto

    def __init__(self):
        super().__init__()
        self.title("Plateforme Cryptomonnaies")
        self.geometry("700x500")
        self.resizable(False, False)

        # le service contient toute la logique metier
        self.__service = CryptoService()

        self.__construire_interface()

    def __construire_interface(self):
        """Construit la barre de navigation et la zone principale."""

        # barre de boutons en haut
        barre = tk.Frame(self, bd=1, relief=tk.RAISED)
        barre.pack(side=tk.TOP, fill=tk.X)

        tk.Button(barre, text="Accueil",    command=self.__page_accueil).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(barre, text="Acheter",    command=self.__page_achat).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(barre, text="Vendre",     command=self.__page_vente).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(barre, text="Historique", command=self.__page_historique).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(barre, text="Stocks",     command=self.__page_stocks).pack(side=tk.LEFT, padx=5, pady=5)

        # compteur de transactions a droite dans la barre
        self.__label_compteur = tk.Label(barre, text="")
        self.__label_compteur.pack(side=tk.RIGHT, padx=10)

        # zone principale qui va changer selon la page
        self.__zone = tk.Frame(self)
        self.__zone.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.__page_accueil()
# efface contenue de zone principale
    def __vider_zone(self):
        """Efface le contenu de la zone principale."""
        for widget in self.__zone.winfo_children():
            widget.destroy()
        # mise a jour du compteur
        total = self.__service.compteur_transactions()
        self.__label_compteur.config(text="Total transactions : " + str(total))

#page accueil
    def __page_accueil(self):
        self.__vider_zone()

        tk.Label(self.__zone, text="Cryptomonnaies disponibles", font=("Arial", 12, "bold")).pack(pady=5)

        cadre = tk.Frame(self.__zone)
        cadre.pack(fill=tk.BOTH, expand=True)

        # en-tetes
        tk.Label(cadre, text="Nom",        width=15, relief=tk.RIDGE, bg="lightgray").grid(row=0, column=0)
        tk.Label(cadre, text="Symbole",    width=10, relief=tk.RIDGE, bg="lightgray").grid(row=0, column=1)
        tk.Label(cadre, text="Prix (USD)", width=15, relief=tk.RIDGE, bg="lightgray").grid(row=0, column=2)
        tk.Label(cadre, text="Stock",      width=15, relief=tk.RIDGE, bg="lightgray").grid(row=0, column=3)

        try:
            cryptos = self.__service.lister_cryptos()
        except Exception as erreur:
            messagebox.showerror("Erreur", str(erreur))
            return

        for i, crypto in enumerate(cryptos, start=1):
            tk.Label(cadre, text=crypto.get_nom(),                           width=15, relief=tk.RIDGE).grid(row=i, column=0)
            tk.Label(cadre, text=crypto.get_symbole(),                       width=10, relief=tk.RIDGE).grid(row=i, column=1)
            tk.Label(cadre, text=str(crypto.get_prix_unitaire()) + " USD",   width=15, relief=tk.RIDGE).grid(row=i, column=2)
            tk.Label(cadre, text=str(round(crypto.get_quantite_stock(), 2)), width=15, relief=tk.RIDGE).grid(row=i, column=3)

        tk.Button(self.__zone, text="Rafraichir", command=self.__page_accueil).pack(pady=10)

##page achat

    def __page_achat(self):
        self.__vider_zone()

        tk.Label(self.__zone, text="Acheter une cryptomonnaie", font=("Arial", 12, "bold")).pack(pady=5)

        try:
            cryptos = self.__service.lister_cryptos()
        except Exception as erreur:
            messagebox.showerror("Erreur", str(erreur))
            return

        tk.Label(self.__zone, text="Choisissez une cryptomonnaie :").pack(anchor="w")

        self.__listbox_achat = tk.Listbox(self.__zone, height=5, width=55)
        self.__listbox_achat.pack(pady=5)

        for crypto in cryptos:
            self.__listbox_achat.insert(
                tk.END,
                crypto.get_symbole() + " - " + crypto.get_nom() +
                " | Prix : " + str(crypto.get_prix_unitaire()) + " USD" +
                " | Stock : " + str(round(crypto.get_quantite_stock(), 2))
            )
        self.__listbox_achat.select_set(0)

        tk.Label(self.__zone, text="Quantite a acheter :").pack(anchor="w")
        self.__saisie_achat = tk.Entry(self.__zone, width=20)
        self.__saisie_achat.pack(anchor="w", pady=3)

        self.__label_resultat_achat = tk.Label(self.__zone, text="", fg="green", wraplength=600)
        self.__label_resultat_achat.pack(pady=5)

        self.__cryptos_achat = cryptos

        tk.Button(self.__zone, text="Acheter", command=self.__executer_achat).pack(pady=5)
#recupere les valeurs saisies et apelle le service pour achat
    def __executer_achat(self):
        index = self.__listbox_achat.curselection()
        if not index:
            messagebox.showwarning("Attention", "Selectionnez une cryptomonnaie.")
            return

        crypto_choisie = self.__cryptos_achat[index[0]]

        try:
            quantite = float(self.__saisie_achat.get().strip().replace(",", "."))
            if quantite <= 0:
                raise ValueError()
        except ValueError:
            self.__label_resultat_achat.config(text="Quantite invalide. Entrez un nombre positif.", fg="red")
            return

        try:
            resultat = self.__service.acheter(crypto_choisie.get_id_crypto(), quantite)
        except ValueError as erreur:
            self.__label_resultat_achat.config(text=str(erreur), fg="red")
            return

        msg = ("Achat confirme !\n"
               + str(resultat["quantite"]) + " " + resultat["crypto"]
               + " = " + str(round(resultat["montant_usd"], 2)) + " USD\n"
               + "Stock restant : " + str(round(resultat["stock_restant"], 2)))

        if resultat["restock_effectue"] is not None:
            msg = msg + "\nRestock automatique : +" + str(resultat["restock_effectue"]["quantite_ajoutee"]) + " unites"

        self.__label_resultat_achat.config(text=msg, fg="green")
        self.__saisie_achat.delete(0, tk.END)
        self.__page_achat()

#page
    def __page_vente(self):
        self.__vider_zone()

        tk.Label(self.__zone, text="Vendre une cryptomonnaie", font=("Arial", 12, "bold")).pack(pady=5)

        try:
            cryptos = self.__service.lister_cryptos()
        except Exception as erreur:
            messagebox.showerror("Erreur", str(erreur))
            return

        tk.Label(self.__zone, text="Choisissez une cryptomonnaie :").pack(anchor="w")

        self.__listbox_vente = tk.Listbox(self.__zone, height=5, width=55)
        self.__listbox_vente.pack(pady=5)

        for crypto in cryptos:
            self.__listbox_vente.insert(
                tk.END,
                crypto.get_symbole() + " - " + crypto.get_nom() +
                " | Prix : " + str(crypto.get_prix_unitaire()) + " USD" +
                " | Stock : " + str(round(crypto.get_quantite_stock(), 2))
            )
        self.__listbox_vente.select_set(0)

        tk.Label(self.__zone, text="Quantite a vendre :").pack(anchor="w")
        self.__saisie_vente = tk.Entry(self.__zone, width=20)
        self.__saisie_vente.pack(anchor="w", pady=3)

        self.__label_resultat_vente = tk.Label(self.__zone, text="", fg="green", wraplength=600)
        self.__label_resultat_vente.pack(pady=5)

        self.__cryptos_vente = cryptos

        tk.Button(self.__zone, text="Vendre", command=self.__executer_vente).pack(pady=5)

    def __executer_vente(self):
        """Recupere les valeurs saisies et appelle le service pour vendre."""
        index = self.__listbox_vente.curselection()
        if not index:
            messagebox.showwarning("Attention", "Selectionnez une cryptomonnaie.")
            return

        crypto_choisie = self.__cryptos_vente[index[0]]

        try:
            quantite = float(self.__saisie_vente.get().strip().replace(",", "."))
            if quantite <= 0:
                raise ValueError()
        except ValueError:
            self.__label_resultat_vente.config(text="Quantite invalide. Entrez un nombre positif.", fg="red")
            return

        try:
            resultat = self.__service.vendre(crypto_choisie.get_id_crypto(), quantite)
        except ValueError as erreur:
            self.__label_resultat_vente.config(text=str(erreur), fg="red")
            return

        msg = ("Vente confirmee !\n"
               + str(resultat["quantite"]) + " " + resultat["crypto"]
               + " = " + str(round(resultat["montant_usd"], 2)) + " USD\n"
               + "Stock restant : " + str(round(resultat["stock_restant"], 2)))

        self.__label_resultat_vente.config(text=msg, fg="green")
        self.__saisie_vente.delete(0, tk.END)
        self.__page_vente()

## PAGE HISTORIQUE

    def __page_historique(self):
        self.__vider_zone()

        tk.Label(self.__zone, text="Historique des transactions", font=("Arial", 12, "bold")).pack(pady=5)

        cadre = tk.Frame(self.__zone)
        cadre.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(cadre)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(cadre, width=80, height=15, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        try:
            transactions = self.__service.historique_transactions()
            cryptos = self.__service.lister_cryptos()

            # dictionnaire pour retrouver le symbole depuis l'id
            dico_cryptos = {}
            for c in cryptos:
                dico_cryptos[c.get_id_crypto()] = c.get_symbole()

            if not transactions:
                listbox.insert(tk.END, "Aucune transaction enregistree.")
            else:
                for tx in transactions:
                    if tx.get_type_action() == "ACHAT_USER":
                        type_lbl = "ACHAT"
                    else:
                        type_lbl = "VENTE"

                    symbole = dico_cryptos.get(tx.get_id_crypto(), "?")

                    ligne = (tx.get_date_heure() + "  |  " + type_lbl +
                             "  |  " + symbole +
                             "  |  Qte : " + str(round(tx.get_quantite_echangee(), 4)) +
                             "  |  " + str(round(tx.get_montant_total_usd(), 2)) + " USD")
                    listbox.insert(tk.END, ligne)

        except Exception as erreur:
            messagebox.showerror("Erreur", str(erreur))
# PAGE STOCKS


    def __page_stocks(self):
        self.__vider_zone()

        tk.Label(self.__zone, text="Stocks disponibles", font=("Arial", 12, "bold")).pack(pady=5)

        try:
            cryptos = self.__service.lister_cryptos()
        except Exception as erreur:
            messagebox.showerror("Erreur", str(erreur))
            return

        cadre = tk.Frame(self.__zone)
        cadre.pack()

        # en-tetes
        tk.Label(cadre, text="Crypto",   width=15, relief=tk.RIDGE, bg="lightgray").grid(row=0, column=0, padx=2, pady=2)
        tk.Label(cadre, text="Symbole",  width=10, relief=tk.RIDGE, bg="lightgray").grid(row=0, column=1, padx=2, pady=2)
        tk.Label(cadre, text="Stock",    width=15, relief=tk.RIDGE, bg="lightgray").grid(row=0, column=2, padx=2, pady=2)
        tk.Label(cadre, text="Etat",     width=20, relief=tk.RIDGE, bg="lightgray").grid(row=0, column=3, padx=2, pady=2)

        for i, crypto in enumerate(cryptos, start=1):
            stock = crypto.get_quantite_stock()

            # indication de l'etat du stock
            if stock <= 400:
                etat = "Bas - restock bientot"
                couleur = "orange"
            else:
                etat = "Normal"
                couleur = "black"

            tk.Label(cadre, text=crypto.get_nom(),    width=15, relief=tk.RIDGE).grid(row=i, column=0, padx=2, pady=2)
            tk.Label(cadre, text=crypto.get_symbole(),width=10, relief=tk.RIDGE).grid(row=i, column=1, padx=2, pady=2)
            tk.Label(cadre, text=str(round(stock, 2)),width=15, relief=tk.RIDGE).grid(row=i, column=2, padx=2, pady=2)
            tk.Label(cadre, text=etat, fg=couleur,    width=20, relief=tk.RIDGE).grid(row=i, column=3, padx=2, pady=2)

        tk.Button(self.__zone, text="Rafraichir", command=self.__page_stocks).pack(pady=10)
