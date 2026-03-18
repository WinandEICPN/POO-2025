"""
Frame de gestion des vulnérabilités.
créer, modifier, supprimer et visualiser les vulnérabilités.

Une vulnérabilité est une fiche de référence pure (type, criticité, description).
Le statut et la date de correction sont gérés dans l'onglet Affectations.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from models.network_vulnerability import NetworkVulnerability
from models.system_vulnerability import SystemVulnerability
from models.application_vulnerability import ApplicationVulnerability
from models.vulnerability import Vulnerability
from repositories.vulnerability_repository import VulnerabilityRepository

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


class VulnerabilitiesFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self._repo = VulnerabilityRepository()
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        toolbar = tk.Frame(self, bg=BG, pady=8)
        toolbar.pack(fill="x", padx=10)

        tk.Label(toolbar, text="Gestion des vulnérabilités",
                 font=("Helvetica", 13, "bold"), bg=BG, fg=FG).pack(side="left")

        btn_frame = tk.Frame(toolbar, bg=BG)
        btn_frame.pack(side="right")

        tk.Button(btn_frame, text="↻", command=self.refresh,
                  bg=BG2, fg=FG, font=FONT, relief="flat", padx=6, cursor="hand2").pack(side="left", padx=5)
        self._btn(btn_frame, "＋ Ajouter",  GREEN,  self._open_add_dialog).pack(side="left", padx=4)
        self._btn(btn_frame, "✏ Modifier",  ACCENT, self._open_edit_dialog).pack(side="left", padx=4)
        self._btn(btn_frame, "✕ Supprimer", RED,    self._delete_selected).pack(side="left", padx=4)

        cols = ("ID", "Type", "Titre", "CVE", "Criticité", "Date découverte", "Action recommandée")
        self._tree = ttk.Treeview(self, columns=cols, show="headings", style="Custom.Treeview")
        self._style_tree()

        for col in cols:
            self._tree.heading(col, text=col)

        self._tree.column("ID",                 width=40,  anchor="center")
        self._tree.column("Type",               width=90,  anchor="center")
        self._tree.column("Titre",              width=200)
        self._tree.column("CVE",                width=110, anchor="center")
        self._tree.column("Criticité",          width=80,  anchor="center")
        self._tree.column("Date découverte",    width=110, anchor="center")
        self._tree.column("Action recommandée", width=320)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=5)
        scrollbar.pack(side="right", fill="y", pady=5, padx=(0, 10))

        self._tree.bind("<Double-1>", lambda e: self._open_edit_dialog())

    def _style_tree(self):
        style = ttk.Style()
        style.configure("Custom.Treeview",
                        background=BG2, foreground=FG,
                        fieldbackground=BG2, rowheight=28, font=FONT)
        style.configure("Custom.Treeview.Heading",
                        background="#11111b", foreground=ACCENT,
                        font=("Helvetica", 10, "bold"))
        style.map("Custom.Treeview", background=[("selected", "#45475a")])

    def _btn(self, parent, text, color, command):
        return tk.Button(parent, text=text, command=command,
                         bg=color, fg="#1e1e2e", font=("Helvetica", 9, "bold"),
                         relief="flat", padx=10, pady=5, cursor="hand2")

    def refresh(self):
        for row in self._tree.get_children():
            self._tree.delete(row)

        for vuln in self._repo.find_all():
            color = CRITICALITY_COLORS.get(vuln.criticality, FG)
            tag = vuln.criticality.replace("é", "e").replace("É", "E")
            self._tree.insert("", "end", tags=(tag,), values=(
                vuln.id,
                vuln.get_type_label(),
                vuln.title,
                vuln.cve_id or "-",
                vuln.criticality,
                vuln.discovery_date,
                vuln.get_recommended_action()
            ))
            self._tree.tag_configure(tag, foreground=color)

    def _get_selected_id(self):
        selected = self._tree.selection()
        if not selected:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner une vulnérabilité.")
            return None
        return int(self._tree.item(selected[0])["values"][0])

    def _open_add_dialog(self):
        VulnerabilityDialog(self, title="Ajouter une vulnérabilité", on_save=self._save_new)

    def _open_edit_dialog(self):
        vuln_id = self._get_selected_id()
        if vuln_id is None:
            return
        vuln = self._repo.find_by_id(vuln_id)
        if vuln:
            VulnerabilityDialog(self, title="Modifier la vulnérabilité",
                                vuln=vuln, on_save=self._save_edit)

    def _save_new(self, vuln: Vulnerability):
        self._repo.insert(vuln)
        self.refresh()

    def _save_edit(self, vuln: Vulnerability):
        self._repo.update(vuln)
        self.refresh()

    def _delete_selected(self):
        vuln_id = self._get_selected_id()
        if vuln_id is None:
            return
        if messagebox.askyesno("Confirmation",
                               "Supprimer cette vulnérabilité ? Les affectations associées seront également supprimées."):
            self._repo.delete(vuln_id)
            self.refresh()


class VulnerabilityDialog(tk.Toplevel):
    """
    Dialogue pour ajouter/modifier une vulnérabilité.
    Contient uniquement les champs de la fiche de référence :
    type, titre, description, CVE, criticité et champs spécifiques au type.
    """

    def __init__(self, parent, title: str, on_save, vuln: Vulnerability = None):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()
        self._on_save = on_save
        self._vuln = vuln
        self._build_form()
        self._center()

    def _center(self):
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - 280
        y = self.winfo_screenheight() // 2 - 220
        self.geometry(f"560x490+{x}+{y}")

    def _build_form(self):
        self._type_var        = tk.StringVar(value="Réseau")
        self._title_var       = tk.StringVar()
        self._desc_var        = tk.StringVar()
        self._cve_var         = tk.StringVar()
        self._criticality_var = tk.StringVar(value="Moyen")
        self._extra1_var      = tk.StringVar()
        self._extra2_var      = tk.StringVar()

        row = 0

        tk.Label(self, text="Type *", bg=BG, fg=FG, font=FONT).grid(row=row, column=0, padx=20, pady=8, sticky="w")
        type_menu = ttk.Combobox(self, textvariable=self._type_var,
                                  values=["Réseau", "Système", "Applicatif"],
                                  state="readonly", width=30)
        type_menu.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        type_menu.bind("<<ComboboxSelected>>", self._update_extra_labels)
        row += 1

        tk.Label(self, text="Titre *", bg=BG, fg=FG, font=FONT).grid(row=row, column=0, padx=20, pady=8, sticky="w")
        tk.Entry(self, textvariable=self._title_var, width=32, bg=BG2, fg=FG,
                 insertbackground=FG, relief="flat").grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        tk.Label(self, text="Description", bg=BG, fg=FG, font=FONT).grid(row=row, column=0, padx=20, pady=8, sticky="w")
        self._desc_text = tk.Text(self, width=32, height=3, bg=BG2, fg=FG,
                                   insertbackground=FG, relief="flat")
        self._desc_text.grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        tk.Label(self, text="CVE ID", bg=BG, fg=FG, font=FONT).grid(row=row, column=0, padx=20, pady=8, sticky="w")
        tk.Entry(self, textvariable=self._cve_var, width=32, bg=BG2, fg=FG,
                 insertbackground=FG, relief="flat").grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        tk.Label(self, text="Criticité *", bg=BG, fg=FG, font=FONT).grid(row=row, column=0, padx=20, pady=8, sticky="w")
        ttk.Combobox(self, textvariable=self._criticality_var,
                     values=["Faible", "Moyen", "Élevé", "Critique"],
                     state="readonly", width=30).grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        # Champs dynamiques selon le type
        self._extra1_label = tk.Label(self, text="Port", bg=BG, fg=FG, font=FONT)
        self._extra1_label.grid(row=row, column=0, padx=20, pady=8, sticky="w")
        tk.Entry(self, textvariable=self._extra1_var, width=32, bg=BG2, fg=FG,
                 insertbackground=FG, relief="flat").grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        self._extra2_label = tk.Label(self, text="Protocole", bg=BG, fg=FG, font=FONT)
        self._extra2_label.grid(row=row, column=0, padx=20, pady=8, sticky="w")
        tk.Entry(self, textvariable=self._extra2_var, width=32, bg=BG2, fg=FG,
                 insertbackground=FG, relief="flat").grid(row=row, column=1, padx=20, pady=8, sticky="w")
        row += 1

        if self._vuln:
            self._type_var.set(self._vuln.get_type_label())
            self._title_var.set(self._vuln.title)
            self._desc_text.insert("1.0", self._vuln.description)
            self._cve_var.set(self._vuln.cve_id)
            self._criticality_var.set(self._vuln.criticality)
            d = self._vuln.to_dict()
            self._extra1_var.set(d.get("extra_field1", ""))
            self._extra2_var.set(d.get("extra_field2", ""))
            self._update_extra_labels()

        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="💾 Enregistrer", command=self._save,
                  bg=GREEN, fg="#1e1e2e", font=("Helvetica", 10, "bold"),
                  relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=10)
        tk.Button(btn_frame, text="Annuler", command=self.destroy,
                  bg=BG2, fg=FG, font=FONT, relief="flat",
                  padx=15, pady=6, cursor="hand2").pack(side="left", padx=10)

    def _update_extra_labels(self, event=None):
        t = self._type_var.get()
        if t == "Réseau":
            self._extra1_label.config(text="Port")
            self._extra2_label.config(text="Protocole")
        elif t == "Système":
            self._extra1_label.config(text="Composant affecté")
            self._extra2_label.config(text="")
        elif t == "Applicatif":
            self._extra1_label.config(text="Nom de l'application")
            self._extra2_label.config(text="")

    def _save(self):
        try:
            t            = self._type_var.get()
            title        = self._title_var.get()
            description  = self._desc_text.get("1.0", "end-1c")
            cve          = self._cve_var.get()
            criticality  = self._criticality_var.get()
            extra1       = self._extra1_var.get()
            extra2       = self._extra2_var.get()
            vuln_id      = self._vuln.id if self._vuln else None

            if t == "Réseau":
                port = int(extra1) if extra1.isdigit() else None
                vuln = NetworkVulnerability(title, description, cve, criticality,
                                            port=port, protocol=extra2, vuln_id=vuln_id)
            elif t == "Système":
                vuln = SystemVulnerability(title, description, cve, criticality,
                                           affected_component=extra1, vuln_id=vuln_id)
            else:
                vuln = ApplicationVulnerability(title, description, cve, criticality,
                                                application_name=extra1, vuln_id=vuln_id)

            if not vuln.validate():
                messagebox.showerror("Erreur", "Données invalides. Vérifiez les champs obligatoires.")
                return

            self._on_save(vuln)
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Erreur de validation", str(e))