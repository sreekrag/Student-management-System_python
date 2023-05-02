from tkinter import (
    X,
    W,
    LEFT,
    Label,
    Entry,
    HORIZONTAL,
)
from tkinter import ttk
from tkinter import messagebox

from application.gui.student.validators import (
    is_digit_validator,
    is_float_validator
)
from application.lib.db_ops import db_operation

class AddCourse:

    def __init__(self, tab_controller, window):
        self.tab_controller = tab_controller
        self.window = window
        self.frame = ttk.Labelframe(tab_controller, text="Add-Data")
        self.frame.pack(fill=X)
        self.tab_controller.add(self.frame, text='Add Data')

        # register the validators
        self.course_id_validator = self.window.register(is_digit_validator)


    def add_course_data(self):
        '''This function invokes when the okay button is pressed.'''
        course_id = self.course_id_entry.get()
        course_name = self.course_name_entry.get()
        professor_id = self.professor_id_entry.get()


        # writing the course data
        try:
            db_operation.admin_add_course(
                course_id=course_id,
                course_name=course_name,
                professor_id=professor_id
            )
            messagebox.showinfo("Information", "Succesfully Added data to DB")
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Operation Failed", str(e))

    def create_input_layout(self, parent_frame):
        # course id
        course_id_frame = ttk.Frame(parent_frame)
        course_id_frame.pack(fill=X)
        course_id_label = Label(course_id_frame, text="CourseID", width=15)
        course_id_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.course_id_entry = Entry(course_id_frame, validate="key", validatecommand=(
            self.course_id_validator, "%P"))
        self.course_id_entry.pack(fill=X, padx=(5, 100), expand=True)

        # course name
        course_name_frame = ttk.Frame(parent_frame)
        course_name_frame.pack(fill=X)
        course_name_label = Label(course_name_frame, text="CourseName", width=15)
        course_name_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.course_name_entry = Entry(course_name_frame)
        self.course_name_entry.pack(fill=X, padx=(5, 100), expand=True)

        # professor id
        professor_id_frame = ttk.Frame(parent_frame)
        professor_id_frame.pack(fill=X)
        professor_id_label = Label(professor_id_frame, text="ProfessorID", width=15)
        professor_id_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.professor_id_entry = Entry(professor_id_frame, validate="key", validatecommand=(
            self.course_id_validator, "%P"))
        self.professor_id_entry.pack(fill=X, padx=(5, 100), expand=True)

    def create_layout(self):
        label = Label(self.frame, text='Enter Details Below',
                      padx=5, pady=5,
                      font='Helvetica 12 bold'
                      )
        label.pack()


        self.create_input_layout(self.frame)
        # horizontal separator
        h_sep = ttk.Separator(self.frame, orient=HORIZONTAL)
        h_sep.pack()

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=X)
        button_ok = ttk.Button(button_frame, text='Okay',
                               command=self.add_course_data)
        button_clear = ttk.Button(
            button_frame, text='Clear', command=self.clear_form)
        button_ok.pack()
        button_clear.pack()

    def get_input_list(self):
        return [
            self.course_id_entry,
            self.course_name_entry,
            self.professor_id_entry
        ]

    def clear_form(self):
        '''clear all the input fields'''
        for input_field in self.get_input_list():
            # clear the input data
            input_field.delete(0, 'end')
