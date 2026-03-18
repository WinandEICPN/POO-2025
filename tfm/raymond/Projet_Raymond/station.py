# Import des différentes classes de pompes
# Chaque classe représente un type spécifique de carburant
from pompe import PompeEssence95, PompeEssence98, PompeDiesel

# Import de la classe Database
# Cette classe gère toutes les interactions avec la base de données SQLite
from database import Database


# Classe Station
# Cette classe représente la station-service dans son ensemble.
# Elle gère :
# - les pompes disponibles.
# - les ventes de carburant.
# - la communication avec la base de données.
class Station:

    # Constructeur de la classe Station
    def __init__(self):

        # Création de l'objet Database (Singleton)
        # Permet d'accéder à la base de données de manière centralisée
        self.db = Database()

        # Liste qui va contenir toutes les pompes de la station
        self.pompes = []

        # Appel d'une méthode privée pour créer les pompes
        self._creer_pompes()

    # Méthode privée servant à initialiser les pompes de la station
    # Le "_" indique que cette méthode ne doit être utilisée qu'en interne
    def _creer_pompes(self):

        # Ajout d'une pompe Essence 95 avec 500 litres en stock
        self.pompes.append(PompeEssence95(500))

        # Ajout d'une pompe Essence 98 avec 400 litres en stock
        self.pompes.append(PompeEssence98(400))

        # Ajout d'une pompe Diesel avec 600 litres en stock
        self.pompes.append(PompeDiesel(600))

    # Méthode permettant de trouver une pompe selon le type de carburant
    def trouver_pompe(self, type_carburant):

        # Parcours de toutes les pompes de la station
        for pompe in self.pompes:

            # Vérification si la pompe correspond au carburant demandé
            if pompe._type_carburant == type_carburant:

                # Si trouvée, on retourne l'objet pompe
                return pompe

        # Si aucune pompe ne correspond, on retourne None
        return None

# Méthode principale permettant d'effectuer une vente de carburant
    def vendre(self, type_carburant, litres):

        # Validation des données utilisateur
        # On vérifie que la quantité demandée est valide
        if litres <= 0:
            return "Quantité invalide"

        # Recherche de la pompe correspondant au carburant demandé
        pompe = self.trouver_pompe(type_carburant)

        # Si aucune pompe n'est trouvée
        if pompe is None:
            return "Carburant introuvable"

        # Appel de la méthode distribuer de la pompe
        # Cette méthode va vérifier le stock et calculer le montant
        montant = pompe.distribuer(litres)

        # Si la pompe retourne -1, cela signifie que le stock est insuffisant
        if montant == -1:
            return "Stock insuffisant"

        # Enregistrement de la vente dans la base de données
        self.db.ajouter_vente(type_carburant, litres, montant)

        # Mise à jour du stock dans la base de données
        # On récupère le nouveau stock depuis la pompe
        self.db.update_stock(type_carburant, pompe.get_stock())

        # Message de confirmation envoyé à l'interface utilisateur
        return f"Vente réussie : {montant} €"
