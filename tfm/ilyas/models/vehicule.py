from abc import ABC, abstractmethod


class Vehicule(ABC):

    def __init__(self, vehicule_id, marque, modele, immatriculation, prix_par_jour):
        self.id = vehicule_id
        self.marque = marque
        self.modele = modele
        self.immatriculation = immatriculation
        self.prix_par_jour = prix_par_jour
        self.disponible = True

    def afficher_infos(self):
        return f"{self.marque} {self.modele} - {self.immatriculation} | Prix/jour: {self.prix_par_jour}€ | Disponible: {self.disponible}"

    def louer(self):
        if not self.disponible:
            raise Exception("Ce véhicule est déjà loué.")
        self.disponible = False

    def retourner(self):
        self.disponible = True

    @abstractmethod
    def calculer_prix_location(self, nb_jours):
        pass