from models.base_model import BaseModel

class Personne(BaseModel):
    
    #Classe abstraite Personne pour Etudiant et Formateur
    #Contient nom, email et validation
    
    def __init__(self, nom, email):
        self._nom = nom.strip()
        self._email = email.strip()
        self._validate()

    def _validate(self):
        if not self._nom or not self._email:
            raise ValueError("Nom et email obligatoires")
        if "@" not in self._email:
            raise ValueError("Email invalide")

    @property
    def nom(self):
        return self._nom

    @property
    def email(self):
        return self._email