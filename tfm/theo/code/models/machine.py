"""
Classe Machine, représente une machine dans l'inventaire.
Hérite de Entity et encapsule ses données via des propriétés.
"""
import re
from models.entity import Entity


class Machine(Entity):
    """
    Représente une machine physique ou virtuelle à surveiller.
    """

    def __init__(self, name: str, ip_address: str, os: str,
                 description: str = "", machine_id: int = None):
        # Attributs privés, accès contrôlé via propriétés
        self.__name = name
        self.__ip_address = ip_address
        self.__os = os
        self.__description = description
        self.__id = machine_id


    # Propriétés

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and value <= 0:
            raise ValueError("L'ID doit être un entier positif.")
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Le nom de la machine ne peut pas être vide.")
        self.__name = value.strip()

    @property
    def ip_address(self):
        return self.__ip_address

    @ip_address.setter
    def ip_address(self, value: str):
        """Valide le format d'une adresse IPv4."""
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, value):
            raise ValueError(f"Adresse IP invalide : {value}")
        parts = value.split(".")
        if any(int(p) > 255 for p in parts):
            raise ValueError(f"Adresse IP invalide (octet > 255) : {value}")
        self.__ip_address = value

    @property
    def os(self):
        return self.__os

    @os.setter
    def os(self, value: str):
        if not value or not value.strip():
            raise ValueError("Le système d'exploitation ne peut pas être vide.")
        self.__os = value.strip()

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value.strip() if value else ""

    # --- Méthodes abstraites implémentées ---

    def validate(self) -> bool:
        """Valide les champs obligatoires de la machine."""
        try:
            if not self.__name or not self.__name.strip():
                return False
            # Re-valide l'IP via le setter
            self.ip_address = self.__ip_address
            if not self.__os or not self.__os.strip():
                return False
            return True
        except ValueError:
            return False

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "name": self.__name,
            "ip_address": self.__ip_address,
            "os": self.__os,
            "description": self.__description
        }

    def __str__(self):
        return f"Machine[{self.__id}] {self.__name} — {self.__ip_address} ({self.__os})"
