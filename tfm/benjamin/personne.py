from abc import ABC, abstractmethod

class Personne(ABC):
    def __init__(self, nom):
        self.nom = nom

    @abstractmethod
    def afficher(self):
        pass