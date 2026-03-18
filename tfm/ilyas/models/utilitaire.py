from .vehicule import Vehicule


class Utilitaire(Vehicule):
    def __init__(self, vehicule_id, marque, modele, immatriculation, prix_par_jour, volume_charge):
        super().__init__(vehicule_id, marque, modele, immatriculation, prix_par_jour)
        self.volume_charge = volume_charge

    def calculer_prix_location(self, nb_jours):
        return (self.prix_par_jour * nb_jours) + 20

    def afficher_infos(self):
        return f"{super().afficher_infos()}, Volume de charge: {self.volume_charge} m3"