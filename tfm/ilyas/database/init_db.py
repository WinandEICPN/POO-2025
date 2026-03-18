from .connection import DatabaseConnection


def create_tables():

    db = DatabaseConnection()
    cursor = db.get_cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicules(
        id INTEGER PRIMARY KEY,
        marque TEXT,
        modele TEXT,
        immatriculation TEXT,
        prix_par_jour REAL,
        type TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY,
        nom TEXT,
        email TEXT,
        numero_permis TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations(
        id INTEGER PRIMARY KEY,
        client_id INTEGER,
        vehicule_id INTEGER,
        nb_jours INTEGER
    )
    """)

    db.commit()