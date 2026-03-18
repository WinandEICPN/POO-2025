# Import des classes DAO qui gèrent l'accès à la base de données
# Chaque DAO est responsable d'une table spécifique
from dao.etudiantDAO import EtudiantDAO
from dao.formateurDAO import FormateurDAO
from dao.coursDAO import CoursDAO
from dao.inscriptionDAO import InscriptionDAO

# Import des classes métier représentant les objets manipulés dans l'application
from models.etudiant import Etudiant
from models.formateur import Formateur
from models.cours import Cours

class CentreManager:
    """
    Manager central pour toute la logique métier de l'application.

    Cette classe agit comme intermédiaire entre :
    - l'interface graphique (UI)
    - les DAO (accès à la base de données)

    Elle gère :
    - la validation des données
    - les règles métier
    - les opérations d'inscription
    """

    def __init__(self):
        
        # Création des DAO utilisés dans le système.
        # Chaque DAO correspond à une table de la base de données.
        
        self.etudiantDAO = EtudiantDAO()
        self.formateurDAO = FormateurDAO()
        self.coursDAO = CoursDAO()
        self.inscriptionDAO = InscriptionDAO()

    # Gestion des etudiants
    def ajouter_etudiant(self, nom, email):
        
        # Vérifier que les champs ne sont pas vides.
        if not nom.strip() or not email.strip():
            raise ValueError("Tous les champs sont obligatoires")
         
        if "@" not in email:
            raise ValueError("Email invalide")
        
        # Pour vérifier qu'il n'y a pas de doublon.
        # ça parcourt la liste existante.
        for e in self.get_etudiants():
            if e[1].lower() == nom.strip().lower() and e[2].lower() == email.strip().lower():
                raise ValueError("Cet étudiant existe déjà")
            
        # Création de l'objet métier etudiant.
        etu = Etudiant(nom,email)
        
        # faire appelle du DAO pour enregistrer l'étudiant.
        self.etudiantDAO.insert(etu)

    def get_etudiants(self):
        return self.etudiantDAO.get_all()

    def supprimer_etudiant(self, etu_id):
        self.etudiantDAO.delete(etu_id)

        # Formateurs 
    def ajouter_formateur(self, nom, email):
        if not nom.strip() or not email.strip():
            raise ValueError("Tous les champs sont obligatoires")
        if "@" not in email:
            raise ValueError("Email invalide")
        
        for f in self.get_formateurs():
            if f[1].lower() == nom.strip().lower() and f[2].lower() == email.strip().lower():
                raise ValueError("Ce formateur existe déjà")
        form = Formateur(nom,email)
        self.formateurDAO.insert(form)

    def get_formateurs(self):
        return self.formateurDAO.get_all()

    def supprimer_formateur(self, f_id):
        self.formateurDAO.delete(f_id)

        # Cours
    def creer_cours(self, titre, duree, formateur_id):
        if not titre.strip():
            raise ValueError("Titre obligatoire")
        if titre.strip().isdigit():
            raise ValueError("Titre ne peut pas être un chiffre")
        if not str(duree).isdigit() or int(duree) <=0:
            raise ValueError("Durée invalide")
        
        for c in self.get_cours():
            if c[1].lower() == titre.strip().lower() and c[3]==formateur_id:
                raise ValueError("Ce cours existe déjà pour ce formateur")
        cours = Cours(titre,int(duree),formateur_id)
        self.coursDAO.insert(cours)

    def get_cours(self):
        return self.coursDAO.get_all()

    def supprimer_cours(self, c_id):
        self.coursDAO.delete(c_id)

    # Inscriptions
    def inscrire(self, etudiant_id, cours_id):
        for insc in self.inscriptionDAO.get_all():
    # Vérif qu'un étudiant ne s'inscrit pas 2x au même cours
            if insc[1] == etudiant_id and insc[2] == cours_id:
                raise ValueError("Cet étudiant est déjà inscrit à ce cours")
        self.inscriptionDAO.insert(etudiant_id,cours_id)

    def get_inscriptions_details(self):
        
        """
        renvoie liste de tuples : (Cours, Durée, Formateur, Étudiant, Email) 
        (structure de données qui stocke une collection ordonnée d'éléments, similaire à une liste, mais immuable) 
        ( = non modifiable après sa création)
        """
        data = []
        inscriptions = self.inscriptionDAO.get_all()
        
        # Création de dictionnaires pour accèder aux données.
        etudiants = {e[0]:(e[1],e[2]) for e in self.get_etudiants()}
        cours = {c[0]:c for c in self.get_cours()}
        formateurs = {f[0]:f[1] for f in self.get_formateurs()}
        
        # Parcours des inscriptions
        for insc in inscriptions:
            etu_id, cours_id = insc[1], insc[2]
            if etu_id not in etudiants or cours_id not in cours:
                continue
            c = cours[cours_id]
            f_nom = formateurs.get(c[3],"Inconnu")
            e_nom, e_email = etudiants[etu_id]
            data.append((c[1],c[2],f_nom,e_nom,e_email))
        return data