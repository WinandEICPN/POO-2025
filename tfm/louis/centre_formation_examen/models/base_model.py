from abc import ABC, abstractmethod

class BaseModel(ABC):

    #Classe abstraite pour les modèles métiers.
    #Définit un contrat pour toutes les entités : save et delete
    
    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass