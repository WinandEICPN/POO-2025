class LocationService:

    def __init__(self):
        # UI code uses `liste_locations` (French naming). Keep it in sync.
        self.liste_locations = []
        self.locations = self.liste_locations

    def ajouter_location(self, location):
        self.liste_locations.append(location)

    def afficher_locations(self):
        for l in self.liste_locations:
            print(l.afficher_infos())