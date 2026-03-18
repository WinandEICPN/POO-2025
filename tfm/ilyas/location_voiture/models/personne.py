class Personne:

    def __init__(self, personne_id, nom, email):
        self.id = personne_id
        self.nom = nom
        self.email = email

    def afficher_infos(self):
        return f"ID: {self.id}, Nom: {self.nom}, Email: {self.email}"