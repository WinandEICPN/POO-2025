# restock_access.py
# Classe d'accès aux données de la table "restock".
# Elle contient uniquement des op SQL

from datetime import datetime
from database import DBConnection
from restock import Restock

# classe qui premet de save et lire les restocks de la db
class RestockAccess:
    """Permet d'enregistrer et de lire les restocks dans la base de données."""

    def __init__(self):
        # On récupère la connexion unique via le Singleton
        self._db = DBConnection.get_instance().get_connection()

    def enregistrer(self, quantite, id_crypto):
# Insère un restock automatique dans la base et retourne son id
        date_maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur = self._db.cursor()
        cur.execute(
            "INSERT INTO restock (quantite_ajoutee, date_ravitaillement, id_crypto) VALUES (?, ?, ?)",
            (quantite, date_maintenant, id_crypto)
        )
        self._db.commit()
        id_genere = cur.lastrowid
        cur.close()
        return id_genere

#historique des restocks par crypto
    def get_by_crypto(self, id_crypto):
        cur = self._db.cursor()
        cur.execute(
            "SELECT * FROM restock WHERE id_crypto = ? ORDER BY date_ravitaillement DESC",
            (id_crypto,)
        )
        rows = cur.fetchall()
        cur.close()

        liste = []
        for row in rows:
            liste.append(self._ligne_vers_restock(row))
        return liste
#converti une ligne de la db en objet restock
    def _ligne_vers_restock(self, row):
        return Restock(
            id_ravitaillement=row["id_ravitaillement"],
            quantite_ajoutee=float(row["quantite_ajoutee"]),
            id_crypto=row["id_crypto"],
            date_ravitaillement=row["date_ravitaillement"]
        )
