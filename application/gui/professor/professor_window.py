from tkinter import (
    X,
    W,
    END,
    LEFT,
    Label,
    Entry,
    HORIZONTAL,
)
from tkinter import ttk
from tkinter import messagebox

from application.gui.student.validators import (
    is_digit_validator,
    # is_float_validator
)
from application.lib.db_ops import db_operation



def is_grade_validator(value_str):
    if not value_str:
        # just to use the clear method
        # or else this field wont cleared
        return True
    try:
        value = int(value_str)
        if value > 0 and value <=100:
            return True
        return False
    except ValueError:
        return False



class ProfessorMainView:

    def __init__(self, window, initial_data):
        self.window = window
        self.exit_app = lambda: window.destroy()
        # password, id, first_name, last_name
        self.initial_data = initial_data
        self.frame = ttk.Labelframe(self.window, text="Add-Data")
        self.frame.pack(fill=X)

        # register the validators
        self.grade_validator = self.window.register(is_grade_validator)
        self.id_validator = self.window.register(is_digit_validator)
        self.create_layout()


    def add_professor_data(self):
        '''This function invokes when the okay button is pressed.'''
        student_id = self.student_id_entry.get()
        student_first_name = self.student_first_name_entry.get()
        student_last_name = self.student_last_name_entry.get()
        course_id = self.course_id_entry.get()
        course_name = self.course_name_entry.get()
        grade = self.grade_entry.get()
        prof_first_name = self.professor_first_name_entry.get()

        # writing the grade data
        try:
            db_operation.add_grades(
                student_id=student_id,
                student_first_name=student_first_name,
                student_last_name=student_last_name,
                course_id=course_id,
                course_name=course_name,
                grade=grade,
                prof_user_id=self.initial_data[1]
            )
            messagebox.showinfo("Information", "Succesfully Added data to DB")
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Operation Failed", str(e))

    def create_input_layout(self, parent_frame):

        # Professor First Name
        professor_first_name_frame = ttk.Frame(parent_frame)
        professor_first_name_frame.pack(fill=X)
        professor_first_name_label = Label(professor_first_name_frame, text="First Name", width=15)
        professor_first_name_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.professor_first_name_entry = Entry(professor_first_name_frame)
        self.professor_first_name_entry.pack(fill=X, padx=(5, 100), expand=True)
        self.professor_first_name_entry.insert(END, self.initial_data[-2])
        self.professor_first_name_entry.config(state="disabled")

        # Professor Last Name
        professor_last_name_frame = ttk.Frame(parent_frame)
        professor_last_name_frame.pack(fill=X)
        professor_last_name_label = Label(professor_last_name_frame, text="Last Name", width=15)
        professor_last_name_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.professor_last_name_entry = Entry(professor_last_name_frame)
        self.professor_last_name_entry.pack(fill=X, padx=(5, 100), expand=True)
        self.professor_last_name_entry.insert(END, self.initial_data[-1])
        self.professor_last_name_entry.config(state="disabled")

        # Course Name
        course_name_frame = ttk.Frame(parent_frame)
        course_name_frame.pack(fill=X)
        course_name_label = Label(course_name_frame, text="Course Name", width=15)
        course_name_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.course_name_entry = Entry(course_name_frame)
        self.course_name_entry.pack(fill=X, padx=(5, 100), expand=True)

        # Course Number
        course_id_frame = ttk.Frame(parent_frame)
        course_id_frame.pack(fill=X)
        course_id_label = Label(course_id_frame, text="Course Number", width=15)
        course_id_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.course_id_entry = Entry(course_id_frame, validate="key", validatecommand=(
            self.id_validator, "%P"))
        self.course_id_entry.pack(fill=X, padx=(5, 100), expand=True)

        # Student Number
        student_id_frame = ttk.Frame(parent_frame)
        student_id_frame.pack(fill=X)
        student_id_label = Label(student_id_frame, text="Student Number", width=15)
        student_id_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.student_id_entry = Entry(student_id_frame, validate="key", validatecommand=(
            self.id_validator, "%P"))
        self.student_id_entry.pack(fill=X, padx=(5, 100), expand=True)

        # Student Name
        student_first_name_frame = ttk.Frame(parent_frame)
        student_first_name_frame.pack(fill=X)
        student_first_name_label = Label(student_first_name_frame, text="Student First Name", width=15)
        student_first_name_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.student_first_name_entry = Entry(student_first_name_frame)
        self.student_first_name_entry.pack(fill=X, padx=(5, 100), expand=True)

        # Student Name
        student_last_name_frame = ttk.Frame(parent_frame)
        student_last_name_frame.pack(fill=X)
        student_last_name_label = Label(student_last_name_frame, text="Student Last Name", width=15)
        student_last_name_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.student_last_name_entry = Entry(student_last_name_frame)
        self.student_last_name_entry.pack(fill=X, padx=(5, 100), expand=True)

        # Grade
        grade_frame = ttk.Frame(parent_frame)
        grade_frame.pack(fill=X)
        grade_label = Label(grade_frame, text="Grade", width=15)
        grade_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.grade_entry = Entry(grade_frame, validate="key", validatecommand=(
            self.grade_validator, "%P"))
        self.grade_entry.pack(fill=X, padx=(5, 100), expand=True)

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
        button_ok = ttk.Button(button_frame, text='Submit',
                               command=self.add_professor_data)
        button_clear = ttk.Button(
            button_frame, text='Reset', command=self.clear_form)
        button_exit = ttk.Button(
            button_frame, text='Exit', command=self.exit_app)
        button_ok.pack()
        button_clear.pack()
        button_exit.pack()


    def get_input_list(self):
        return [
            self.student_id_entry,
            self.student_first_name_entry,
            self.student_last_name_entry,
            self.course_id_entry,
            self.course_name_entry,
            self.grade_entry,
        ]

    def clear_form(self):
        '''clear all the input fields'''
        for input_field in self.get_input_list():
            # clear the input data
            input_field.delete(0, 'end')
