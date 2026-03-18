from database.database import Database

class InscriptionDAO:
    #DAO pour table inscriptions#

    def __init__(self):
        self.conn = Database().get_connection()
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS inscriptions (id INTEGER PRIMARY KEY, etudiant_id INTEGER, cours_id INTEGER)"
        )

    def insert(self, etudiant_id, cours_id):
        self.conn.execute(
            "INSERT INTO inscriptions (etudiant_id,cours_id) VALUES (?,?)",
            (etudiant_id, cours_id)
        )
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute("SELECT * FROM inscriptions")
        return [tuple(row) for row in cursor]

    def delete(self, insc_id):
        self.conn.execute("DELETE FROM inscriptions WHERE id=?",(insc_id,))
        self.conn.commit()