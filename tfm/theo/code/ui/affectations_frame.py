"""
Frame affectation.
toutes les affectations de toutes les machines sont affichées.
Le statut et la date de correction sont propres à chaque affectation.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from repositories.machine_repository import MachineRepository
from repositories.vulnerability_repository import VulnerabilityRepository
from repositories.affectation_repository import AffectationRepository

BG = "#1e1e2e"
BG2 = "#313244"
FG = "#cdd6f4"
ACCENT = "#89b4fa"
RED = "#f38ba8"
GREEN = "#a6e3a1"
FONT = ("Helvetica", 10)

CRITICALITY_COLORS = {
    "Critique": "#f38ba8",
    "Élevé":    "#fab387",
    "Moyen":    "#f9e2af",
    "Faible":   "#a6e3a1"
}


class AffectationsFrame(tk.Frame):

    def __init__(self, parent, refresh_machines_cb=None, refresh_vulns_cb=None):
        super().__init__(parent, bg=BG)
        self._machine_repo  = MachineRepository()
        self._vuln_repo     = VulnerabilityRepository()
        self._affect_repo   = AffectationRepository()
        self._sort_by       = tk.StringVar(value="criticality")
        self._build_ui()

    def _build_ui(self):
        # Barre d'outils
        toolbar = tk.Frame(self, bg=BG, pady=8)
        toolbar.pack(fill="x", padx=10)

        tk.Label(toolbar, text="Gestion des affectations",
                 font=("Helvetica", 13, "bold"), bg=BG, fg=FG).pack(side="left")

        btn_frame = tk.Frame(toolbar, bg=BG)
        btn_frame.pack(side="right")

        tk.Label(btn_frame, text="Trier par :", bg=BG, fg=FG, font=FONT).pack(side="left", padx=5)
        ttk.Combobox(btn_frame, textvariable=self._sort_by,
                     values=["criticality", "status", "machine"],
                     state="readonly", width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="↻", command=self.refresh,
                  bg=BG2, fg=FG, font=FONT, relief="flat", padx=6, cursor="hand2").pack(side="left", padx=5)

        tk.Button(btn_frame, text="＋ Affecter",
                  command=self._open_assign_dialog,
                  bg=GREEN, fg="#1e1e2e", font=("Helvetica", 9, "bold"),
                  relief="flat", padx=10, pady=5, cursor="hand2").pack(side="left", padx=4)
        tk.Button(btn_frame, text="✓ Marquer Terminé",
                  command=self._mark_as_done,
                  bg=ACCENT, fg="#1e1e2e", font=("Helvetica", 9, "bold"),
                  relief="flat", padx=10, pady=5, cursor="hand2").pack(side="left", padx=4)
        tk.Button(btn_frame, text="✕ Retirer",
                  command=self._unassign_selected,
                  bg=RED, fg="#1e1e2e", font=("Helvetica", 9, "bold"),
                  relief="flat", padx=10, pady=5, cursor="hand2").pack(side="left", padx=4)

        # Tableau
        cols = ("Machine", "IP", "Type", "Titre", "CVE",
                "Criticité", "Statut", "Date affectation", "Date correction")
        self._tree = ttk.Treeview(self, columns=cols, show="headings", style="Custom.Treeview")
        self._style_tree()

        for col in cols:
            self._tree.heading(col, text=col)

        self._tree.column("Machine",          width=130)
        self._tree.column("IP",               width=110, anchor="center")
        self._tree.column("Type",             width=80,  anchor="center")
        self._tree.column("Titre",            width=180)
        self._tree.column("CVE",              width=100, anchor="center")
        self._tree.column("Criticité",        width=75,  anchor="center")
        self._tree.column("Statut",           width=90,  anchor="center")
        self._tree.column("Date affectation", width=110, anchor="center")
        self._tree.column("Date correction",  width=110, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=5)
        scrollbar.pack(side="right", fill="y", pady=5, padx=(0, 10))

        self.refresh()

    def _style_tree(self):
        style = ttk.Style()
        style.configure("Custom.Treeview",
                        background=BG2, foreground=FG,
                        fieldbackground=BG2, rowheight=28, font=FONT)
        style.configure("Custom.Treeview.Heading",
                        background="#11111b", foreground=ACCENT,
                        font=("Helvetica", 10, "bold"))
        style.map("Custom.Treeview", background=[("selected", "#45475a")])

    def refresh(self):
        """Recharge toutes les affectations."""
        for row in self._tree.get_children():
            self._tree.delete(row)

        affectations = self._affect_repo.find_all(sort_by=self._sort_by.get())

        for a in affectations:
            color_tag = a["criticality"].replace("é", "e").replace("É", "E")
            self._tree.insert("", "end", tags=(color_tag,), values=(
                a["machine_name"],
                a["ip_address"],
                a["type"],
                a["title"],
                a["cve_id"] or "-",
                a["criticality"],
                a["status"],
                a["assigned_date"],
                a["fix_date"] or "-"
            ))
            self._tree.tag_configure(
                color_tag, foreground=CRITICALITY_COLORS.get(a["criticality"], FG)
            )

    def _get_selected(self):
        """Retourne (machine_name, vuln_title, machine_id, vuln_id) depuis la ligne sélectionnée."""
        selected = self._tree.selection()
        if not selected:
            messagebox.showwarning("Sélection requise",
                                   "Veuillez sélectionner une affectation dans la liste.")
            return None
        values = self._tree.item(selected[0])["values"]
        machine_name = values[0]
        ip           = values[1]
        vuln_title   = values[3]

        # Retrouve les IDs depuis les repos
        machine = next((m for m in self._machine_repo.find_all()
                        if m.name == machine_name and m.ip_address == ip), None)
        vuln    = next((v for v in self._vuln_repo.find_all()
                        if v.title == vuln_title), None)

        if not machine or not vuln:
            messagebox.showerror("Erreur", "Impossible de retrouver les IDs.")
            return None

        return machine.id, vuln.id, vuln_title

    def _open_assign_dialog(self):
        AssignDialog(self,
                     machine_repo=self._machine_repo,
                     vuln_repo=self._vuln_repo,
                     affect_repo=self._affect_repo,
                     on_done=self.refresh)

    def _mark_as_done(self):
        result = self._get_selected()
        if not result:
            return
        machine_id, vuln_id, titre = result

        info = self._affect_repo.get_affectation_info(machine_id, vuln_id)
        if info.get("status") == "Terminé":
            messagebox.showinfo("Info", "Cette affectation est déjà marquée comme Terminée.")
            return

        today = datetime.now().strftime("%Y-%m-%d")
        self._affect_repo.update_status(machine_id, vuln_id, status="Terminé", fix_date=today)
        self.refresh()
        messagebox.showinfo("Succès",
                            f"Affectation '{titre}' marquée Terminée ✅\n"
                            f"La vulnérabilité reste disponible pour d'autres machines.")

    def _unassign_selected(self):
        result = self._get_selected()
        if not result:
            return
        machine_id, vuln_id, titre = result
        if messagebox.askyesno("Confirmation",
                               f"Retirer '{titre}' de cette machine ?"):
            self._affect_repo.unassign(machine_id, vuln_id)
            self.refresh()


class AssignDialog(tk.Toplevel):
    """
    Dialogue pour affecter une vulnérabilité à une machine.
    Deux dropdowns, machine + vulnérabilité.
    """

    def __init__(self, parent, machine_repo, vuln_repo, affect_repo, on_done):
        super().__init__(parent)
        self.title("Affecter une vulnérabilité")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()
        self._machine_repo = machine_repo
        self._vuln_repo    = vuln_repo
        self._affect_repo  = affect_repo
        self._on_done      = on_done
        self._build_ui()
        self._center()

    def _center(self):
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - 230
        y = self.winfo_screenheight() // 2 - 100
        self.geometry(f"460x220+{x}+{y}")

    def _build_ui(self):
        tk.Label(self, text="Machine :", bg=BG, fg=FG,
                 font=("Helvetica", 11, "bold")).grid(row=0, column=0, padx=20, pady=15, sticky="w")
        tk.Label(self, text="Vulnérabilité :", bg=BG, fg=FG,
                 font=("Helvetica", 11, "bold")).grid(row=1, column=0, padx=20, pady=15, sticky="w")

        # Machines
        machines = self._machine_repo.find_all()
        self._machine_map = {f"{m.name} ({m.ip_address})": m.id for m in machines}
        self._machine_var = tk.StringVar()
        ttk.Combobox(self, textvariable=self._machine_var,
                     values=list(self._machine_map.keys()),
                     state="readonly", width=30).grid(row=0, column=1, padx=20, pady=15)

        # Vulnérabilités
        vulns = self._vuln_repo.find_all()
        self._vuln_map = {f"{v.title} [{v.get_type_label()} — {v.criticality}]": v.id for v in vulns}
        self._vuln_var = tk.StringVar()
        ttk.Combobox(self, textvariable=self._vuln_var,
                     values=list(self._vuln_map.keys()),
                     state="readonly", width=30).grid(row=1, column=1, padx=20, pady=15)

        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)
        tk.Button(btn_frame, text="✔ Affecter", command=self._assign,
                  bg=GREEN, fg="#1e1e2e", font=("Helvetica", 10, "bold"),
                  relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=10)
        tk.Button(btn_frame, text="Annuler", command=self.destroy,
                  bg=BG2, fg=FG, font=FONT, relief="flat",
                  padx=15, pady=6, cursor="hand2").pack(side="left", padx=10)

    def _assign(self):
        machine_key = self._machine_var.get()
        vuln_key    = self._vuln_var.get()

        if not machine_key or not vuln_key:
            messagebox.showwarning("Champs requis",
                                   "Veuillez sélectionner une machine et une vulnérabilité.")
            return

        machine_id = self._machine_map[machine_key]
        vuln_id    = self._vuln_map[vuln_key]

        if self._affect_repo.assign(machine_id, vuln_id):
            messagebox.showinfo("Succès", "Vulnérabilité affectée avec succès ✅")
            self._on_done()
            self.destroy()
        else:
            messagebox.showerror("Erreur",
                                 "Cette vulnérabilité est déjà affectée à cette machine.")