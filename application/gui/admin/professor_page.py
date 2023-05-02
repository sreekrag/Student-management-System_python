from tkinter import ttk

from application.gui.professor.admin_add_professor import AddProfessor
from application.gui.professor.admin_update_professor import UpdateProfessor
from application.gui.professor.admin_professor_view import ViewProfessor

class AdminProfessorView:

    def __init__(self, parent):
        self.main_window = parent
        self.tab_control = ttk.Notebook(self.main_window)
        self.create_layout()

    def create_layout(self):
        # add prof
        add_data = AddProfessor(self.tab_control, self.main_window)
        add_data.create_layout()

        # view prof
        view_data = ViewProfessor(self.tab_control, self.main_window)
        view_data.create_layout()

        # update prof
        update_data = UpdateProfessor(self.tab_control, self.main_window)
        update_data.create_layout()

        self.tab_control.pack(expand=1, fill='both')

