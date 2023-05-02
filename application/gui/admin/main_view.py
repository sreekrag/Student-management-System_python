from tkinter import *
from tkinter import ttk

from application.gui.admin.student_page import AdminStudnetView
from application.gui.admin.professor_page import AdminProfessorView
from application.gui.admin.course_page import AdminCourseView

class AdminMainView:

    def __init__(self, parent):
        self.parent = parent
        self.create_layout()

    def create_layout(self):
        self.tab_controller = ttk.Notebook(self.parent)
        self.tab_controller.pack()

        # student view
        self.student_frame = ttk.Labelframe(self.parent, text="Student View")
        self.student_frame.pack(fill=X)
        self.tab_controller.add(self.student_frame, text="Student")
        AdminStudnetView(self.student_frame)

        # professor view
        self.professor_frame = ttk.Labelframe(self.parent, text="Professor View")
        self.professor_frame.pack(fill=X)
        self.tab_controller.add(self.professor_frame, text="Professor")
        AdminProfessorView(self.professor_frame)

        # Course View
        self.course_frame = ttk.Labelframe(self.parent, text="Course View")
        self.course_frame.pack(fill=X)
        self.tab_controller.add(self.course_frame, text="Courses")
        AdminCourseView(self.course_frame)

if __name__ == "__main__":
    window = Tk()
    window.title("Student App")
    admin_view = AdminMainView(window)
    window.mainloop()
