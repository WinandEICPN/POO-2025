
# Classe qui représente un ravitaillement automatique du stock.
# Quand le stock d'une crypto descend trop bas on enregistre un restock.
# Hérite de EntiteBase (la classe abstraite).

from datetime import datetime
from entite_base import EntiteBase

# classe represente un restockage automatique qui se déclanche qui on a atteint la limite pour le restock
class Restock(EntiteBase):

    def __init__(self, id_ravitaillement, quantite_ajoutee, id_crypto, date_ravitaillement=None):
        # Attributs privés
        self.__id_ravitaillement = id_ravitaillement
        self.__quantite_ajoutee  = quantite_ajoutee
        self.__id_crypto         = id_crypto

 # Si aucune date n'est fournie on prend la date et l'heure actuelles
        if date_ravitaillement is None:
            self.__date_ravitaillement = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.__date_ravitaillement = date_ravitaillement

# les methodes getter java style

    def get_id_ravitaillement(self):
        return self.__id_ravitaillement

    def get_quantite_ajoutee(self):
        return self.__quantite_ajoutee

    def get_id_crypto(self):
        return self.__id_crypto

    def get_date_ravitaillement(self):
        return self.__date_ravitaillement

#  Méthodes abstraites de la classe mere  EntiteBase 

    def valider(self):
        return self.__quantite_ajoutee > 0

    def afficher(self):
        return ("[" + self.__date_ravitaillement + "] Restock crypto #"
                + str(self.__id_crypto) + " : +"
                + str(self.__quantite_ajoutee) + " unités")

    def to_dict(self):
        return {
            "id_ravitaillement":   self.__id_ravitaillement,
            "quantite_ajoutee":    self.__quantite_ajoutee,
            "id_crypto":           self.__id_crypto,
            "date_ravitaillement": self.__date_ravitaillement
        }

    def __str__(self):
        return self.afficher()
