# Classe FILLE représentant le Hedera symbole HBAR
# Hérite de Cryptomonnaie (classe mère)

from cryptomonnaie import Cryptomonnaie, STOCK_INITIAL

#classe fille hbar de la classse mere cryptomonnaie
class Hbar(Cryptomonnaie):

# Variables de classe : propres au HBAR
    NOM         = "Hedera"
    SYMBOLE     = "HBAR"
    PRIX_DEFAUT = 0.35

#appel au constructuer de la classe mere via super et ajout valeur propre du HBAR
    def __init__(self, id_crypto, quantite_stock=STOCK_INITIAL, prix_unitaire=PRIX_DEFAUT):
        super().__init__(id_crypto, self.NOM, self.SYMBOLE, prix_unitaire, quantite_stock)

    # surcharge de la methode afficher de la classe mere grace au type de technologie du Hedera
# le hashgraph est une technologie différente de la blokchain et compliquée à comprendre mais en gros Les nœuds partagent leurs historiques entre eux comme des rumeurs qui se propagent (gossip protocol), jusqu'à ce que tout le réseau soit d'accord
    def afficher(self):
        return ("Hedera (HBAR)"
                + " | Prix : " + str(self.get_prix_unitaire()) + " USD"
                + " | Stock : " + str(self.get_quantite_stock())
                + " | Type : Hashgraph")
