"""
Classe abstraite de base pour toutes les classes métier.
Toutes les classes métiers héritent de cette classe.
"""
from abc import ABC, abstractmethod


class Entity(ABC):

    @abstractmethod
    def validate(self) -> bool:
        """Vérifie que les données de l'entité sont valides avant sauvegarde."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Sérialise l'entité en dictionnaire (utile pour la DB et l'UI)."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Représentation lisible de l'objet."""
        pass


