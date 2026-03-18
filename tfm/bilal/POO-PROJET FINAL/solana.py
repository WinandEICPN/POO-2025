# Classe FILLE  Solana
# Hérite de Cryptomonnaie (classe mère)

from cryptomonnaie import Cryptomonnaie, STOCK_INITIAL


class Solana(Cryptomonnaie):

    NOM         = "Solana"
    SYMBOLE     = "SOL"
    PRIX_DEFAUT = 200.00

    def __init__(self, id_crypto, quantite_stock=STOCK_INITIAL, prix_unitaire=PRIX_DEFAUT):
        # constructeur de la classe mere est appele avec utilisation du super
        super().__init__(id_crypto, self.NOM, self.SYMBOLE, prix_unitaire, quantite_stock)

    # surchage de la methode  de afficher() pour avoir description spécifique au Solana
    # proof of history technologie propre au SOL
    # consiste en  sorte d'horloge cryptographique intégrée dans la blockchain. Chaque transaction a une "preuve du moment" où elle s'est produite, ce qui permet de traiter des milliers de transactions par seconde
    def afficher(self):
        return ("Solana (SOL)"
                + " | Prix : " + str(self.get_prix_unitaire()) + " USD"
                + " | Stock : " + str(self.get_quantite_stock())
                + " | Type : Proof of History")
