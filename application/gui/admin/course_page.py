from tkinter import ttk

from application.gui.course.admin_add_course import AddCourse
from application.gui.course.admin_view_course import ViewCourses
from application.gui.course.admin_update_course import UpdateCourses

class AdminCourseView:

    def __init__(self, parent):
        self.main_window = parent
        self.tab_control = ttk.Notebook(self.main_window)
        self.create_layout()

    def create_layout(self):
        # add Course
        add_data = AddCourse(self.tab_control, self.main_window)
        add_data.create_layout()

        # view courses
        view_data = ViewCourses(self.tab_control, self.main_window)
        view_data.create_layout()

        # update course
        update_data = UpdateCourses(self.tab_control, self.main_window)
        update_data.create_layout()

        self.tab_control.pack(expand=1, fill='both')

