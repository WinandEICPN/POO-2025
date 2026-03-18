# Import du module abc (Abstract Base Classes)
# Ce module permet de créer des classes abstraites en Python
from abc import ABC, abstractmethod

# Classe abstraite Pompe.
# Elle sert de modèle pour les classes filles (Essence95, Essence98, Diesel)
class Pompe(ABC):
# Constructeur de la classe
    def __init__(self, type_carburant, prix_litre, stock):
        # L'attribut est protégé (underscore) pour respecter l'encapsulation
        self._type_carburant = type_carburant
        self._prix_litre = prix_litre
        self._stock = stock

# Méthode abstraite
# Toute classe fille doit obligatoirement implémenter cette méthode
    @abstractmethod
    def distribuer(self, litres):
        pass

# Méthode permettant de récupérer le stock restant
    def get_stock(self):
        return self._stock

# Méthode permettant de récupérer le prix du litre
    def get_prix(self):
        return self._prix_litre

# Classe représentant une pompe d'essence 95.
# Elle hérite de la classe abstraite Pompe
class PompeEssence95(Pompe):
    # Constructeur spécifique à la pompe Essence 95
    def __init__(self, stock):
        # Appel du constructeur de la classe parent (Pompe)
        # On fixe automatiquement le type et le prix du carburant
        super().__init__("Essence 95", 1.80, stock)

 # Implémentation de la méthode abstraite distribuer()
    def distribuer(self, litres):

        # Validation : quantité invalide
        # Si l'utilisateur demande 0 litre ou une valeur négative
        if litres <= 0:
            return -1

        # Vérification que le stock est suffisant
        if litres <= self._stock:

            # Mise à jour du stock après distribution
            self._stock -= litres

            # Calcul du montant de la vente
            return litres * self._prix_litre
        else:
            # Si le stock est insuffisant
            return -1

# Classe représentant une pompe d'essence 98.
# Elle hérite également de la classe Pompe
class PompeEssence98(Pompe):
    def __init__(self, stock):
        # Initialisation avec le type et prix de l'Essence 98
        super().__init__("Essence 98", 1.95, stock)

    # Implémentation de la méthode abstraite distribuer()
    def distribuer(self, litres):

        # Validation : quantité invalide
        if litres <= 0:
            return -1

        # Vérification du stock disponible
        if litres <= self._stock:
            # Mise à jour du stock
            self._stock -= litres
            # Calcul du prix total
            return litres * self._prix_litre
        else:
            return -1

# Classe représentant une pompe Diesel
# Elle hérite également de la classe abstraite Pompe
class PompeDiesel(Pompe):
    def __init__(self, stock):
        # Initialisation avec les informations du Diesel
        super().__init__("Diesel", 1.70, stock)

    def distribuer(self, litres):

        # Validation : quantité invalide
        if litres <= 0:
            return -1

        # Vérification du stock disponible
        if litres <= self._stock:

            # Mise à jour du stock après vente.
            self._stock -= litres

            # Calcul du montant total
            return litres * self._prix_litre
        else:
            return -1
