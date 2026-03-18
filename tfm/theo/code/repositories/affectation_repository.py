"""
Repository des affectations, gère le lien entre machines et vulnérabilités.
Utilise la classe Affectation.
"""
from datetime import datetime
from database.db_connection import DatabaseConnection
from models.affectation import Affectation


class AffectationRepository:

    def __init__(self):
        self._db = DatabaseConnection()

    def assign(self, machine_id: int, vuln_id: int, note: str = "") -> bool:
        """Associe une vulnérabilité à une machine avec le statut 'En cours'."""
        affectation = Affectation(machine_id=machine_id, vuln_id=vuln_id, note=note)
        if not affectation.validate():
            return False
        cursor = self._db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO machine_vulnerabilities
                    (machine_id, vuln_id, assigned_date, status, fix_date, note)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (affectation.machine_id, affectation.vuln_id,
                  affectation.assigned_date, affectation.status,
                  affectation.fix_date, affectation.note))
            self._db.commit()
            return True
        except Exception:
            return False

    def unassign(self, machine_id: int, vuln_id: int) -> bool:
        """Supprime l'association entre une machine et une vulnérabilité."""
        cursor = self._db.get_cursor()
        cursor.execute(
            "DELETE FROM machine_vulnerabilities WHERE machine_id=? AND vuln_id=?",
            (machine_id, vuln_id)
        )
        self._db.commit()
        return cursor.rowcount > 0

    def update_status(self, machine_id: int, vuln_id: int,
                      status: str, fix_date: str = None) -> bool:
        """Met à jour le statut de l'affectation via un objet Affectation."""
        affectation = Affectation(machine_id=machine_id, vuln_id=vuln_id,
                                  status=status, fix_date=fix_date)
        cursor = self._db.get_cursor()
        cursor.execute("""
            UPDATE machine_vulnerabilities
            SET status = ?, fix_date = ?
            WHERE machine_id = ? AND vuln_id = ?
        """, (affectation.status, affectation.fix_date,
              affectation.machine_id, affectation.vuln_id))
        self._db.commit()
        return cursor.rowcount > 0

    def is_assigned(self, machine_id: int, vuln_id: int) -> bool:
        cursor = self._db.get_cursor()
        cursor.execute(
            "SELECT 1 FROM machine_vulnerabilities WHERE machine_id=? AND vuln_id=?",
            (machine_id, vuln_id)
        )
        return cursor.fetchone() is not None

    def get_assigned_vuln_ids(self, machine_id: int) -> list:
        cursor = self._db.get_cursor()
        cursor.execute(
            "SELECT vuln_id FROM machine_vulnerabilities WHERE machine_id=?",
            (machine_id,)
        )
        return [row["vuln_id"] for row in cursor.fetchall()]

    def get_affectation_info(self, machine_id: int, vuln_id: int):
        """Retourne un objet Affectation ou None."""
        cursor = self._db.get_cursor()
        cursor.execute(
            "SELECT * FROM machine_vulnerabilities WHERE machine_id=? AND vuln_id=?",
            (machine_id, vuln_id)
        )
        row = cursor.fetchone()
        if row:
            return self._row_to_affectation(row)
        return None

    def find_all(self, sort_by: str = "criticality") -> list:
        """
        Retourne toutes les affectations avec JOIN.
        Chaque dict contient les données machine + vulnérabilité + affectation
        pour l'affichage dans l'UI.
        """
        cursor = self._db.get_cursor()
        order = {
            "criticality": """ORDER BY CASE v.criticality
                WHEN 'Critique' THEN 1 WHEN 'Élevé' THEN 2
                WHEN 'Moyen'    THEN 3 WHEN 'Faible' THEN 4 END""",
            "status":  "ORDER BY mv.status, m.name",
            "machine": "ORDER BY m.name, v.title"
        }.get(sort_by, "ORDER BY m.name")

        cursor.execute(f"""
            SELECT
                m.id         AS machine_id,
                m.name       AS machine_name,
                m.ip_address,
                v.id         AS vuln_id,
                v.title,
                v.cve_id,
                v.criticality,
                v.type,
                mv.status,
                mv.assigned_date,
                mv.fix_date,
                mv.note
            FROM machine_vulnerabilities mv
            JOIN machines m        ON m.id = mv.machine_id
            JOIN vulnerabilities v ON v.id = mv.vuln_id
            {order}
        """)
        return [dict(row) for row in cursor.fetchall()]

    def _row_to_affectation(self, row) -> Affectation:
        """Convertit une ligne SQL en objet Affectation."""
        return Affectation(
            machine_id=row["machine_id"],
            vuln_id=row["vuln_id"],
            assigned_date=row["assigned_date"],
            status=row["status"],
            fix_date=row["fix_date"],
            note=row["note"],
            affectation_id=row["id"]
        )