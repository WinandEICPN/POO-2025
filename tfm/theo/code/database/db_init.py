"""
Initialisation de la base de données.
Crée les tables si elles n'existent pas encore au premier lancement.
"""
from database.db_connection import DatabaseConnection


def initialize_database():
    """
    Crée les tables de la base de données au premier lancement.
    Utilise IF NOT EXISTS pour être idempotent.
    """
    db = DatabaseConnection()
    cursor = db.get_cursor()

    # Table des machines
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS machines (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            ip_address  TEXT NOT NULL,
            os          TEXT NOT NULL,
            description TEXT DEFAULT ''
        )
    """)

    # Table des vulnérabilités
    # extra_field1 et extra_field2 stockent les données spécifiques à chaque type
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vulnerabilities (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            title           TEXT NOT NULL,
            description     TEXT DEFAULT '',
            cve_id          TEXT DEFAULT '',
            criticality     TEXT NOT NULL DEFAULT 'Moyen',
            type            TEXT NOT NULL,
            discovery_date  TEXT NOT NULL,
            extra_field1    TEXT DEFAULT '',
            extra_field2    TEXT DEFAULT ''
        )
    """)

    # Table d'affectation — relie machines et vulnérabilités
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS machine_vulnerabilities (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id      INTEGER NOT NULL,
            vuln_id         INTEGER NOT NULL,
            assigned_date   TEXT NOT NULL,
            fix_date        TEXT,
            status          TEXT NOT NULL DEFAULT 'En cours',
            note            TEXT DEFAULT '',
            FOREIGN KEY (machine_id) REFERENCES machines(id) ON DELETE CASCADE,
            FOREIGN KEY (vuln_id)    REFERENCES vulnerabilities(id) ON DELETE CASCADE,
            UNIQUE (machine_id, vuln_id)
        )
    """)

    db.commit()
    print("Base de données initialisée avec succès.")
