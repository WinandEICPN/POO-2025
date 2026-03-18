# Classe d'accès aux données de la table "transaction_crypto".
# Elle contient uniquement des opérations SQL (pas de logique métier).

from datetime import datetime
from database import DBConnection
from transaction import Transaction

#Permet d'enregistrer et de lire les transactions dans la base de données

class TransactionAccess:

    def __init__(self):
        # On récupère la connexion unique via le Singleton
        self._db = DBConnection.get_instance().get_connection()

    #Insère une nouvelle transaction dans la base et retourne son id
    def enregistrer(self, type_action, quantite, montant, id_crypto):
        date_maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur = self._db.cursor()
        cur.execute(
            "INSERT INTO transaction_crypto (type_action, quantite_echangee, montant_total_usd, date_heure, id_crypto) VALUES (?, ?, ?, ?, ?)",
            (type_action, quantite, montant, date_maintenant, id_crypto)
        )
        self._db.commit()
        id_genere = cur.lastrowid
        cur.close()
        return id_genere
# retourne toutes les transactions de la plus recente à l'ancienne
    def get_all(self):
        cur = self._db.cursor()
        cur.execute("SELECT * FROM transaction_crypto ORDER BY date_heure DESC")
        rows = cur.fetchall()
        cur.close()

        liste = []
        for row in rows:
            liste.append(self._ligne_vers_transaction(row))
        return liste
# return les transactions pour une crypto donnée
    def get_by_crypto(self, id_crypto):
        cur = self._db.cursor()
        cur.execute(
            "SELECT * FROM transaction_crypto WHERE id_crypto = ? ORDER BY date_heure DESC",
            (id_crypto,)
        )
        rows = cur.fetchall()
        cur.close()

        liste = []
        for row in rows:
            liste.append(self._ligne_vers_transaction(row))
        return liste
# return le nombre total de transactions enregistrées
    def compter_total(self):
        cur = self._db.cursor()
        cur.execute("SELECT COUNT(*) AS total FROM transaction_crypto")
        row = cur.fetchone()
        cur.close()

        if row is None:
            return 0
        return row["total"]
#converti une ligne de la db en objet transaction
    def _ligne_vers_transaction(self, row):
        return Transaction(
            id_transaction=row["id_transaction"],
            type_action=row["type_action"],
            quantite_echangee=float(row["quantite_echangee"]),
            montant_total_usd=float(row["montant_total_usd"]),
            id_crypto=row["id_crypto"],
            date_heure=row["date_heure"]
        )
