from db import Database

db = Database()


def ajouter_livre(titre):
    return db.ajouter_livre(titre)


def supprimer_livre(titre):
    return db.supprimer_livre(titre)


def afficher_livres():
    return db.get_livres()


def emprunter_livre(titre_livre, nom_utilisateur, duree_jours):
    return db.emprunter_livre(titre_livre, nom_utilisateur, duree_jours)


def rendre_livre(titre_livre, nom_utilisateur):
    return db.rendre_livre(titre_livre, nom_utilisateur)


def afficher_emprunts_actifs():
    return db.get_emprunts_actifs()
