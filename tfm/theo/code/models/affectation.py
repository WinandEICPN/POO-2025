"""
Classe Affectation — représente le lien entre une machine et une vulnérabilité.
Hérite de Entity.
"""
from datetime import datetime
from models.entity import Entity


class Affectation(Entity):
    """
    Représente une affectation d'une vulnérabilité à une machine.
    Chaque affectation a son propre statut et sa propre date de correction,
    elles sont indépendantes de la vulnérabilité globale.
    """

    VALID_STATUSES = ["En cours", "Terminé"]

    def __init__(self, machine_id: int, vuln_id: int,
                 assigned_date: str = None, status: str = "En cours",
                 fix_date: str = None, note: str = "",
                 affectation_id: int = None):
        self.__id            = affectation_id
        self.__machine_id    = machine_id
        self.__vuln_id       = vuln_id
        self.__assigned_date = assigned_date or datetime.now().strftime("%Y-%m-%d")
        self.__status        = status
        self.__fix_date      = fix_date
        self.__note          = note

    # Propriétés

    @property
    def id(self):
        return self.__id

    @property
    def machine_id(self):
        return self.__machine_id

    @property
    def vuln_id(self):
        return self.__vuln_id

    @property
    def assigned_date(self):
        return self.__assigned_date

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value: str):
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Statut invalide. Valeurs acceptées : {self.VALID_STATUSES}")
        self.__status = value

    @property
    def fix_date(self):
        return self.__fix_date

    @fix_date.setter
    def fix_date(self, value: str):
        self.__fix_date = value

    @property
    def note(self):
        return self.__note

    @note.setter
    def note(self, value: str):
        self.__note = value.strip() if value else ""

    # Méthodes abstraites implémentées

    def validate(self) -> bool:
        if not self.__machine_id or not self.__vuln_id:
            return False
        if self.__status not in self.VALID_STATUSES:
            return False
        return True

    def to_dict(self) -> dict:
        return {
            "id":            self.__id,
            "machine_id":    self.__machine_id,
            "vuln_id":       self.__vuln_id,
            "assigned_date": self.__assigned_date,
            "status":        self.__status,
            "fix_date":      self.__fix_date,
            "note":          self.__note
        }

    def __str__(self):
        return (f"Affectation[machine={self.__machine_id}, vuln={self.__vuln_id}] "
                f"| Statut: {self.__status}")