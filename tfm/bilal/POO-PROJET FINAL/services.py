# services.py
# Classe qui contient toute la logique métier de l'application.
# C'est ici qu'on vérifie les règles (stock suffisant, seuil de restock, etc.)
# Elle utilise les classes Access pour accéder à la base de données.
# La gestion des exceptions suit le cours "Gestion des exceptions en Python".

from cryptomonnaie import QUANTITE_RECHARGE, STOCK_MAX_RACHAT
from crypto_access import CryptoAccess
from transaction_access import TransactionAccess
from restock_access import RestockAccess


class CryptoService:
    """Gère toute la logique métier : achat, vente, restock automatique, historique."""

    def __init__(self):
        # On crée les objets d'accès qui vont communiquer avec la base de données
        self.__crypto_access      = CryptoAccess()
        self.__transaction_access = TransactionAccess()
        self.__restock_access     = RestockAccess()

    # --- Consultation ---

    def lister_cryptos(self):
        """Retourne la liste de toutes les cryptomonnaies."""
        return self.__crypto_access.get_all()

    def get_crypto(self, id_crypto):
        """Retourne une cryptomonnaie par son id. Lève une erreur si elle n'existe pas."""
        crypto = self.__crypto_access.get_by_id(id_crypto)
        if crypto is None:
            raise ValueError("Cryptomonnaie introuvable.")
        return crypto

    def compteur_transactions(self):
        """Retourne le nombre total de transactions enregistrées."""
        return self.__transaction_access.compter_total()

    # --- Achat (l'utilisateur achète à la plateforme) ---

    def acheter(self, id_crypto, quantite):
        """
        L'utilisateur achète une quantité de crypto.
        La plateforme vérifie le stock avant de valider.
        Lève ValueError si la quantité est invalide ou le stock insuffisant.
        """
        # Validation de base : la quantité doit être positive
        if quantite <= 0:
            raise ValueError("La quantité doit être positive.")

        # On récupère la crypto depuis la base de données
        try:
            crypto = self.get_crypto(id_crypto)
        except ValueError:
            raise ValueError("Cryptomonnaie introuvable.")

        # Vérification : est-ce qu'on a assez de stock ?
        if not crypto.peut_vendre_a_user(quantite):
            raise ValueError(
                "Stock insuffisant. Disponible : "
                + str(crypto.get_quantite_stock()) + " " + crypto.get_symbole() + "."
            )

        # Calcul du montant total
        montant = quantite * crypto.get_prix_unitaire()

        # On retire la quantité du stock (dans l'objet en mémoire)
        crypto.debiter_stock(quantite)

        # On sauvegarde le nouveau stock en base de données
        self.__crypto_access.update_stock(crypto.get_id_crypto(), crypto.get_quantite_stock())

        # On enregistre la transaction dans la base
        id_tx = self.__transaction_access.enregistrer(
            "ACHAT_USER", quantite, montant, crypto.get_id_crypto()
        )

        # On vérifie si un restock automatique est nécessaire
        info_restock = None
        if crypto.necessite_recharge():
            info_restock = self.__effectuer_restock(crypto)

        # On retourne un dictionnaire avec le résultat de l'opération
        return {
            "succes":           True,
            "type":             "ACHAT_USER",
            "crypto":           crypto.get_symbole(),
            "quantite":         quantite,
            "montant_usd":      montant,
            "stock_restant":    crypto.get_quantite_stock(),
            "id_transaction":   id_tx,
            "restock_effectue": info_restock
        }

    # --- Vente (l'utilisateur vend à la plateforme) ---

    def vendre(self, id_crypto, quantite):
        """
        L'utilisateur vend une quantité de crypto à la plateforme.
        La plateforme vérifie qu'elle ne dépasse pas son stock maximum.
        Lève ValueError si la quantité est invalide ou le stock maximum déjà atteint.
        """
        if quantite <= 0:
            raise ValueError("La quantité doit être positive.")

        try:
            crypto = self.get_crypto(id_crypto)
        except ValueError:
            raise ValueError("Cryptomonnaie introuvable.")

        # Calcul du maximum que la plateforme peut racheter
        max_rachetable = crypto.quantite_rachetable()

        if max_rachetable <= 0:
            raise ValueError(
                "La plateforme ne peut plus racheter de " + crypto.get_symbole()
                + " (stock maximum de " + str(STOCK_MAX_RACHAT) + " atteint)."
            )

        # Vérification : est-ce que la quantité demandée est acceptable ?
        if not crypto.peut_racheter_a_user(quantite):
            raise ValueError(
                "La plateforme ne peut racheter que "
                + str(max_rachetable) + " " + crypto.get_symbole()
                + " (limite de stock : " + str(STOCK_MAX_RACHAT) + ")."
            )

        # Calcul du montant total
        montant = quantite * crypto.get_prix_unitaire()

        # On ajoute la quantité au stock (dans l'objet en mémoire)
        crypto.crediter_stock(quantite)

        # On sauvegarde le nouveau stock en base de données
        self.__crypto_access.update_stock(crypto.get_id_crypto(), crypto.get_quantite_stock())

        # On enregistre la transaction dans la base
        id_tx = self.__transaction_access.enregistrer(
            "VENTE_USER", quantite, montant, crypto.get_id_crypto()
        )

        return {
            "succes":           True,
            "type":             "VENTE_USER",
            "crypto":           crypto.get_symbole(),
            "quantite":         quantite,
            "montant_usd":      montant,
            "stock_restant":    crypto.get_quantite_stock(),
            "id_transaction":   id_tx,
            "restock_effectue": None
        }

    # --- Restock automatique (méthode privée, appelée en interne) ---

    def __effectuer_restock(self, crypto):
        """
        Déclenche un restock automatique.
        On ajoute QUANTITE_RECHARGE unités pour revenir à 1000.
        Cette méthode est privée : elle n'est appelée que depuis acheter().
        """
        crypto.crediter_stock(QUANTITE_RECHARGE)

        # Sauvegarde du nouveau stock en base
        self.__crypto_access.update_stock(crypto.get_id_crypto(), crypto.get_quantite_stock())

        # Enregistrement du restock dans la table restock
        id_rs = self.__restock_access.enregistrer(QUANTITE_RECHARGE, crypto.get_id_crypto())

        print("Restock automatique : " + crypto.get_symbole()
              + " +" + str(QUANTITE_RECHARGE) + " unités"
              + " → stock : " + str(crypto.get_quantite_stock()))

        return {
            "quantite_ajoutee": QUANTITE_RECHARGE,
            "nouveau_stock":    crypto.get_quantite_stock(),
            "id_restock":       id_rs
        }

    # --- Historique ---

    def historique_transactions(self, id_crypto=None):
        """Retourne l'historique des transactions. Filtrable par crypto."""
        if id_crypto is not None:
            return self.__transaction_access.get_by_crypto(id_crypto)
        return self.__transaction_access.get_all()

    def historique_restocks(self, id_crypto):
        """Retourne l'historique des restocks pour une crypto."""
        return self.__restock_access.get_by_crypto(id_crypto)