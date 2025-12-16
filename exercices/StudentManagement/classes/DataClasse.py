class Student():
    def __init__(self, id, nom, mail):
        self.id = id
        self.nom = nom
        self.mail = mail
        self.courses = []

    def __str__(self):
        return f"l'étudiant s'appelle {self.nom} et à l'id:  {self.id}. mail: {self.mail}"

class Course():
    def __init__(self, id, titre, credit):
        self.id = id
        self.titre = titre
        self.credit = credit

class Enrollment():
    def __init__(self, student, course, dateInscription, note):
        self._student = student
        self._course = course
        self.dateInscription = dateInscription
        self.note = note

    @property
    def student(self):
        if self._student != None:
            return self._student
        else:
            raise AttributeError('Student is not set')
    @property
    def course(self):
        if self._course != None:
            return self._course
        else:
            raise AttributeError('Course is not set')

    @student.setter
    def student(self, value):
        self._student = value

    @course.setter
    def course(self, value):
        self._course = value