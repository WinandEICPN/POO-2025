
#classe bastraite tout le monde va en hériter
# permet de laisser le choix d'implementer certaines methoeds aux classes filles
from abc import ABC, abstractmethod


class EntiteBase(ABC):

# Méthode abstraite afficher description
    @abstractmethod
    def afficher(self):
        pass

# verifie que donnees sont valides pour chaque objet
    @abstractmethod
    def valider(self):
        pass

# retourne les données sous forme de dictionnaire
    @abstractmethod
    def to_dict(self):
        pass

# afficher string
    def __str__(self):
        return self.afficher()
