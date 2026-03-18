class ClientService:

    def __init__(self):
        # The UI expects `liste_clients` (French naming) while internal code may use `clients`.
        # Keep both names in sync to avoid AttributeError when the UI accesses `client_service.liste_clients`.
        self.liste_clients = []
        self.clients = self.liste_clients

    def ajouter_client(self, client):
        self.liste_clients.append(client)

    def afficher_clients(self):
        for c in self.liste_clients:
            print(c.afficher_infos())

    def trouver_client(self, client_id):
        for c in self.liste_clients:
            if c.id == client_id:
                return c
        return None