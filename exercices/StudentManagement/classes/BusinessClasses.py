from exercices.StudentManagement.classes.DBConnection import DBConnection
from exercices.StudentManagement.classes.DataClasse import Student, Course, Enrollment


class StudentAccess:
    def __init__(self):
        self.dbConnection = DBConnection.get_instance().get_connection()

    def getStudents(self):
        cursor = self.dbConnection.cursor()
        cursor.execute("SELECT * FROM TStudent")
        students = cursor.fetchall()
        returnList = []
        for student in students:
            student = Student(student["id_TStudent"], student["nom"], student["mail"])
            returnList.append(student)

        return returnList

    def getStudentByID(self, id):
        cursor = self.dbConnection.cursor()
        cursor.execute("SELECT * FROM TStudent WHERE id_TStudent = ?", (id,))
        student = cursor.fetchone()
        return Student(student["id_TStudent"], student["nom"], student["mail"])

    def loadCourses(self, student):
        cursor = self.dbConnection.cursor()
        cursor.execute("SELECT e.id_TCourse, e.date_inscription, e.note, c.Titre, c.Credit FROM TEnrollment E join TCourse C on e.id_TCourse = c.id_TCourse WHERE id_TStudent = ?", [student.id])
        courses = cursor.fetchall()
        for course in courses:
            Tcourse = Course(course["id_TCourse"], course["Titre"], course["Credit"])
            enrollment = Enrollment(student, Tcourse, course["date_inscription"], course["note"])
            student.courses.append(enrollment)