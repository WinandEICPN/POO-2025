from database.init_db import create_tables
from models.voiture import Voiture
from models.utilitaire import Utilitaire
from models.client import Client
from models.location import Location

from service.vehicule_service import VehiculeService
from service.client_service import ClientService
from service.location_service import LocationService


def main():
    
    create_tables()
    
    vehicule_service = VehiculeService()
    client_service = ClientService()
    location_service = LocationService()

    # Création véhicules
    voiture1 = Voiture(1, "Toyota", "Yaris", "AA123BB", 40, 5)
    utilitaire1 = Utilitaire(2, "Renault", "Master", "CC456DD", 60, 12)

    vehicule_service.ajouter_vehicule(voiture1)
    vehicule_service.ajouter_vehicule(utilitaire1)

    # Création client
    client1 = Client(1, "Ilyas", "ilyas@email.com", "PERMIS123", "password123")
    client_service.ajouter_client(client1)

    # Location
    location1 = Location(1, client1, voiture1, 3)
    location_service.ajouter_location(location1)

    print("\n=== VEHICULES ===")
    vehicule_service.afficher_vehicules()

    print("\n=== CLIENTS ===")
    client_service.afficher_clients()

    print("\n=== LOCATIONS ===")
    location_service.afficher_locations()


if __name__ == "__main__":
    main()


import os
import sqlite3

print("Dossier courant :", os.getcwd())

conn = sqlite3.connect("test.db")
print("database créée")
conn.close()
print(Voiture)