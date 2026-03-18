from abc import ABC, abstractmethod

class Equipement(ABC):

    def __init__(self,nom,ip,etat):
        self.nom=nom
        self.ip=ip
        self.etat=etat

    @abstractmethod
    def afficher(self):
        pass