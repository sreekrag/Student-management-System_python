from tkinter import ttk
from tkinter import (
    X,
    W,
    END,
    LEFT,
    BOTH,
    Label,
    Entry,
    Button,
    StringVar,
    OptionMenu,
    HORIZONTAL,
    Radiobutton,
)
from tkinter import messagebox

from application.gui.student.validators import (
    is_digit_validator,
    is_float_validator
)
from application.gui.professor.admin_add_professor import AddProfessor
from application.lib.db_ops import db_operation


class UpdateProfessor(AddProfessor):

    column_replace = {
        "EMPLOYEE_ID": "p.student_number",
        "FIRST_NAME": "usr.first_name",
        "LAST_NAME": "usr.last_name",
        "USERNAME": "usr.username",
        "EMAIL_ID": "usr.email_id",
    }
    def __init__(self, tab_controller, window):
        self.tab_controller = tab_controller
        self.window = window
        self.frame = ttk.Labelframe(tab_controller, text="Update/Delete Student")
        self.frame.pack(fill=X)
        self.tab_controller.add(self.frame, text='Update/Delete Data')

        # register the validators
        self.student_id_validator = self.window.register(is_digit_validator)
        self.gpa_validator = self.window.register(is_float_validator)

        # FILTER OPTIONS
        self.filter_by_option = [
            "EMPLOYEE_ID",
            "FIRST_NAME",
            "LAST_NAME",
            "USERNAME",
            "EMAIL_ID",
        ]
        # SORT KEYS
        self.sort_keys = [
            "EMPLOYEE_ID",
            "FIRST_NAME",
            "LAST_NAME",
            "USERNAME",
            "EMAIL_ID",
        ]

        # StudentsBean obj
        self.data_keys = ['student_id', 'first_name',
                          'last_name', 'major', 'phone', 'gpa', 'date_of_birth']

    def create_searchbox(self, parent_frame):
        # searchbox
        searchbox_frame = ttk.Labelframe(parent_frame, text="Search Here..")
        searchbox_frame.pack(fill=X)
        self.searchbox_entry = Entry(searchbox_frame)
        # self.searchbox_entry.pack(padx=5, expand=True, anchor=W)
        self.searchbox_entry.pack(padx=20, pady=5, expand=1)

        # Search Button
        search_button = Button(parent_frame,
                               text="Search",
                               command=self.search_student)
        search_button.pack(padx=20, pady=8)
        # clear Button
        clear_button = Button(parent_frame,
                              text="Clear",
                              command=self.clear_data)
        clear_button.pack(padx=20, pady=5)

    def create_dropdown_layout(self, parent_frame):
        # drop down list to choose the filter by
        label = Label(
            parent_frame, text='Choose a filter option', padx=15, pady=5,
            font='Helvetica 12 bold'
        )
        label.pack()
        dropdown_frame = ttk.Frame(parent_frame)
        dropdown_frame.pack(anchor=W, padx=10)
        self.dropdown_value = StringVar(dropdown_frame)
        self.dropdown_value.set(self.filter_by_option[0])  # default value
        dropdown_widget = OptionMenu(
            dropdown_frame,
            self.dropdown_value,
            *self.filter_by_option
        )
        dropdown_widget.pack(anchor=W)

    def create_sort_radio_btn_layout(self, parent_frame):
        # radio button for sort keys
        label = Label(
            parent_frame, text='Sort Option', padx=15, pady=5,
            font='Helvetica 12 bold'
        )
        label.pack(anchor=W)
        sort_frame = ttk.Frame(parent_frame)
        sort_frame.pack(anchor=W)
        self.sort_value = StringVar(sort_frame)
        for val, key in enumerate(self.sort_keys):
            Radiobutton(sort_frame,
                        text=key,
                        padx=8,
                        variable=self.sort_value,
                        # command=self.set_sort_key,
                        value=key).pack(anchor=W)
        self.sort_value.set(self.sort_keys[0])  # default value


    def create_layout(self):
        # a frame to hold search, filter & sort frames
        user_input_wrapper_frame = ttk.Frame(self.frame)
        user_input_wrapper_frame.pack(fill=X)

        # search frame
        search_main_frame = ttk.Frame(user_input_wrapper_frame)
        search_main_frame.pack(padx=20, pady=10, side=LEFT, fill=X)
        self.create_searchbox(search_main_frame)
        # frame to hold filter and sort details
        filter_sort_frame = ttk.Labelframe(
            user_input_wrapper_frame, text="Filter & Sort")
        filter_sort_frame.pack(padx=20, pady=10, side=LEFT, fill=BOTH)
        self.create_dropdown_layout(filter_sort_frame)
        # horizontal separator
        h_sep = ttk.Separator(self.frame, orient=HORIZONTAL)
        h_sep.pack(fill=X, padx=5, pady=3)


        # result show place holder
        modify_wrapper_frame = ttk.Frame(self.frame)
        modify_wrapper_frame.pack(fill=X, pady=25)

        # user_id (not included in the inherited layout)
        user_id_frame = ttk.Frame(modify_wrapper_frame)
        user_id_frame.pack(fill=X)
        user_id_label = Label(user_id_frame, text="User_id", width=15)
        user_id_label.pack(side=LEFT, padx=10, pady=5)
        self.user_id_entry = Entry(user_id_frame)
        self.user_id_entry.pack(fill=X, padx=(5, 100), expand=True)

        employee_id_frame = ttk.Frame(modify_wrapper_frame)
        employee_id_frame.pack(fill=X)
        employee_id_label = Label(employee_id_frame, text="Student Number", width=15)
        employee_id_label.pack(side=LEFT, padx=10, pady=5)
        self.employee_id_entry = Entry(employee_id_frame)
        self.employee_id_entry.pack(fill=X, padx=(5, 100), expand=True)

        self.create_input_layout(modify_wrapper_frame)

        button_frame = ttk.Frame(modify_wrapper_frame)
        button_frame.pack(fill=X)
        button_ok = ttk.Button(button_frame, text='Update',
                               command=self.modify_professor_data)
        button_clear = ttk.Button(
            button_frame, text='Clear', command=self.clear_form)
        button_delete = ttk.Button(button_frame, text='Delete User',
                                   command=self.delete_user)
        button_ok.pack()
        button_clear.pack()
        button_delete.pack()


    def get_input_list(self):
        return [
            self.user_id_entry,
            self.employee_id_entry,
            self.username_entry,
            self.first_name_entry,
            self.last_name_entry,
            self.email_entry
        ]

    def clear_data(self):
        self.searchbox_entry.delete(0, 'end')
        # set default value
        self.dropdown_value.set(self.filter_by_option[0])
        # removing table entries
        self.user_id_entry.config(state="normal")
        for input_field in self.get_input_list():
            # clear the input data
            input_field.delete(0, 'end')
        self.password_entry.delete(0, 'end')

    def delete_user(self):
        answer = messagebox.askquestion('Delete User', 'Are you sure you want to DELETE the user?', icon='warning')
        if answer == "yes":
            user_id = self.user_id_entry.get()
            student_id = self.employee_id_entry.get()
            try:
                db_operation.admin_delete_student(
                    user_id=user_id,
                    student_id=student_id
                )
                messagebox.showinfo("Success", "Successfully delete Student info")
                self.clear_data()
            except Exception as e:
                messagebox.showerror("Delete Operation Failed", str(e))

    def search_student(self):
        '''Student searching main logic goes here.'''
        search_field = self.searchbox_entry.get()
        dropdown_data = self.dropdown_value.get()
        self.clear_data()
        results = db_operation.admin_view_professor(
            search_key=search_field,
            sort_key="usr.id",
            filter_key=self.column_replace[dropdown_data],
            all=False
        )
        # (2, 123, 'rsree', 'Sree', 'Rag', 'srag@sree.com')
        if results:
            self.user_id_entry.config(state="normal")
            for idx, entry in enumerate(self.get_input_list()):
                entry.insert(END, results[idx])
            self.user_id_entry.config(state="disabled")

    def modify_professor_data(self):
        '''This function invokes when the okay button is pressed.'''
        user_id = self.user_id_entry.get()
        employee_id = self.employee_id_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        email_id = self.email_entry.get()

        # writing the student data
        try:
            db_operation.admin_view_update_professors(
                user_id=user_id,
                employee_id=employee_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                email_id=email_id,
            )
            self.clear_data()
            messagebox.showinfo("Success", "Successfully Updated the Student info.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
