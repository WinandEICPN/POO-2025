from db import Database

db = Database()


def ajouter_utilisateur(nom):
    return db.ajouter_utilisateur(nom)


def afficher_utilisateurs():
    return db.get_utilisateurs()


def utilisateur_existe(nom):
    return db.utilisateur_existe(nom)


def modifier_utilisateur(ancien_nom, nouveau_nom):
    return db.modifier_utilisateur(ancien_nom, nouveau_nom)


def supprimer_utilisateur(nom):
    return db.supprimer_utilisateur(nom)
