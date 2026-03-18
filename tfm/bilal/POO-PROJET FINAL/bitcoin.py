# bitcoin.py
# Classe FILLE représentant le Bitcoin.
# Hérite de Cryptomonnaie (classe mère).
# Le nom, le symbole et le prix par défaut sont fixés ici.

from cryptomonnaie import Cryptomonnaie, STOCK_INITIAL


class Bitcoin(Cryptomonnaie):
    """Représente le Bitcoin (BTC)."""

    # Variables de classe : propres au Bitcoin
    NOM         = "Bitcoin"
    SYMBOLE     = "BTC"
    PRIX_DEFAUT = 94000.00

    def __init__(self, id_crypto, quantite_stock=STOCK_INITIAL, prix_unitaire=PRIX_DEFAUT):
        # On appelle le constructeur de la classe mère avec les valeurs propres au Bitcoin
        super().__init__(id_crypto, self.NOM, self.SYMBOLE, prix_unitaire, quantite_stock)

# surcharge de la methode afficher() : description spécifique au Bitcoin
#surchage ici consiste à ajouter pour chaque utilisé par chaque blockchain pour confirmer les transactions et créer de nouveaux blocs.
# pour BTC ce mecanisme de la blockchain c'est le proof of work: mineur doivent resoudre des problems mathematiques complexe et celui qui trouve valide le bloc et recoit des btc en recompense
#donc BITCOIN herite de chaque attribu et methode de classe mere cryptomonnaie (heritage) et la surchage consiste à rajouter pour chaque crypto qui correspond à sa technologie de validation des transactions (mecanisme de la blockchain propre à chaque crypto)
    def afficher(self):
        return ("Bitcoin (BTC)"
                + " | Prix : " + str(self.get_prix_unitaire()) + " USD"
                + " | Stock : " + str(self.get_quantite_stock())
                + " | Type : Proof of Work")
