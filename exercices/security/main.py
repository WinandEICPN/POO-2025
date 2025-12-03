from classes.SystemeSurveillance import SystemeSurveillance
from classes.Journal import Journal


def creer_journal_exemple():
    return [
        Journal(0),
        Journal(1),
        Journal(0),
        Journal(2),
        Journal(1),
    ]

def main():
    systeme = SystemeSurveillance()

    systeme.creer_capteur(SystemeSurveillance.TYPE_ANTIVIRUS,
                          'Antivirus serveur fichiers', True)

    systeme.creer_capteur(SystemeSurveillance.TYPE_IDS_RESEAU,
                          'IDS réseau principal', True)

    systeme.creer_capteur(SystemeSurveillance.TYPE_IDS_SYSTEME,
                          'IDS serveur Linux', True)

    print('=== Capteurs enregistrés ===')
    systeme.lister_capteurs()
    print()

    journal = creer_journal_exemple()

    print('=== Analyse globale ===')
    print(systeme.analyser_tous(journal))

if __name__ == '__main__':
    main()
