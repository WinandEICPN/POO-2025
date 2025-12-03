from abc import ABC, abstractmethod

class Plat(ABC):
    def __init__(self, nom: str, prixBase: float):
        self.nom = nom
        self.prixBase = prixBase

    @abstractmethod
    def prix_final(self):
        pass

    def description(self) -> str:
        return f"Plat : {self.nom}, prix de base : {prix_base} €"

class PlatChaud(Plat):
    def __init__(self, nom: str, prixBase: float):
        super().__init__(nom, prixBase)
        self.TVA = 1.12

    def prix_final(self):
        return (self.prixBase * self.TVA)


