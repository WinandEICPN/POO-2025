from classes.CommandeManager import CommandeManager
from classes.Plat import PlatChaud

p = PlatChaud("Pizza", 15.2)
p2 = PlatChaud("Steak", 14.2)

c1 = CommandeManager()
c2 = CommandeManager()
c1.ajouterPlat(p)
c2.ajouterPlat(p2)

c1.printAllPlat()