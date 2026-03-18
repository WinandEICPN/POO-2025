from models.base_model import BaseModel

class Cours(BaseModel):
    
    #Classe Cours avec titre, durée, et formateur
    
    def __init__(self, titre, duree, formateur_id):
        self._titre = titre.strip()
        self._duree = duree
        self._formateur_id = formateur_id
        self._validate()

    def _validate(self):
        if not self._titre:
            raise ValueError("Titre obligatoire")
        if self._titre.isdigit():
            raise ValueError("Titre ne peut pas être un chiffre")
        if not isinstance(self._duree,int) or self._duree <= 0:
            raise ValueError("Durée invalide")

    @property
    def titre(self):
        return self._titre

    @property
    def duree(self):
        return self._duree

    @property
    def formateur_id(self):
        return self._formateur_id

    def save(self):
        pass

    def delete(self):
        pass