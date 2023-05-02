from tkinter import ttk

from application.gui.student.update_student import UpdateStudent
from application.gui.student.view_student import ViewStudent
from application.gui.student.add_student import AddStudent

class AdminStudnetView:


    def __init__(self, parent):
        self.main_window = parent
        self.tab_control = ttk.Notebook(self.main_window)
        self.create_layout()

    def create_layout(self):
        # add Student
        add_data = AddStudent(self.tab_control, self.main_window)
        add_data.create_layout()

        # view student
        view_data = ViewStudent(self.tab_control, self.main_window)
        view_data.create_layout()

        # update student
        update_data = UpdateStudent(self.tab_control, self.main_window)
        update_data.create_layout()

        self.tab_control.pack(expand=1, fill='both')


