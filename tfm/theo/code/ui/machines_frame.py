"""
Frame de gestion des machines.
Affiche la liste des machines et permet d'ajouter, modifier, supprimer.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from models.machine import Machine
from repositories.machine_repository import MachineRepository

# Couleurs de l'interface (thème sombre)
BG = "#1e1e2e"
BG2 = "#313244"
FG = "#cdd6f4"
ACCENT = "#89b4fa"
RED = "#f38ba8"
GREEN = "#a6e3a1"
FONT = ("Helvetica", 10)


class MachinesFrame(tk.Frame):
    """
    Onglet machines.
    """

    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self._repo = MachineRepository()
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        """Construit l'interface barre d'outils + tableau."""
        # Barre d'outils
        toolbar = tk.Frame(self, bg=BG, pady=8)
        toolbar.pack(fill="x", padx=10)

        tk.Label(toolbar, text="Gestion des machines", font=("Helvetica", 13, "bold"),
                 bg=BG, fg=FG).pack(side="left")

        btn_frame = tk.Frame(toolbar, bg=BG)
        btn_frame.pack(side="right")

        self._btn(btn_frame, "＋ Ajouter",   GREEN,  self._open_add_dialog).pack(side="left", padx=4)
        self._btn(btn_frame, "✏ Modifier",   ACCENT, self._open_edit_dialog).pack(side="left", padx=4)
        self._btn(btn_frame, "✕ Supprimer",  RED,    self._delete_selected).pack(side="left", padx=4)

        # Tableau (Treeview)
        cols = ("ID", "Nom", "Adresse IP", "OS", "Description")
        self._tree = ttk.Treeview(self, columns=cols, show="headings",
                                  style="Custom.Treeview")
        self._style_tree()

        for col in cols:
            self._tree.heading(col, text=col)

        self._tree.column("ID",          width=50,  anchor="center")
        self._tree.column("Nom",         width=200)
        self._tree.column("Adresse IP",  width=130, anchor="center")
        self._tree.column("OS",          width=150)
        self._tree.column("Description", width=350)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)

        self._tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=5)
        scrollbar.pack(side="right", fill="y", pady=5, padx=(0, 10))

        # Double-clic pour modifier
        self._tree.bind("<Double-1>", lambda e: self._open_edit_dialog())

    def _style_tree(self):
        style = ttk.Style()
        style.configure("Custom.Treeview",
                        background=BG2, foreground=FG,
                        fieldbackground=BG2, rowheight=28,
                        font=FONT)
        style.configure("Custom.Treeview.Heading",
                        background="#11111b", foreground=ACCENT,
                        font=("Helvetica", 10, "bold"))
        style.map("Custom.Treeview", background=[("selected", "#45475a")])

    def _btn(self, parent, text, color, command):
        return tk.Button(parent, text=text, command=command,
                         bg=color, fg="#1e1e2e", font=("Helvetica", 9, "bold"),
                         relief="flat", padx=10, pady=5, cursor="hand2",
                         activebackground=color)

    def refresh(self):
        """Recharge la liste des machines depuis la base de données."""
        for row in self._tree.get_children():
            self._tree.delete(row)
        for machine in self._repo.find_all():
            d = machine.to_dict()
            self._tree.insert("", "end", values=(
                d["id"], d["name"], d["ip_address"], d["os"], d["description"]
            ))

    def _get_selected_id(self):
        """Retourne l'ID de la machine sélectionnée, ou None."""
        selected = self._tree.selection()
        if not selected:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner une machine.")
            return None
        return int(self._tree.item(selected[0])["values"][0])

    def _open_add_dialog(self):
        MachineDialog(self, title="Ajouter une machine", on_save=self._save_new)

    def _open_edit_dialog(self):
        machine_id = self._get_selected_id()
        if machine_id is None:
            return
        machine = self._repo.find_by_id(machine_id)
        if machine:
            MachineDialog(self, title="Modifier la machine",
                         machine=machine, on_save=self._save_edit)

    def _save_new(self, machine: Machine):
        self._repo.insert(machine)
        self.refresh()

    def _save_edit(self, machine: Machine):
        self._repo.update(machine)
        self.refresh()

    def _delete_selected(self):
        machine_id = self._get_selected_id()
        if machine_id is None:
            return
        if messagebox.askyesno("Confirmation",
                               "Supprimer cette machine ? Les affectations associées seront également supprimées."):
            self._repo.delete(machine_id)
            self.refresh()


class MachineDialog(tk.Toplevel):
    """Dialogue pour ajouter ou modifier une machine."""

    def __init__(self, parent, title: str, on_save, machine: Machine = None):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()  # Fenêtre modale
        self._on_save = on_save
        self._machine = machine
        self._build_form()
        self._center()

    def _center(self):
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - 250
        y = self.winfo_screenheight() // 2 - 200
        self.geometry(f"500x350+{x}+{y}")

    def _build_form(self):
        """Construit le formulaire de saisie."""
        tk.Label(self, text="Nom *", bg=BG, fg=FG, font=FONT).grid(row=0, column=0, padx=20, pady=10, sticky="w")
        tk.Label(self, text="Adresse IP *", bg=BG, fg=FG, font=FONT).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        tk.Label(self, text="Système d'exploitation *", bg=BG, fg=FG, font=FONT).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        tk.Label(self, text="Description", bg=BG, fg=FG, font=FONT).grid(row=3, column=0, padx=20, pady=10, sticky="w")

        self._name_var = tk.StringVar()
        self._ip_var   = tk.StringVar()
        self._os_var   = tk.StringVar()
        self._desc_var = tk.StringVar()

        tk.Entry(self, textvariable=self._name_var, width=30, bg=BG2, fg=FG,
                 insertbackground=FG, relief="flat").grid(row=0, column=1, padx=20, pady=10)
        tk.Entry(self, textvariable=self._ip_var,   width=30, bg=BG2, fg=FG,
                 insertbackground=FG, relief="flat").grid(row=1, column=1, padx=20, pady=10)

        os_options = ["Windows 10", "Windows 11", "Windows Server 2022",
                      "Ubuntu 22.04", "Debian 12", "CentOS 7", "macOS 14", "Autre"]
        os_menu = ttk.Combobox(self, textvariable=self._os_var, values=os_options, width=28)
        os_menu.grid(row=2, column=1, padx=20, pady=10)

        tk.Entry(self, textvariable=self._desc_var, width=30, bg=BG2, fg=FG,
                 insertbackground=FG, relief="flat").grid(row=3, column=1, padx=20, pady=10)

        # Préremplissage si modification
        if self._machine:
            self._name_var.set(self._machine.name)
            self._ip_var.set(self._machine.ip_address)
            self._os_var.set(self._machine.os)
            self._desc_var.set(self._machine.description)

        tk.Label(self, text="* Champs obligatoires", bg=BG, fg="#6c7086",
                 font=("Helvetica", 8)).grid(row=4, column=0, columnspan=2, pady=5)

        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="💾 Enregistrer", command=self._save,
                  bg=GREEN, fg="#1e1e2e", font=("Helvetica", 10, "bold"),
                  relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=10)
        tk.Button(btn_frame, text="Annuler", command=self.destroy,
                  bg=BG2, fg=FG, font=FONT, relief="flat",
                  padx=15, pady=6, cursor="hand2").pack(side="left", padx=10)

    def _save(self):
        """Valide et sauvegarde la machine."""
        try:
            machine = Machine(
                name=self._name_var.get(),
                ip_address=self._ip_var.get(),
                os=self._os_var.get(),
                description=self._desc_var.get(),
                machine_id=self._machine.id if self._machine else None
            )
            if not machine.validate():
                messagebox.showerror("Erreur", "Données invalides. Vérifiez tous les champs obligatoires.")
                return
            self._on_save(machine)
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Erreur de validation", str(e))
