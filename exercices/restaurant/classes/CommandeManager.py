from .Plat import Plat


class CommandeManager:
    _instance = None  # instance unique
    _init_done = False  # empêche la réinitialisation multiple

    def __new__(cls):
        # __new__ crée ou renvoie l’instance unique
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # __init__ peut être appelé plusieurs fois → protéger l'initialisation
        if not self._init_done:
            self._liste = []
            CommandeManager._init_done = True

    def ajouterPlat(self, plat: Plat):
        self._liste.append(plat)

    def printAllPlat(self):
        for plat in self._liste:
            print(plat.description())

