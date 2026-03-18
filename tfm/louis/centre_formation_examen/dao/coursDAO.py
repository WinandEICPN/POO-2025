from database.database import Database
from models.cours import Cours

class CoursDAO:
   #DAO pour table cours

    def __init__(self):
        self.conn = Database().get_connection()
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS cours (id INTEGER PRIMARY KEY, titre TEXT, duree INTEGER, formateur_id INTEGER)"
        )

    def insert(self,c: Cours):
        self.conn.execute(
            "INSERT INTO cours (titre,duree,formateur_id) VALUES (?,?,?)",
            (c.titre,c.duree,c.formateur_id)
        )
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute("SELECT * FROM cours")
        return [tuple(row) for row in cursor]

    def delete(self,c_id):
        self.conn.execute("DELETE FROM cours WHERE id=?",(c_id,))
        self.conn.commit()