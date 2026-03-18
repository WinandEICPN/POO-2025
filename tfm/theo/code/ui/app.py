"""
Application principale
"""
import tkinter as tk
from tkinter import ttk, messagebox

from database.db_connection import DatabaseConnection
from ui.machines_frame import MachinesFrame
from ui.vulnerabilities_frame import VulnerabilitiesFrame
from ui.affectations_frame import AffectationsFrame


class App(tk.Tk):
    """
    Fenêtre principale de l'application VulnTracker.
    Hérite de tk.Tk
    """

    def __init__(self):
        super().__init__()
        self.title("🛡️ VulnTracker — Suivi des vulnérabilités")
        self.geometry("1100x680")
        self.minsize(900, 550)
        self.configure(bg="#1e1e2e")

        self._build_header()
        self._build_notebook()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_header(self):
        """Construit la barre de titre."""
        header = tk.Frame(self, bg="#11111b", pady=10)
        header.pack(fill="x")
        tk.Label(
            header,
            text="🛡️  VulnTracker",
            font=("Helvetica", 18, "bold"),
            bg="#11111b",
            fg="#cdd6f4"
        ).pack(side="left", padx=20)
        tk.Label(
            header,
            text="Inventaire de sécurité des machines",
            font=("Helvetica", 10),
            bg="#11111b",
            fg="#6c7086"
        ).pack(side="left")

    def _build_notebook(self):
        """Crée le notebook avec les 3 onglets principaux."""
        style = ttk.Style(self)
        style.theme_use("clam")

        # Style du notebook
        style.configure("TNotebook", background="#1e1e2e", borderwidth=0)
        style.configure("TNotebook.Tab",
                        background="#313244", foreground="#cdd6f4",
                        padding=[15, 8], font=("Helvetica", 10))
        style.map("TNotebook.Tab",
                  background=[("selected", "#89b4fa")],
                  foreground=[("selected", "#1e1e2e")])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Instanciation des onglets
        self.machines_frame = MachinesFrame(self.notebook)
        self.vulns_frame = VulnerabilitiesFrame(self.notebook)
        self.affectations_frame = AffectationsFrame(
            self.notebook,
            refresh_machines_cb=self.machines_frame.refresh,
            refresh_vulns_cb=self.vulns_frame.refresh
        )

        self.notebook.add(self.machines_frame,     text="Machines")
        self.notebook.add(self.vulns_frame,         text="Vulnerabilites")
        self.notebook.add(self.affectations_frame,  text="Affectations")

        # Rafraîchit le frame d'affectations lors du changement d'onglet
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _on_tab_changed(self, event):
        """Rafraîchit les données à chaque changement d'onglet."""
        selected = self.notebook.index(self.notebook.select())
        if selected == 2:  # Onglet Affectations
            self.affectations_frame.refresh()

    def _on_close(self):
        """Ferme proprement la connexion DB avant de quitter."""
        if messagebox.askokcancel("Quitter", "Voulez-vous quitter VulnTracker ?"):
            DatabaseConnection().close()
            self.destroy()
