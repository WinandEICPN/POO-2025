import tkinter as tk
from tkinter import ttk

class InscriptionsRecapUI:
    #Tableau récapitulatif des inscriptions
    def __init__(self, manager):
        self.manager = manager
        self.window = tk.Toplevel()
        self.window.title("Récap inscriptions")
        self.window.geometry("1020x800")
        self.window.configure(bg="#f0f4f7")

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        columns = ("Cours","Durée","Formateur","Étudiant","Email")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=20, fill="both", expand=True)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for rec in self.manager.get_inscriptions_details():
            self.tree.insert("", "end", values=rec)