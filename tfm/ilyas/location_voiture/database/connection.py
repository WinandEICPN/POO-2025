import sqlite3


class DatabaseConnection:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            # Use a timeout to prevent "database is locked" errors when multiple connections
            # are briefly active; allow cross-thread use if the app ever uses threads.
            cls._instance.connection = sqlite3.connect(
                "location_voiture.db",
                timeout=5,
                check_same_thread=False,
            )
            cls._instance.cursor = cls._instance.connection.cursor()
        return cls._instance

    def get_cursor(self):
        return self.cursor

    def commit(self):
        self.connection.commit()