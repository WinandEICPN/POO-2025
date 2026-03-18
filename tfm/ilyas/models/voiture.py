from .vehicule import Vehicule


class Voiture(Vehicule):

    def __init__(self, vehicule_id, marque, modele, immatriculation, prix_par_jour, nombre_portes):
        super().__init__(vehicule_id, marque, modele, immatriculation, prix_par_jour)
        self.nombre_portes = nombre_portes

    def calculer_prix_location(self, nb_jours):
        return self.prix_par_jour * nb_jours

    def afficher_infos(self):
        return f"{super().afficher_infos()}, Portes: {self.nombre_portes}"