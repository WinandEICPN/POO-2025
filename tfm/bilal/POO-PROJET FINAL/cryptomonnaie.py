from entite_base import EntiteBase

# Constantes valables pour classes mere et filles
STOCK_INITIAL = 1000
SEUIL_RECHARGE = 400  # Si le stock tombe à ce niveau, on recharge
QUANTITE_RECHARGE = 600  # Quantité ajoutée lors du restock (pour revenir à 1000)
STOCK_MAX_RACHAT = 1500  # On ne rachète plus si le stock dépasse ce seuil


# on a ici la classe mere qui hérite d'une classe abstraire donc la classe EntiteBase
# les classes xrp hbar btc etc vont hériter de cette classe mere

class Cryptomonnaie(EntiteBase):

    # comme demandé les attribus sont en privés niveau encapsulation
    def __init__(self, id_crypto, nom, symbole, prix_unitaire, quantite_stock=STOCK_INITIAL):
        # Attributs privés (double underscore = inaccessibles depuis l'extérieur)
        self.__id_crypto = id_crypto
        self.__nom = nom
        self.__symbole = symbole
        self.__prix_unitaire = prix_unitaire
        self.__quantite_stock = quantite_stock

    # les getters vu qu'on a des attributs privés pour pouvoir les utiliser faut getter

    def get_id_crypto(self):
        return self.__id_crypto

    def get_nom(self):
        return self.__nom

    def get_symbole(self):
        return self.__symbole

    def get_prix_unitaire(self):
        return self.__prix_unitaire

    def get_quantite_stock(self):
        return self.__quantite_stock

    # tous mes setters en mode java

    # verification prix positif
    def set_prix_unitaire(self, nouveau_prix):
        if nouveau_prix <= 0:
            raise ValueError("Le prix doit être positif.")
        self.__prix_unitaire = nouveau_prix

    # --- Méthodes métier communes à toutes les cryptos ---
    # je dois voir avec ça si j'ai encore assez de crypto a vendre donc que mon stock est plus grand que la quantité à vendre au client
    def peut_vendre_a_user(self, quantite):
        return self.__quantite_stock >= quantite

    # permet de réponse si on peut encore racheter avec stocl + cryto a acheter du client <= 1500
    def peut_racheter_a_user(self, quantite):
        return (self.__quantite_stock + quantite) <= STOCK_MAX_RACHAT

    # donne combiene on peut encore racheter aux clients
    def quantite_rachetable(self):

        restant = STOCK_MAX_RACHAT - self.__quantite_stock
        if restant < 0:
            return 0
        return restant

    # enleve quantite du stock quand on vend crypto au client

    def debiter_stock(self, quantite):
        if quantite <= 0:
            raise ValueError("quantité doit être postive.")
        if quantite > self.__quantite_stock:
            raise ValueError("Stock insuffisant.")
        self.__quantite_stock -= quantite

    # ajoute au stock quand ya rachat ou restock auto
    def crediter_stock(self, quantite):
        if quantite <= 0:
            raise ValueError("La quantité doit être positive.")
        self.__quantite_stock += quantite

    # donne true si on deoit recharger
    def necessite_recharge(self):

        return self.__quantite_stock <= SEUIL_RECHARGE

    # Méthodes abstraites imposées par EntiteBase
    # classe filles peuvent override si besoin

    def valider(self):
        if not self.__nom:
            return False
        if not self.__symbole:
            return False
        if self.__prix_unitaire <= 0:
            return False
        if self.__quantite_stock < 0:
            return False
        return True

    def afficher(self):
        return (self.__nom + " (" + self.__symbole + ")"
                + " | Prix : " + str(self.__prix_unitaire) + " USD"
                + " | Stock : " + str(self.__quantite_stock))

    def to_dict(self):
        return {
            "id_crypto": self.__id_crypto,
            "nom": self.__nom,
            "symbole": self.__symbole,
            "prix_unitaire_usd": self.__prix_unitaire,
            "quantite_stock": self.__quantite_stock
        }

    # prinbt la chaine de caractere
    def __str__(self):
        return self.afficher()