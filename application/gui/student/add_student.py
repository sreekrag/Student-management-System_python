from tkinter import (
    X,
    W,
    LEFT,
    Label,
    Entry,
    HORIZONTAL,
)
from tkinter import messagebox
from tkinter import ttk

from application.gui.student.validators import (
    is_digit_validator,
    is_float_validator
)
from application.lib.db_ops import db_operation


class AddStudent:

    def __init__(self, tab_controller, window):
        self.tab_controller = tab_controller
        self.window = window
        self.frame = ttk.Labelframe(tab_controller, text="Add-Data")
        self.frame.pack(fill=X)
        self.tab_controller.add(self.frame, text='Add Data')

        # register the validators
        self.student_id_validator = self.window.register(is_digit_validator)
        self.gpa_validator = self.window.register(is_float_validator)


    def add_student_data(self):
        '''This function invokes when the okay button is pressed.'''
        student_id = self.student_id_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        password = self.password_entry.get()
        username = self.username_entry.get()
        email_id = self.email_entry.get()

        # writing the student data
        try:
            db_operation.admin_add_student(
                student_number=student_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                email_id=email_id
            )
            messagebox.showinfo("Information", "Succesfully Added data to DB")
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Operatin Failed", str(e))


    def create_layout(self):
        label = Label(self.frame, text='Enter Details Below',
                      padx=5, pady=5,
                      font='Helvetica 12 bold'
                      )
        label.pack()


        # student id
        student_id_frame = ttk.Frame(self.frame)
        student_id_frame.pack(fill=X)
        student_id_label = Label(student_id_frame, text="StudentID", width=15)
        student_id_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.student_id_entry = Entry(student_id_frame, validate="key", validatecommand=(
            self.student_id_validator, "%P"))
        self.student_id_entry.pack(fill=X, padx=(5, 100), expand=True)

        self.create_input_layout(self.frame)
        # horizontal separator
        h_sep = ttk.Separator(self.frame, orient=HORIZONTAL)
        h_sep.pack()

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=X)
        button_ok = ttk.Button(button_frame, text='Okay',
                               command=self.add_student_data)
        button_clear = ttk.Button(
            button_frame, text='Clear', command=self.clear_form)
        button_ok.pack()
        button_clear.pack()

    def create_input_layout(self, parent_frame):
        # first name
        first_name_frame = ttk.Frame(parent_frame)
        first_name_frame.pack(fill=X)
        first_name_label = Label(first_name_frame, text="First Name", width=15)
        first_name_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.first_name_entry = Entry(first_name_frame)
        self.first_name_entry.pack(fill=X, padx=(5, 100), expand=True)

        # last name
        last_name_frame = ttk.Frame(parent_frame)
        last_name_frame.pack(fill=X)
        last_name_label = Label(last_name_frame, text="Last Name", width=15)
        last_name_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.last_name_entry = Entry(last_name_frame)
        self.last_name_entry.pack(fill=X, padx=(5, 100), expand=True)

        # email_id
        email_id = ttk.Frame(parent_frame)
        email_id.pack(fill=X)
        email_label = Label(email_id, text="Email ID", width=15)
        email_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.email_entry = Entry(email_id)
        self.email_entry.pack(fill=X, padx=(5, 100), expand=True)

        # username
        username = ttk.Frame(parent_frame)
        username.pack(fill=X)
        user_label = Label(username, text="Username", width=15)
        user_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.username_entry = Entry(username)
        self.username_entry.pack(fill=X, padx=(5, 100), expand=True)

        # password
        password_frame = ttk.Frame(parent_frame)
        password_frame.pack(fill=X)
        password_label = Label(password_frame, text="Password", width=15)
        password_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.password_entry = Entry(password_frame)
        self.password_entry.pack(fill=X, padx=(5, 100), expand=True)

    def get_input_list(self):
        return [
            self.student_id_entry,
            self.first_name_entry,
            self.last_name_entry,
            self.email_entry,
            self.password_entry,
            self.email_entry,
            self.username_entry
        ]

    def clear_form(self):
        '''clear all the input fields'''
        for input_field in self.get_input_list():
            # clear the input data
            input_field.delete(0, 'end')
