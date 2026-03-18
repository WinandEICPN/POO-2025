# init_db.py
# Crée les tables de la DB et insère les 5 cryptomonnaies de départ.
# On utilise directement les classes filles pour récupérer le nom  symbole et prix.

from database import DBConnection
from bitcoin import Bitcoin
from ethereum import Ethereum
from xrp import XRP
from solana import Solana
from hbar import Hbar

#intialise et crée table et insere données de départ si les données n'existent pas
def initialiser_base():

    db = DBConnection.get_instance().get_connection()
    cur = db.cursor()

# Création table des cryptomonnaies
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cryptomonnaie (
            id_crypto         INTEGER PRIMARY KEY,
            nom               TEXT    NOT NULL UNIQUE,
            symbole           TEXT    NOT NULL UNIQUE,
            prix_unitaire_usd REAL    NOT NULL,
            quantite_stock    REAL    NOT NULL DEFAULT 1000
        )
    """)

# Création de la table transactions (achat et vente)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transaction_crypto (
            id_transaction    INTEGER PRIMARY KEY,
            type_action       TEXT    NOT NULL,
            quantite_echangee REAL    NOT NULL,
            montant_total_usd REAL    NOT NULL,
            date_heure        TEXT    NOT NULL,
            id_crypto         INTEGER NOT NULL,
            FOREIGN KEY (id_crypto) REFERENCES cryptomonnaie(id_crypto)
        )
    """)

# Création de la table des restocks autom
    cur.execute("""
        CREATE TABLE IF NOT EXISTS restock (
            id_ravitaillement   INTEGER PRIMARY KEY,
            quantite_ajoutee    REAL NOT NULL,
            date_ravitaillement TEXT NOT NULL,
            id_crypto           INTEGER NOT NULL,
            FOREIGN KEY (id_crypto) REFERENCES cryptomonnaie(id_crypto)
        )
    """)

    db.commit()

# Liste des classes filles qui permetrécup les infos directement depuis chaque classe
    classes_cryptos = [Bitcoin, Ethereum, XRP, Solana, Hbar]

    for classe in classes_cryptos:
# vérification  si crypto existe déjà dans DB  avant de l'insérer
        cur.execute("SELECT id_crypto FROM cryptomonnaie WHERE symbole = ?", (classe.SYMBOLE,))
        existante = cur.fetchone()

        if existante is None:
            cur.execute(
                "INSERT INTO cryptomonnaie (nom, symbole, prix_unitaire_usd, quantite_stock) VALUES (?, ?, ?, 1000)",
                (classe.NOM, classe.SYMBOLE, classe.PRIX_DEFAUT)
            )
            print("Crypto ajoutée : " + classe.NOM + " (" + classe.SYMBOLE + ")")

    db.commit()
    cur.close()
    print("Base de données prête.")


if __name__ == "__main__":
    initialiser_base()
