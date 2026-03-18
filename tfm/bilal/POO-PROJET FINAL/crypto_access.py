
# Classe d'accès  table "cryptomonnaie".
# Quand elle lit une ligne de la base de données, elle crée le bon objet

from database import DBConnection
from bitcoin import Bitcoin
from ethereum import Ethereum
from xrp import XRP
from solana import Solana
from hbar import Hbar


# polymorphisme = dico qui associe un symbole à sa classe fille correspondante

CLASSES_PAR_SYMBOLE = {
    "BTC":  Bitcoin,
    "ETH":  Ethereum,
    "XRP":  XRP,
    "SOL":  Solana,
    "HBAR": Hbar,
}

# grace a cette classe je peux lire et modif  les crypto de ma DB
class CryptoAccess:
    def __init__(self):
        # On récupère la connexion unique via Singleton
        self._db = DBConnection.get_instance().get_connection()
#ici on retourne toutes les crytpos sous formes d'objet Bictoin, Ethereum, XRP etc
    def get_all(self):
        cur = self._db.cursor()
        cur.execute("SELECT * FROM cryptomonnaie ORDER BY nom")
        rows = cur.fetchall()
        cur.close()

        liste = []
        for row in rows:
            liste.append(self._ligne_vers_crypto(row))
        return liste
#ici ça permet de retourner une crypto avec son id crypto
    def get_by_id(self, id_crypto):
        cur = self._db.cursor()
        cur.execute("SELECT * FROM cryptomonnaie WHERE id_crypto = ?", (id_crypto,))
        row = cur.fetchone()
        cur.close()

        if row is None:
            return None
        return self._ligne_vers_crypto(row)
# ici je peux retourner une crypto rien qu'avec son symbole ex BTX pour bitcoin
    def get_by_symbole(self, symbole):
        cur = self._db.cursor()
        cur.execute("SELECT * FROM cryptomonnaie WHERE symbole = ?", (symbole.upper(),))
        row = cur.fetchone()
        cur.close()

        if row is None:
            return None
        return self._ligne_vers_crypto(row)
#moise à jour du stock d'une crypto dans la DB

    def update_stock(self, id_crypto, nouveau_stock):
        cur = self._db.cursor()
        cur.execute(
            "UPDATE cryptomonnaie SET quantite_stock = ? WHERE id_crypto = ?",
            (nouveau_stock, id_crypto)
        )
        self._db.commit()
        cur.close()
# ICI un exemple pour expliquer = si dans une ligne de la DB y a symbole btc, le prog comprent qu'il doit créer un objet BITCOIN( polymorphisme)
    def _ligne_vers_crypto(self, row):
        symbole = row["symbole"]

#ici permet de cherche la classe fille correspondant au symbole
        classe = CLASSES_PAR_SYMBOLE.get(symbole)

        if classe is not None:
# On crée un objet de la classe fille (Bitcoin, Ethereum,etc.)
            return classe(
                id_crypto=row["id_crypto"],
                quantite_stock=float(row["quantite_stock"]),
                prix_unitaire=float(row["prix_unitaire_usd"])
            )
        else:
            # Symbole inconnu : raise  une erreur
            raise ValueError("Symbole inconnu en base de données : " + symbole)
