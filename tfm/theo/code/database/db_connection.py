"""
Connexion à la base de données SQLite, Pattern Singleton.
Garantit qu'une seule instance de connexion existe dans toute l'application.
"""
import sqlite3


class DatabaseConnection:
    """
    Pattern Singleton

    Utilisation :
        db = DatabaseConnection()
        conn = db.get_connection()
    """

    _instance = None       # Référence unique vers l'instance
    _connection = None     # Connexion SQLite partagée

    def __new__(cls):
        """
        Si l'instance existe déjà, on la retourne sans en créer une nouvelle.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # La connexion est créée une seule fois ici
            cls._connection = sqlite3.connect("vuln_tracker.db", check_same_thread=False)
            cls._connection.row_factory = sqlite3.Row  # Résultats accessibles par nom de colonne
            cls._connection.execute("PRAGMA foreign_keys = ON")  # Activation des clés étrangères
        return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        """Retourne la connexion active à la base de données."""
        return self._connection

    def get_cursor(self) -> sqlite3.Cursor:
        """Retourne un curseur pour exécuter des requêtes."""
        return self._connection.cursor()

    def commit(self):
        """Valide les transactions en attente."""
        self._connection.commit()

    def close(self):
        """Ferme proprement la connexion (fermeture de l'app)."""
        if self._connection:
            self._connection.close()
            DatabaseConnection._instance = None
            DatabaseConnection._connection = None
