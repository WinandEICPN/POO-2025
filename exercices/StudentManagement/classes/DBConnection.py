import sqlite3


class DBConnection:
    _instance = None  # Attribut de classe pour stocker l'unique instance

    def __init__(self, db_path: str = "../resources/db/database.db"):
        self._connection = sqlite3.connect("resources/db/database.db")

        self._connection.row_factory = sqlite3.Row
        init_schema(self)

    @classmethod
    def get_instance(cls, db_path: str = "../resources/db/database.db"):
        if cls._instance is None:
            cls._instance = DBConnection(db_path)

        return cls._instance

    def get_connection(self) -> sqlite3.Connection:

        return self._connection


def init_schema(self):
    cur = self._connection.cursor()

    cur.execute(""" 
    CREATE TABLE IF NOT EXISTS TStudent(
       Id_TStudent INTEGER,
       Nom TEXT,
       Mail TEXT,
       PRIMARY KEY(Id_TStudent)
    );
   """)

    cur.execute(""" 
    CREATE TABLE IF NOT EXISTS  TCourse(
       Id_TCourse INTEGER,
       Titre TEXT,
       Credit INTEGER,
       PRIMARY KEY(Id_TCourse)
    );
   """)

    cur.execute(""" 
    CREATE TABLE IF NOT EXISTS  TEnrollment(
       Id_TStudent INTEGER,
       Id_TCourse INTEGER,
       date_inscription NUMERIC,
       note NUMERIC(15,2)  ,
       PRIMARY KEY(Id_TStudent, Id_TCourse),
       FOREIGN KEY(Id_TStudent) REFERENCES TStudent(Id_TStudent),
       FOREIGN KEY(Id_TCourse) REFERENCES TCourse(Id_TCourse)
    );
   """)

    self._connection.commit()

    cur.execute("SELECT * FROM TStudent")
    rows = cur.fetchall()
    if len(rows) == 0:
        cur.execute("""INSERT
        INTO
        TStudent(Id_TStudent, Nom, Mail)
        VALUES
        (1, 'Alice Dupont', 'alice.dupont@ecole.be'),
        (2, 'Benoit Martin', 'benoit.martin@ecole.be'),
        (3, 'Chloe Bernard', 'chloe.bernard@ecole.be'),
        (4, 'Dylan Simon', 'dylan.simon@ecole.be'),
        (5, 'Emma Leroy', 'emma.leroy@ecole.be');""")

        cur.execute("""INSERT
        INTO
        TCourse(Id_TCourse, Titre, Credit)
        VALUES
        (1, 'Python - Bases', 5),
        (2, 'Bases de données', 4),
        (3, 'Réseaux - Introduction', 3);""")

        cur.execute("""INSERT
        INTO
        TEnrollment(Id_TStudent, Id_TCourse, date_inscription, note)
        VALUES (1, 1, '2025-09-10', 14.50),
        (1, 2, '2025-09-12', 13.00),
        (1, 3, '2025-09-15', 15.25),

        (2, 1, '2025-09-10', 12.00),
        (2, 2, '2025-09-12', 16.00),
        (2, 3, '2025-09-15', 11.75),

        (3, 1, '2025-09-11', 17.00),
        (3, 2, '2025-09-13', 14.00),
        (3, 3, '2025-09-16', 13.50),

        (4, 1, '2025-09-11', 10.00),
        (4, 3, '2025-09-16', 12.25),
        (5, 2, '2025-09-13', 15.00);""")
        self._connection.commit()


