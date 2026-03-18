
# Classe FILLE représentant le XRP (Ripple), ma crypto préférée :)
# Hérite de Cryptomonnaie - classe mère

from cryptomonnaie import Cryptomonnaie, STOCK_INITIAL


class XRP(Cryptomonnaie):
    NOM         = "XRP"
    SYMBOLE     = "XRP"
    PRIX_DEFAUT = 2.50

    def __init__(self, id_crypto, quantite_stock=STOCK_INITIAL, prix_unitaire=PRIX_DEFAUT):
# appelle constructeur de la classe mère  avec super et avec les valeurs propres au XRP
        super().__init__(id_crypto, self.NOM, self.SYMBOLE, prix_unitaire, quantite_stock)

    # surchage methode afficher() : description spécifique au XRP avec technologie propre à xrp
    # consensus ledger: ici pas de mineurs ni de validateurs classiques. Un réseau de nœuds de confiance (choisis par la société Ripple) se mettent d'accord rapidement sur les transactions.
    def afficher(self):
        return ("XRP (XRP)"
                + " | Prix : " + str(self.get_prix_unitaire()) + " USD"
                + " | Stock : " + str(self.get_quantite_stock())
                + " | Type : Consensus Ledger")