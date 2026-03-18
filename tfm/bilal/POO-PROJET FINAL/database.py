
# Classe Singleton qui gère la connexion unique à la base de données SQLite.
# Pattern Singleton : 1 seule instance est créée et partagée dans tout le prog
# On accède à la connexion via : DBConnection.get_instance().get_connection()

import sqlite3


class DBConnection:

    _instance = None   # Variable de classe : stocke l'unique instance
    _init_done = False # Empêche de réinitialiser la connexion à chaque appel

    def __init__(self, db_path="crypto.db"):
        # initialise  connexion une seule fois grâce au _init_done
        if not DBConnection._init_done:
            self._connection = sqlite3.connect(db_path, check_same_thread=False)
            # row_factory permet d'accéder aux colonnes par leur nom (ex: row["nom"])
            self._connection.row_factory = sqlite3.Row
            # Active la vérification des clés étrangères
            self._connection.execute("PRAGMA foreign_keys = ON")
            DBConnection._init_done = True
            print("Connexion à la base de données ouverte.")
#methoeds de la classe database
# dans la methode get instance on retourne l'instance unique de DBCONNECTION et si existe pas elle est créee
    @classmethod
    def get_instance(cls, db_path="crypto.db"):
        if cls._instance is None:
            cls._instance = DBConnection(db_path)
        return cls._instance
#retourne l'object connetion SQLITE
    def get_connection(self):
        return self._connection
