# Import de la bibliothèque sqlite3
# Cette bibliothèque permet de créer et manipuler une base de données SQLite

import sqlite3

# Cette classe gère toute la communication avec la base de données.
# Elle utilise le design pattern Singleton pour garantir qu'une seule connexion
# à la base de données existe dans toute l'application.

class Database:
    _instance = None     # Variable de classe qui stocke l'unique instance de Database

# Méthode spéciale appelée lors de la création d'un objet.
# Elle est redéfinie ici pour implémenter le pattern Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect("station.db")
            cls._instance.cursor = cls._instance.conn.cursor()
            cls._instance.creer_tables()
        return cls._instance

# Méthode qui crée les tables nécessaires dans la base de données
# Cette méthode est appelée automatiquement lors de la première création de Database

    def creer_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pompes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_carburant TEXT UNIQUE,
            prix_litre REAL,
            stock REAL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_carburant TEXT,
            litres REAL,
            montant REAL,
            FOREIGN KEY(type_carburant) REFERENCES pompes(type_carburant)
        )
        """)
# Sauvegarde des modifications dans la base de données
        self.conn.commit()

# Méthode permettant d'ajouter une nouvelle vente dans la base de données
    def ajouter_vente(self, type_carburant, litres, montant):
        self.cursor.execute(
            "INSERT INTO ventes (type_carburant, litres, montant) VALUES (?, ?, ?)",
            (type_carburant, litres, montant)
        )
        self.conn.commit()

# Méthode qui récupère toutes les ventes enregistrées
    def get_ventes(self):
        self.cursor.execute("SELECT * FROM ventes")
        return self.cursor.fetchall()               # fetchall() retourne toutes les lignes sous forme de liste

# Méthode permettant de mettre à jour le stock d'une pompe
    def update_stock(self, type_carburant, nouveau_stock):
        self.cursor.execute(
            "UPDATE pompes SET stock = ? WHERE type_carburant = ?",
            (nouveau_stock, type_carburant)
        )
        self.conn.commit()         # Sauvegarde des modifications

# Méthode permettant de supprimer une vente spécifique.
# Elle utilise l'identifiant unique de la vente
    def supprimer_vente(self, id_vente):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM ventes WHERE id=?",
            (id_vente,)
        )
        self.conn.commit()        # Sauvegarde des modifications

# Méthode permettant de supprimer toutes les ventes de la base de données
# Cette méthode peut être utile pour réinitialiser l'historique des ventes
    def supprimer_ventes(self):
        self.cursor.execute("DELETE FROM ventes")
        self.conn.commit()
