class ClientService:

    def __init__(self):
        self.clients = []

    def ajouter_client(self, client):
        self.clients.append(client)

    def afficher_clients(self):
        for c in self.clients:
            print(c.afficher_infos())

    def trouver_client(self, client_id):
        for c in self.clients:
            if c.id == client_id:
                return c
        return None