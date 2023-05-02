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
from application.gui.student.add_student import AddStudent
from application.lib.db_ops import db_operation

class AddProfessor(AddStudent):

    def __init__(self, tab_controller, window):
        self.tab_controller = tab_controller
        self.window = window
        self.frame = ttk.Labelframe(tab_controller, text="Add-Data")
        self.frame.pack(fill=X)
        self.tab_controller.add(self.frame, text='Add Data')

        # register the validators
        self.employee_id_validator = self.window.register(is_digit_validator)
        self.gpa_validator = self.window.register(is_float_validator)


    def add_professor_data(self):
        '''This function invokes when the okay button is pressed.'''
        employee_id = self.employee_id_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        email_id = self.email_entry.get()


        # writing the student data
        try:
            db_operation.admin_add_professor(
                employee_id=employee_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                email_id=email_id
            )
            messagebox.showinfo("Information", "Succesfully Added data to DB")
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Operation Failed", str(e))

    def create_layout(self):
        label = Label(self.frame, text='Enter Details Below',
                      padx=5, pady=5,
                      font='Helvetica 12 bold'
                      )
        label.pack()

        # empoloyee id
        employee_id_frame = ttk.Frame(self.frame)
        employee_id_frame.pack(fill=X)
        employee_id_label = Label(employee_id_frame, text="EmployeeID", width=15)
        employee_id_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.employee_id_entry = Entry(employee_id_frame, validate="key", validatecommand=(
            self.employee_id_validator, "%P"))
        self.employee_id_entry.pack(fill=X, padx=(5, 100), expand=True)

        self.create_input_layout(self.frame)
        # horizontal separator
        h_sep = ttk.Separator(self.frame, orient=HORIZONTAL)
        h_sep.pack()

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=X)
        button_ok = ttk.Button(button_frame, text='Okay',
                               command=self.add_professor_data)
        button_clear = ttk.Button(
            button_frame, text='Clear', command=self.clear_form)
        button_ok.pack()
        button_clear.pack()

    def get_input_list(self):
        return [
            self.username_entry,
            self.password_entry,
            self.first_name_entry,
            self.last_name_entry,
            self.employee_id_entry,
            self.email_entry
        ]

    def clear_form(self):
        '''clear all the input fields'''
        for input_field in self.get_input_list():
            # clear the input data
            input_field.delete(0, 'end')
