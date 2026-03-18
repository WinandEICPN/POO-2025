import sqlite3


class Database:

    def __init__(self):

        self.conn = sqlite3.connect("parc_informatique.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS locaux(
            id INTEGER PRIMARY KEY,
            nom TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipements(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            etat TEXT,
            local_id INTEGER,
            FOREIGN KEY(local_id) REFERENCES locaux(id)
        )
        """)

        self.cursor.execute("INSERT OR IGNORE INTO locaux VALUES (1,'Direction')")
        self.cursor.execute("INSERT OR IGNORE INTO locaux VALUES (2,'Employés')")

        self.conn.commit()

    def execute(self, query, params=()):

        self.cursor.execute(query, params)
        self.conn.commit()

        return self.cursor