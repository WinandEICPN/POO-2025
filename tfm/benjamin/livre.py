class Livre:
    def __init__(self, titre):
        self.__titre = titre

    def get_titre(self):
        return self.__titre