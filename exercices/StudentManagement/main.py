from classes.BusinessClasses import StudentAccess

studentAccess = StudentAccess()
students = studentAccess.getStudents()
for student in students:
    print(student)
    studentAccess.loadCourses(student)
    for course in student.courses:
        print(f"    l'étudiant est inscrit au cours: {course.course.titre} depuis {course.dateInscription}")



