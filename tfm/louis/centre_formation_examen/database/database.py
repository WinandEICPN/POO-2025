import sqlite3

class Database:
    
    #Singleton pour la connexion SQLite.
    #Garantit une seule instance pour toutes les DAO.

    """Cela permet :
    - d'éviter d'ouvrir plusieurs connexions SQLite
    - de centraliser l'accès à la base de données
    - de partager la même connexion entre tous les DAO"""
   

    
    _instance = None

    def __new__(cls, db_file="centre.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect(db_file)
            cls._instance.conn.row_factory = sqlite3.Row
        return cls._instance
    
    """La méthode __new__ est utilisée pour contrôler la création
        de l'objet. Elle permet d'empêcher la création de plusieurs
        instances de la classe Database."""

    def get_connection(self):
        return self.conn
    
        #Retourne la connexion à la base de données.
        #Cette méthode est utilisée par toutes les classes DAO.

    def close(self):
        
        #Ferme la connexion à la base et réinitialise l'instance Singleton.
        #À appeler à la fermeture de l'application.
        
        if self.conn:
            self.conn.close()
            self.conn = None
            Database._instance = None