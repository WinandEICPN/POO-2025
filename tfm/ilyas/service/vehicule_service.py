from database.connection import DatabaseConnection
from models.voiture import Voiture
from models.utilitaire import Utilitaire


class VehiculeService:

    def __init__(self):
        self.db = DatabaseConnection()
        self.cursor = self.db.get_cursor()
        self.liste_vehicules = []
        self.charger_vehicules()

    def charger_vehicules(self):
        """Charge les véhicules depuis la base de données en mémoire."""
        self.cursor.execute(
            "SELECT id, marque, modele, immatriculation, prix_par_jour, type FROM vehicules"
        )
        rows = self.cursor.fetchall()
        self.liste_vehicules = []
        for vid, marque, modele, immat, prix, type_vehicule in rows:
            if type_vehicule == "Voiture":
                v = Voiture(vid, marque, modele, immat, prix, nombre_portes=4)
            elif type_vehicule == "Utilitaire":
                v = Utilitaire(vid, marque, modele, immat, prix, volume_charge=0)
            else:
                # Default to Voiture if type is unknown
                v = Voiture(vid, marque, modele, immat, prix, nombre_portes=4)
            self.liste_vehicules.append(v)

    def ajouter_vehicule(self, vehicule):
        type_vehicule = vehicule.__class__.__name__

        self.cursor.execute("""
            INSERT INTO vehicules (id, marque, modele, immatriculation, prix_par_jour, type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            vehicule.id,
            vehicule.marque,
            vehicule.modele,
            vehicule.immatriculation,
            vehicule.prix_par_jour,
            type_vehicule
        ))

        self.db.commit()
        self.liste_vehicules.append(vehicule)

    def afficher_vehicules(self):
        self.cursor.execute("SELECT * FROM vehicules")
        vehicules = self.cursor.fetchall()

        for v in vehicules:
            print(v)

    def trouver_vehicule(self, vehicule_id):
        self.cursor.execute("SELECT * FROM vehicules WHERE id = ?", (vehicule_id,))
        return self.cursor.fetchone()

    def supprimer_vehicule(self, vehicule_id):
        self.cursor.execute("DELETE FROM vehicules WHERE id = ?", (vehicule_id,))
        self.db.commit()
        self.liste_vehicules = [v for v in self.liste_vehicules if v.id != vehicule_id]