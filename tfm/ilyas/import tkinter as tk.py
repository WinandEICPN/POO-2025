import tkinter as tk
from tkinter import messagebox
from models.client import Client
from models.voiture import Voiture
from models.location import Location
from database.init_db import create_tables
from service.client_service import ClientService
from service.vehicule_service import VehiculeService
from service.location_service import LocationService

# --- Initialisation de la base de données ---
create_tables()

# --- Services ---
client_service = ClientService()
vehicule_service = VehiculeService()
location_service = LocationService()

# --- Compte Admin ---
ADMIN_ACCOUNT = {"username": "admin", "password": "1234"}

# --- Current user ---
current_client = None

# --- Fenêtre principale ---
root = tk.Tk()
root.title("Location Voitures")
root.geometry("950x550")

# --- Frames ---
page_accueil = tk.Frame(root, bg="#dceefc")
page_inscription = tk.Frame(root, bg="#e6f7e6")
page_login_client = tk.Frame(root, bg="#fff3e6")
page_client = tk.Frame(root, bg="#f0fff0")
page_admin = tk.Frame(root, bg="#fff0f5")

for frame in (page_accueil, page_inscription, page_login_client, page_client, page_admin):
    frame.place(x=0, y=0, relwidth=1, relheight=1)

def show_frame(frame):
    frame.tkraise()

# ---------------- PAGE ACCUEIL ----------------
tk.Label(page_accueil, text="Bienvenue", font=("Arial", 18), bg="#dceefc").pack(pady=30)
tk.Button(page_accueil, text="Inscription Client", width=25, command=lambda: show_frame(page_inscription), bg="#b0c4de").pack(pady=10)
tk.Button(page_accueil, text="Connexion", width=25, command=lambda: show_frame(page_login_client), bg="#b0c4de").pack(pady=10)

# ---------------- PAGE INSCRIPTION CLIENT ----------------
tk.Label(page_inscription, text="Inscription Client", font=("Arial", 16), bg="#e6f7e6").pack(pady=20)
form_inscr = tk.Frame(page_inscription, bg="#e6f7e6")
form_inscr.pack(pady=10)

tk.Label(form_inscr, text="ID", bg="#e6f7e6").grid(row=0, column=0)
entry_id_inscr = tk.Entry(form_inscr)
entry_id_inscr.grid(row=0, column=1)

tk.Label(form_inscr, text="Nom", bg="#e6f7e6").grid(row=1, column=0)
entry_nom_inscr = tk.Entry(form_inscr)
entry_nom_inscr.grid(row=1, column=1)

tk.Label(form_inscr, text="Email", bg="#e6f7e6").grid(row=2, column=0)
entry_email_inscr = tk.Entry(form_inscr)
entry_email_inscr.grid(row=2, column=1)

tk.Label(form_inscr, text="Permis", bg="#e6f7e6").grid(row=3, column=0)
entry_permis_inscr = tk.Entry(form_inscr)
entry_permis_inscr.grid(row=3, column=1)

tk.Label(form_inscr, text="Mot de passe", bg="#e6f7e6").grid(row=4, column=0)
entry_password_inscr = tk.Entry(form_inscr, show="*")
entry_password_inscr.grid(row=4, column=1)

def inscrire_client():
    try:
        try:
            id_client = int(entry_id_inscr.get())
        except ValueError:
            messagebox.showerror("Erreur", "ID doit être un nombre")
            return

        nom = entry_nom_inscr.get()
        email = entry_email_inscr.get()
        permis = entry_permis_inscr.get()
        password = entry_password_inscr.get()
        if not nom or not email or not permis or not password:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
            return

        client = Client(id_client, nom, email, permis, password)
        client_service.ajouter_client(client)
        messagebox.showinfo("Succès", f"Client {nom} ajouté !")
        entry_id_inscr.delete(0, tk.END)
        entry_nom_inscr.delete(0, tk.END)
        entry_email_inscr.delete(0, tk.END)
        entry_permis_inscr.delete(0, tk.END)
        entry_password_inscr.delete(0, tk.END)
        show_frame(page_login_client)
    except Exception as e:
        # Affiche une erreur à l'utilisateur et logue l'erreur dans la console pour débogage.
        messagebox.showerror("Erreur", f"Impossible d\'ajouter le client: {e}")
        print("Erreur lors de l\'inscription du client:", e)
tk.Button(page_inscription, text="S'inscrire", command=inscrire_client, bg="#b0c4de").pack(pady=10)
tk.Button(page_inscription, text="Retour", command=lambda: show_frame(page_accueil), bg="#f08080").pack(pady=5)

# ---------------- PAGE LOGIN CLIENT ----------------
tk.Label(page_login_client, text="Connexion", font=("Arial", 16), bg="#fff3e6").pack(pady=20)
form_login = tk.Frame(page_login_client, bg="#fff3e6")
form_login.pack(pady=10)

tk.Label(form_login, text="Email", bg="#fff3e6").grid(row=0, column=0)
entry_login_email = tk.Entry(form_login)
entry_login_email.grid(row=0, column=1)

tk.Label(form_login, text="Mot de passe", bg="#fff3e6").grid(row=1, column=0)
entry_login_pass = tk.Entry(form_login, show="*")
entry_login_pass.grid(row=1, column=1)

def login():
    global current_client
    try:
        email = entry_login_email.get()
        passwd = entry_login_pass.get()
        # Admin
        if email == ADMIN_ACCOUNT["username"] and passwd == ADMIN_ACCOUNT["password"]:
            show_frame(page_admin)
            afficher_voitures_admin()
            return
        # Client
        found = None
        for c in client_service.liste_clients:
            if c.email == email and c.password == passwd:
                found = c
                break
        if found:
            current_client = found
            show_frame(page_client)
            afficher_voitures_client()
        else:
            messagebox.showerror("Erreur", "Email ou mot de passe incorrect")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la connexion : {e}")
        print("Erreur lors de la connexion :", e)

tk.Button(page_login_client, text="Se connecter", command=login, bg="#b0c4de").pack(pady=10)
tk.Button(page_login_client, text="Retour", command=lambda: show_frame(page_accueil), bg="#f08080").pack(pady=5)

# ---------------- PAGE CLIENT ----------------
tk.Label(page_client, text="Voitures disponibles", font=("Arial", 16), bg="#f0fff0").pack(pady=10)
list_voitures_client = tk.Listbox(page_client, width=70)
list_voitures_client.pack(pady=10)

tk.Label(page_client, text="Nombre de jours :", bg="#f0fff0").pack()
entry_nb_jours = tk.Entry(page_client)
entry_nb_jours.pack()

def afficher_voitures_client():
    list_voitures_client.delete(0, tk.END)
    for v in vehicule_service.liste_vehicules:
        list_voitures_client.insert(tk.END, f"{v.id} - {v.marque} {v.modele} ({v.immatriculation}) - {v.prix_par_jour}€/jour")

def reserver_voiture():
    try:
        sel = list_voitures_client.curselection()
        if not sel:
            messagebox.showerror("Erreur", "Sélectionnez une voiture")
            return
        index = sel[0]
        voiture = vehicule_service.liste_vehicules[index]
        try:
            nb_jours = int(entry_nb_jours.get())
        except ValueError:
            messagebox.showerror("Erreur", "Nombre de jours invalide")
            return
        client = current_client
        if not client:
            messagebox.showerror("Erreur", "Client introuvable")
            return
        location = Location(len(location_service.liste_locations) + 1, client, voiture, nb_jours)
        location_service.ajouter_location(location)
        messagebox.showinfo("Succès", f"Voiture {voiture.marque} {voiture.modele} réservée pour {nb_jours} jours !")
        entry_nb_jours.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de réserver : {e}")
        print("Erreur lors de la réservation :", e)

tk.Button(page_client, text="Réserver sélection", command=reserver_voiture, bg="#b0c4de").pack(pady=5)
tk.Button(page_client, text="Déconnexion", command=lambda: show_frame(page_accueil), bg="#f08080").pack(pady=10)

# ---------------- PAGE ADMIN ----------------
tk.Label(page_admin, text="Gestion Véhicules (Admin)", font=("Arial", 16), bg="#fff0f5").pack(pady=10)
form_admin = tk.Frame(page_admin, bg="#fff0f5")
form_admin.pack(pady=10)

tk.Label(form_admin, text="ID Véhicule", bg="#fff0f5").grid(row=0, column=0)
entry_id_voiture = tk.Entry(form_admin)
entry_id_voiture.grid(row=0, column=1)

tk.Label(form_admin, text="Marque", bg="#fff0f5").grid(row=1, column=0)
entry_marque_voiture = tk.Entry(form_admin)
entry_marque_voiture.grid(row=1, column=1)

tk.Label(form_admin, text="Modèle", bg="#fff0f5").grid(row=2, column=0)
entry_modele_voiture = tk.Entry(form_admin)
entry_modele_voiture.grid(row=2, column=1)

tk.Label(form_admin, text="Immatriculation", bg="#fff0f5").grid(row=3, column=0)
entry_immat_voiture = tk.Entry(form_admin)
entry_immat_voiture.grid(row=3, column=1)

tk.Label(form_admin, text="Prix/Jour", bg="#fff0f5").grid(row=4, column=0)
entry_prix_voiture = tk.Entry(form_admin)
entry_prix_voiture.grid(row=4, column=1)

tk.Label(form_admin, text="Nb Places", bg="#fff0f5").grid(row=5, column=0)
entry_places_voiture = tk.Entry(form_admin)
entry_places_voiture.grid(row=5, column=1)

list_voitures_admin = tk.Listbox(page_admin, width=70)
list_voitures_admin.pack(pady=10)

def afficher_voitures_admin():
    list_voitures_admin.delete(0, tk.END)
    for v in vehicule_service.liste_vehicules:
        list_voitures_admin.insert(tk.END, f"{v.id} - {v.marque} {v.modele} ({v.immatriculation}) - {v.prix_par_jour}€/jour")

def ajouter_voiture_admin():
    try:
        id_v = int(entry_id_voiture.get())
        prix = float(entry_prix_voiture.get())
        places = int(entry_places_voiture.get())
    except ValueError:
        messagebox.showerror("Erreur", "ID, prix ou places invalides")
        return
    marque = entry_marque_voiture.get()
    modele = entry_modele_voiture.get()
    immat = entry_immat_voiture.get()
    if not marque or not modele or not immat:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
        return
    v = Voiture(id_v, marque, modele, immat, prix, places)
    vehicule_service.ajouter_vehicule(v)
    afficher_voitures_admin()
    messagebox.showinfo("Succès", f"Voiture {marque} {modele} ajoutée !")

def supprimer_voiture_admin():
    sel = list_voitures_admin.curselection()
    if not sel:
        messagebox.showerror("Erreur", "Sélectionnez une voiture")
        return
    index = sel[0]
    vehicule = vehicule_service.liste_vehicules[index]
    vehicule_service.supprimer_vehicule(vehicule.id)
    afficher_voitures_admin()

tk.Button(form_admin, text="Ajouter Véhicule", command=ajouter_voiture_admin, bg="#b0c4de").grid(row=6, column=0, columnspan=2, pady=5)
tk.Button(page_admin, text="Supprimer Véhicule sélectionné", command=supprimer_voiture_admin, bg="#f08080").pack(pady=5)
tk.Button(page_admin, text="Déconnexion", command=lambda: show_frame(page_accueil), bg="#f08080").pack(pady=10)

# --- Lancer la page accueil ---
show_frame(page_accueil)
root.mainloop()
