
# représente une opération d'achat ou de vente.
# Hérite de EntiteBase (classe abstraite).

from datetime import datetime
from entite_base import EntiteBase

# Représente un achat ou une vente de cryptomonnaie sur la plateforme
class Transaction(EntiteBase):

    # Les deux types d'opérations possibles (variables de classe)
    TYPE_ACHAT = "ACHAT_USER"
    TYPE_VENTE = "VENTE_USER"

    def __init__(self, id_transaction, type_action, quantite_echangee, montant_total_usd, id_crypto, date_heure=None):
        # Attributs privés
        self.__id_transaction   = id_transaction
        self.__type_action      = type_action
        self.__quantite_echangee = quantite_echangee
        self.__montant_total_usd = montant_total_usd
        self.__id_crypto        = id_crypto

        # Si aucune date n'est fournie, on prend la date et l'heure actuelles
        if date_heure is None:
            self.__date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.__date_heure = date_heure

    # methode getter

    def get_id_transaction(self):
        return self.__id_transaction

    def get_type_action(self):
        return self.__type_action

    def get_quantite_echangee(self):
        return self.__quantite_echangee

    def get_montant_total_usd(self):
        return self.__montant_total_usd

    def get_id_crypto(self):
        return self.__id_crypto

    def get_date_heure(self):
        return self.__date_heure

    # Méthodes abstraites imposées par EntiteBase

    def valider(self):
        if self.__type_action not in (self.TYPE_ACHAT, self.TYPE_VENTE):
            return False
        if self.__quantite_echangee <= 0:
            return False
        if self.__montant_total_usd <= 0:
            return False
        return True

    def afficher(self):
        if self.__type_action == self.TYPE_ACHAT:
            action = "Achat"
        else:
            action = "Vente"
        return ("[" + self.__date_heure + "] " + action
                + " | Qté : " + str(self.__quantite_echangee)
                + " | Montant : " + str(self.__montant_total_usd) + " USD")

    def to_dict(self):
        return {
            "id_transaction":    self.__id_transaction,
            "type_action":       self.__type_action,
            "quantite_echangee": self.__quantite_echangee,
            "montant_total_usd": self.__montant_total_usd,
            "id_crypto":         self.__id_crypto,
            "date_heure":        self.__date_heure
        }

    def __str__(self):
        return self.afficher()
