import sqlite3

from exercices.tkinter.classes.db.DbConnection import DbConnection


# =========================
# DAO (accès DB)
# =========================
class UserDao:
    def __init__(self, db: DbConnection):
        self.db = db

    def create_table(self):
        self.db.execute("""
        CREATE TABLE IF NOT EXISTS TUser(
            Id_User INTEGER PRIMARY KEY AUTOINCREMENT,
            Nom TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL
        );
        """)

    def add_user(self, nom: str, pwd: str) -> bool:
        try:
            self.db.execute(
                "INSERT INTO TUser(Nom, Password) VALUES (?, ?)",
                (nom, pwd)
            )
            return True
        except sqlite3.IntegrityError:
            # Nom déjà existant (UNIQUE)
            return False

    def user_exists(self, nom: str, pwd: str) -> bool:
        cur = self.db.execute(
            "SELECT 1 FROM TUser WHERE Nom = ? AND Password = ?",
            (nom, pwd)
        )
        return cur.fetchone() is not None

