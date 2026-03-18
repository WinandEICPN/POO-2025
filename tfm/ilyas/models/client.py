from .personne import Personne


class Client(Personne):

    def __init__(self, personne_id, nom, email, numero_permis, password):
        super().__init__(personne_id, nom, email)
        self.numero_permis = numero_permis
        self.password = password

    def afficher_infos(self):
        return f"{super().afficher_infos()}, Permis: {self.numero_permis}"