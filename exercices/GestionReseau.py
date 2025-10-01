import re

class Machine:
    def __init__(self, hostname, ip):
        self.__hostname = hostname
        self.__ip = ip
        self.__started = {}

    def ping(self, machine):
        ipLocal = self.__ip.split('.')
        ipDistant = machine.ip.split('.')
        ipCorrect = True
        for i in range(3):
            if ipLocal[i] != ipDistant[i]:
                ipCorrect = False
        return ipCorrect

    def start(self, service):
        self.__started[service] = True

    def stop(self, service):
        self.__started[service] = False

    def isStarted(self):
        returnList = []
        for service in self.__started.keys():
            if self.__started[service]:
                returnList.append(service)
        return returnList

#Getter Setter
    @property
    def hostname(self):
        return self.__hostname

    @hostname.setter
    def hostname(self, hostname):
        self.__hostname = hostname

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, ip):
        pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\." \
                  r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\." \
                  r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\." \
                  r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        if re.match(pattern, ip):
            self.__ip = ip
        else:
            print("IP invalide")

class Paquet:
    def __init__(self, type, taille):
        self.__type = type
        self.__taille = taille

    def envoyer(self):

# Getter Setter
    def getType(self):
        return self.__type

    def setType(self, type):
        self.__type = type

    def getTaille(self):
        return self.__taille

    def setTaille(self, taille):
        self.__taille = taille



srv1 = Machine('SRV1', '10.0.0.5')
print(f"ma machine {srv1.hostname} a l'adresse ip {srv1.ip}")

srv1.start("ssh")
print(srv1.isStarted())
srv1.start("http")
print(srv1.isStarted())
srv1.stop("ssh")
print(srv1.isStarted())

PC1 = Machine('PC1', '192.168.1.10')
PC2 = Machine('PC2', '192.168.1.21')
print(PC1.ping(PC2))
print(PC1.ping(srv1))


