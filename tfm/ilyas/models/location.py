from datetime import datetime


class Location:

    def __init__(self, location_id, client, vehicule, nb_jours):
        self.id = location_id
        self.client = client
        self.vehicule = vehicule
        self.nb_jours = nb_jours
        self.date_location = datetime.now()

    def calculer_prix(self):
        return self.vehicule.calculer_prix_location(self.nb_jours)

    def afficher_infos(self):
        return f"Location {self.id} | Client: {self.client.nom} | Véhicule: {self.vehicule.marque} {self.vehicule.modele} | Jours: {self.nb_jours} | Prix total: {self.calculer_prix()}€"