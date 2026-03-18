# Classe Vente
# Cette classe représente une vente de carburant réalisée dans la station.
# Elle permet de stocker les informations principales d'une transaction.

class Vente:

    # Constructeur de la classe Vente
    # Cette méthode est appelée lorsqu'un nouvel objet Vente est créé
    def __init__(self, type_carburant, litres, montant):
        # Type de carburant vendu (Essence 95, Essence 98, Diesel)
        self.type_carburant = type_carburant

        # Quantité de carburant vendue en litres
        self.litres = litres

        # Montant total de la vente en euros
        self.montant = montant
