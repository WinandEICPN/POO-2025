import sqlite3


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect("biblio.db")
            cls._instance.cursor = cls._instance.conn.cursor()
        return cls._instance

    def create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS livres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT
            )
            """
        )

        self.cursor.execute("PRAGMA table_info(livres)")
        colonnes_livres = [col[1] for col in self.cursor.fetchall()]

        if "disponible" not in colonnes_livres:
            self.cursor.execute(
                "ALTER TABLE livres ADD COLUMN disponible INTEGER DEFAULT 1"
            )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS emprunts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_livre INTEGER NOT NULL,
                id_utilisateur INTEGER NOT NULL,
                duree_jours INTEGER NOT NULL DEFAULT 1,
                date_emprunt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_retour TIMESTAMP,
                FOREIGN KEY (id_livre) REFERENCES livres(id),
                FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id)
            )
            """
        )

        self.cursor.execute("PRAGMA table_info(emprunts)")
        colonnes_emprunts = [col[1] for col in self.cursor.fetchall()]

        if "duree_jours" not in colonnes_emprunts:
            self.cursor.execute(
                "ALTER TABLE emprunts ADD COLUMN duree_jours INTEGER DEFAULT 1"
            )

        self.conn.commit()

    def ajouter_livre(self, titre):
        self.cursor.execute(
            "INSERT INTO livres (titre, disponible) VALUES (?, 1)",
            (titre,),
        )
        self.conn.commit()
        return True, "Livre ajoute"

    def supprimer_livre(self, titre_livre):
        self.cursor.execute(
            """
            SELECT id, disponible FROM livres
            WHERE LOWER(TRIM(titre)) = LOWER(TRIM(?))
            ORDER BY id
            LIMIT 1
            """,
            (titre_livre,),
        )
        livre = self.cursor.fetchone()
        if livre is None:
            return False, "Livre introuvable"
        if livre[1] == 0:
            return False, "Suppression impossible: livre emprunte"

        self.cursor.execute(
            "DELETE FROM livres WHERE id = ?",
            (livre[0],),
        )
        self.conn.commit()
        return True, "Livre supprime"

    def get_livres(self):
        self.cursor.execute("SELECT * FROM livres ORDER BY titre")
        return self.cursor.fetchall()

    def utilisateur_existe(self, nom_utilisateur):
        self.cursor.execute(
            """
            SELECT id FROM utilisateurs
            WHERE LOWER(TRIM(nom)) = LOWER(TRIM(?))
            ORDER BY id
            LIMIT 1
            """,
            (nom_utilisateur,),
        )
        return self.cursor.fetchone() is not None

    def emprunter_livre(self, titre_livre, nom_utilisateur, duree_jours):
        self.cursor.execute(
            """
            SELECT id, disponible FROM livres
            WHERE LOWER(TRIM(titre)) = LOWER(TRIM(?))
            ORDER BY id
            LIMIT 1
            """,
            (titre_livre,),
        )
        livre = self.cursor.fetchone()
        if livre is None:
            return False, "Livre introuvable"
        if livre[1] == 0:
            return False, "Livre deja emprunte"

        self.cursor.execute(
            """
            SELECT id FROM utilisateurs
            WHERE LOWER(TRIM(nom)) = LOWER(TRIM(?))
            ORDER BY id
            LIMIT 1
            """,
            (nom_utilisateur,),
        )
        utilisateur = self.cursor.fetchone()
        if utilisateur is None:
            return False, "Utilisateur non enregistre. Inscription obligatoire"

        self.cursor.execute(
            "UPDATE livres SET disponible = 0 WHERE id = ?",
            (livre[0],),
        )
        self.cursor.execute(
            """
            INSERT INTO emprunts (id_livre, id_utilisateur, duree_jours, date_retour)
            VALUES (?, ?, ?, NULL)
            """,
            (livre[0], utilisateur[0], duree_jours),
        )
        self.conn.commit()
        return True, "Livre emprunte"

    def rendre_livre(self, titre_livre, nom_utilisateur):
        self.cursor.execute(
            """
            SELECT id FROM livres
            WHERE LOWER(TRIM(titre)) = LOWER(TRIM(?))
            ORDER BY id
            LIMIT 1
            """,
            (titre_livre,),
        )
        livre = self.cursor.fetchone()
        if livre is None:
            return False, "Livre introuvable"

        self.cursor.execute(
            """
            SELECT id FROM utilisateurs
            WHERE LOWER(TRIM(nom)) = LOWER(TRIM(?))
            ORDER BY id
            LIMIT 1
            """,
            (nom_utilisateur,),
        )
        utilisateur = self.cursor.fetchone()
        if utilisateur is None:
            return False, "Utilisateur non enregistre"

        self.cursor.execute(
            """
            SELECT id FROM emprunts
            WHERE id_livre = ? AND id_utilisateur = ? AND date_retour IS NULL
            ORDER BY id DESC
            LIMIT 1
            """,
            (livre[0], utilisateur[0]),
        )
        emprunt = self.cursor.fetchone()
        if emprunt is None:
            return False, "Aucun emprunt en cours pour ce livre et cet utilisateur"

        self.cursor.execute(
            """
            UPDATE emprunts
            SET date_retour = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (emprunt[0],),
        )
        self.cursor.execute(
            "UPDATE livres SET disponible = 1 WHERE id = ?",
            (livre[0],),
        )
        self.conn.commit()
        return True, "Livre rendu"

    def get_emprunts_actifs(self):
        self.cursor.execute(
            """
            SELECT e.id, l.titre, u.nom, e.duree_jours, e.date_emprunt
            FROM emprunts e
            JOIN livres l ON l.id = e.id_livre
            JOIN utilisateurs u ON u.id = e.id_utilisateur
            WHERE e.date_retour IS NULL
            ORDER BY e.date_emprunt DESC
            """
        )
        return self.cursor.fetchall()

    def ajouter_utilisateur(self, nom):
        self.cursor.execute(
            "INSERT INTO utilisateurs (nom) VALUES (?)",
            (nom,),
        )
        self.conn.commit()
        return True, "Utilisateur ajoute"

    def modifier_utilisateur(self, ancien_nom, nouveau_nom):
        self.cursor.execute(
            """
            SELECT id FROM utilisateurs
            WHERE LOWER(TRIM(nom)) = LOWER(TRIM(?))
            ORDER BY id
            LIMIT 1
            """,
            (ancien_nom,),
        )
        utilisateur = self.cursor.fetchone()
        if utilisateur is None:
            return False, "Utilisateur introuvable"

        self.cursor.execute(
            "UPDATE utilisateurs SET nom = ? WHERE id = ?",
            (nouveau_nom, utilisateur[0]),
        )
        self.conn.commit()
        return True, "Utilisateur modifie"

    def supprimer_utilisateur(self, nom):
        self.cursor.execute(
            """
            SELECT id FROM utilisateurs
            WHERE LOWER(TRIM(nom)) = LOWER(TRIM(?))
            ORDER BY id
            LIMIT 1
            """,
            (nom,),
        )
        utilisateur = self.cursor.fetchone()
        if utilisateur is None:
            return False, "Utilisateur introuvable"

        self.cursor.execute(
            """
            SELECT id FROM emprunts
            WHERE id_utilisateur = ? AND date_retour IS NULL
            LIMIT 1
            """,
            (utilisateur[0],),
        )
        emprunt_actif = self.cursor.fetchone()
        if emprunt_actif is not None:
            return False, "Suppression impossible: utilisateur avec emprunt en cours"

        self.cursor.execute(
            "DELETE FROM utilisateurs WHERE id = ?",
            (utilisateur[0],),
        )
        self.conn.commit()
        return True, "Utilisateur supprime"

    def get_utilisateurs(self):
        self.cursor.execute("SELECT * FROM utilisateurs ORDER BY nom")
        return self.cursor.fetchall()
