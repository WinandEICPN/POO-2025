
# Classe FILLE de cryptomonnaie représentant l'Ethereum.

from cryptomonnaie import Cryptomonnaie, STOCK_INITIAL


class Ethereum(Cryptomonnaie):

# Variables de classe ETH Donc propre a ETH
    NOM         = "Ethereum"
    SYMBOLE     = "ETH"
    PRIX_DEFAUT = 3200.00
# LE SUPER permet d'appeler le constructeur de la classe mere avec le super et mettre les valeurs propres à l'eth
    def __init__(self, id_crypto, quantite_stock=STOCK_INITIAL, prix_unitaire=PRIX_DEFAUT):
        super().__init__(id_crypto, self.NOM, self.SYMBOLE, prix_unitaire, quantite_stock)

# on surhage la methode afficher avec le mecanisme de validation de la blockchain ETH qui est le proof of stake et donc ça permet de rajouter la specificté par rapport aux autre cryptos
# le proof of stake c'est en gros: au lieu de calculer comme pour BTC, les validateurs "misent" leurs ETH comme garantie. Plus tu mises, plus tu as de chances d'être choisi pour valider un bloc.
    def afficher(self):
        return ("Ethereum (ETH)"
                + " | Prix : " + str(self.get_prix_unitaire()) + " USD"
                + " | Stock : " + str(self.get_quantite_stock())
                + " | Type : Proof of Stake")
