from personne import Personne

class Utilisateur(Personne):
    def afficher(self):
        return f"Utilisateur: {self.nom}"
