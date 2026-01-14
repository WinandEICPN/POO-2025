import tkinter as tk

from exercices.tkinter.classes.Page.LogIn import LogIn
from exercices.tkinter.classes.db.DAO import UserDao
from exercices.tkinter.classes.db.DbConnection import DbConnection


def main():
    db = DbConnection("app.db")
    dao = UserDao(db)
    dao.create_table()

    root = tk.Tk()
    app = LogIn(root, dao)

    try:
        root.mainloop()
    finally:
        db.close()


main()
