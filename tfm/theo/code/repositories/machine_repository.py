"""
Repository des machines, gère toutes les opérations CRUD db.
La logique db est ici et non pas dans les classes métier.
"""
from database.db_connection import DatabaseConnection
from models.machine import Machine


class MachineRepository:
    """
    Gère la persistance des objets Machine en db.
    """

    def __init__(self):
        self._db = DatabaseConnection()  # Singleton — toujours la même instance

    def insert(self, machine: Machine) -> int:
        """Insère une nouvelle machine. Retourne l'ID généré."""
        if not machine.validate():
            raise ValueError("Les données de la machine sont invalides.")

        cursor = self._db.get_cursor()
        cursor.execute(
            "INSERT INTO machines (name, ip_address, os, description) VALUES (?, ?, ?, ?)",
            (machine.name, machine.ip_address, machine.os, machine.description)
        )
        self._db.commit()
        return cursor.lastrowid

    def update(self, machine: Machine) -> bool:
        """Met à jour une machine existante. Retourne True si ok."""
        if not machine.validate():
            raise ValueError("Les données de la machine sont invalides.")
        if machine.id is None:
            raise ValueError("Impossible de mettre à jour une machine sans ID.")

        cursor = self._db.get_cursor()
        cursor.execute(
            "UPDATE machines SET name=?, ip_address=?, os=?, description=? WHERE id=?",
            (machine.name, machine.ip_address, machine.os, machine.description, machine.id)
        )
        self._db.commit()
        return cursor.rowcount > 0

    def delete(self, machine_id: int) -> bool:
        """Supprime une machine par son ID. Retourne True si ok."""
        cursor = self._db.get_cursor()
        cursor.execute("DELETE FROM machines WHERE id=?", (machine_id,))
        self._db.commit()
        return cursor.rowcount > 0

    def find_by_id(self, machine_id: int):
        """Retourne un objet Machine correspondant à l'ID, ou None si inexistant."""
        cursor = self._db.get_cursor()
        cursor.execute("SELECT * FROM machines WHERE id=?", (machine_id,))
        row = cursor.fetchone()
        return self._row_to_machine(row) if row else None

    def find_all(self) -> list:
        """Retourne la liste de toutes les machines."""
        cursor = self._db.get_cursor()
        cursor.execute("SELECT * FROM machines ORDER BY name")
        return [self._row_to_machine(row) for row in cursor.fetchall()]

    def _row_to_machine(self, row) -> Machine:
        """Convertit une ligne SQLite en objet Machine."""
        return Machine(
            name=row["name"],
            ip_address=row["ip_address"],
            os=row["os"],
            description=row["description"],
            machine_id=row["id"]
        )
