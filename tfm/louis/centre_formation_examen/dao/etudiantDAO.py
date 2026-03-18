from database.database import Database

""" 
Import de la classe Database qui gère la connexion SQLite
Cette classe utilise le pattern Singleton pour garantir
qu'une seule connexion à la base de données existe dans l'application
"""

from models.etudiant import Etudiant

class EtudiantDAO:
    
    # DAO (data access object) pour table etudiant.
    # Elle centralise toutes les opérations SQL concernant les étudiants.
    # intermédiaire entre BD et le reste.
    
    def __init__(self):
        
        # Récupèration de la connexion à la base via le singleton.
        # Toutes les classes DAO utilisent la même connexion.
        
        self.conn = Database().get_connection()
        
        # crée la table etudiant si elle n'existe pas encore.
        # evite des erreurs si la base est vide.
        
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS etudiants (id INTEGER PRIMARY KEY, nom TEXT, email TEXT)"
        )

        # Validation de la modification dans la base.
        # (nécessaire pour les requêtes INSERT / UPDATE / DELETE). 
        
    def insert(self, etu: Etudiant):
        
        # Insertion d'un nouvel étudiant dans la base de données.
        # La requête utilise des paramètres (?) afin d'éviter les injections SQL.
        # et de sécuriser les données entrées par l'utilisateur
        
        self.conn.execute(
            "INSERT INTO etudiants (nom,email) VALUES (?,?)",
            (etu.nom, etu.email)
        )
        
        self.conn.commit()

    def get_all(self):
        
        # Récupération de tous les étudiants enregistrés dans la BD.
        
        cursor = self.conn.execute("SELECT * FROM etudiants")
        return [tuple(row) for row in cursor]

    def delete(self, etu_id):
        
        # Supprime un étudiant via son ID
        # ID qui correspond à la clé primaire de la table
        self.conn.execute("DELETE FROM etudiants WHERE id=?",(etu_id,))
        self.conn.commit()