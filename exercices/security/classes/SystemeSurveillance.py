from .CapteurSecurite import *


class SystemeSurveillance:
    TYPE_ANTIVIRUS = "antivirus"
    TYPE_IDS_RESEAU = "ids_reseau"
    TYPE_IDS_SYSTEME = "ids_systeme"

    def __init__(self):
        self._capteurs: list[CapteurSecurite] = []

    def creer_capteur(self, type_capteur: str, nom: str, actif: bool = True) -> CapteurSecurite | None:
        if type_capteur == self.TYPE_ANTIVIRUS:
            capteur = CapteurAntivirus(nom, actif)
        elif type_capteur == self.TYPE_IDS_RESEAU:
            capteur = CapteurIDSReseau(nom, actif)
        elif type_capteur == self.TYPE_IDS_SYSTEME:
            capteur = CapteurIDSSysteme(nom, actif)
        else:
            return None

        self.ajouter_capteur(capteur)
        return capteur

    def ajouter_capteur(self, capteur: CapteurSecurite) -> None:
        self._capteurs.append(capteur)

    def lister_capteurs(self) -> list[CapteurSecurite]:
        return self._capteurs

    def analyser_tous(self, journal: list[Journal]) -> dict[str, float]:
        resultats: dict[str, float] = {}
        for capteur in self._capteurs:
            if capteur.actif:
                capteur.analyser(journal)
                resultats[capteur.nom] = capteur.niveau_risque()
        return resultats