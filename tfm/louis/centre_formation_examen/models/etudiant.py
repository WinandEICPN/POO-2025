from models.personne import Personne

"""
Import de la classe Personne depuis le module models.
Elle sert de classe parent pour les différents types de personnes
du système (Etudiant, Formateur)
"""

class Etudiant(Personne):
    
    """
    Classe métier représentant un étudiant du centre de formation.
    Elle récupère ses attibuts grace à la classe personne.
    Cette classe est utilisée pour manipuler les données d'un étudiant
    dans l'application avant leur enregistrement en base de données.
    """
    
    # Étudiant hérite de Personne.
    
    def save(self):
        pass
    
    # methode pour enregister un étudiant et géré par la classe DAO.

    def delete(self):
        pass
    
    # pareil ici pour supprimer.