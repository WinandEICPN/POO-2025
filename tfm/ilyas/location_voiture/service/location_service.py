class LocationService:

    def __init__(self):
        self.locations = []

    def ajouter_location(self, location):
        self.locations.append(location)

    def afficher_locations(self):
        for l in self.locations:
            print(l.afficher_infos())