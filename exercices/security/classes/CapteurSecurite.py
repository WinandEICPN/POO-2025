from abc import ABC, abstractmethod

from .Journal import Journal


class CapteurSecurite(ABC):
    def __init__(self, nom: str, actif: bool = True):
        self._nom = nom
        self._actif = actif
        self._dernier_score = 0.0

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def actif(self) -> bool:
        return self._actif

    @actif.setter
    def actif(self, valeur: bool):
        self._actif = valeur

    @abstractmethod
    def analyser(self, journal: list[Journal]) -> None:
        pass

    @abstractmethod
    def niveau_risque(self) -> float:
        pass

    def description(self) -> str:
        return f"Capteur '{self._nom}' ({self.__class__.__name__}) - {"actif" if self._actif else "inactif"} - risque={self._dernier_score:.2f}"


class CapteurAntivirus(CapteurSecurite):
    def analyser(self, journal: list[Journal]) -> None:
        if not journal:
            self._dernier_score = 0.0
            return

        nb_suspects = 0
        nb_alertes = 0
        for j in journal:
            if j.niveau == 1:
                nb_suspects += 1
            elif j.niveau == 2:
                nb_alertes += 1
        total = len(journal)

        self._dernier_score = ((nb_suspects * 1) + (nb_alertes * 2)) / (2 * total) * 100

    def niveau_risque(self) -> float:
        return self._dernier_score


class CapteurIDS(CapteurSecurite, ABC):
    def __init__(self, nom: str, actif: bool = True):
        super().__init__(nom, actif)
        self.nb_normaux = 0
        self.nb_suspects = 0
        self.nb_alertes = 0

    def niveau_risque(self) -> float:
        total = self.nb_normaux + self.nb_suspects + self.nb_alertes
        if total == 0:
            self._dernier_score = 0.0
        else:
            self._dernier_score = ((self.nb_suspects * 1.5) + (self.nb_alertes * 3)) / (3 * total) * 100
        return self._dernier_score



class CapteurIDSReseau(CapteurIDS):
    def analyser(self, journal: list[Journal]) -> None:

        for j in journal:
            if j.niveau == 0:
                self.nb_normaux += 1
            elif j.niveau == 1:
                self.nb_suspects += 1
            elif j.niveau == 2:
                self.nb_alertes += 1

        self.niveau_risque()


class CapteurIDSSysteme(CapteurIDS):
    def analyser(self, journal: list[Journal]) -> None:
        for j in journal:
            if j.niveau == 0:
                self.nb_normaux += 1
            elif j.niveau == 1:
                # On “sur-compte” légèrement les suspects pour un système
                self.nb_suspects += 1
            elif j.niveau == 2:
                self.nb_alertes += 1

        self.niveau_risque()
