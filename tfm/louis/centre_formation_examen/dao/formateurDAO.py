from database.database import Database
from models.formateur import Formateur

class FormateurDAO:
    #DAO pour table formateurs

    def __init__(self):
        self.conn = Database().get_connection()
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS formateurs (id INTEGER PRIMARY KEY, nom TEXT, email TEXT)"
        )

    def insert(self, f: Formateur):
        self.conn.execute(
            "INSERT INTO formateurs (nom,email) VALUES (?,?)",
            (f.nom,f.email)
        )
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute("SELECT * FROM formateurs")
        return [tuple(row) for row in cursor]

    def delete(self, f_id):
        self.conn.execute("DELETE FROM formateurs WHERE id=?",(f_id,))
        self.conn.commit()