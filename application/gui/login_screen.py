from hashlib import sha3_256

from tkinter import (
    X,
    W,
    LEFT,
    Label,
    Entry,
    StringVar,
    OptionMenu,
    HORIZONTAL,
)
from tkinter import ttk
from tkinter import Tk
from tkinter import messagebox

from application.gui.admin.main_view import AdminMainView
from application.gui.professor.professor_window import ProfessorMainView
from application.gui.student.student_main_window import MainViewStudent
from application.lib.db_ops import db_operation
from application.lib.constants import SALT


class LoginScreen:

    def __init__(self, window):
        self.window = window
        self.window.title("Login")
        self.frame = ttk.Labelframe(window, text="Login")
        self.frame.pack(fill=X)
        self.create_layout()
        self.user_type_options = ["Admin", "Professor", "Student"]
        self.user_type_dict = {"Admin": 1, "Professor": 2, "Student": 3}

    def create_layout(self):

        self.create_input_layout()
        # horizontal separator
        h_sep = ttk.Separator(self.frame, orient=HORIZONTAL)
        h_sep.pack()
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=X)
        button_ok = ttk.Button(button_frame, text='Login',
                               command=self.process_login)
        button_clear = ttk.Button(
            button_frame, text='Clear', command=self.clear_form)
        button_ok.pack()
        button_clear.pack()

    def create_input_layout(self):

        self.user_type_options = ["Admin", "Professor", "Student"]
        # user-name
        username_frame = ttk.Frame(self.frame)
        username_frame.pack(fill=X)
        username_label = Label(username_frame, text="Username", width=15)
        username_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.username_entry = Entry(username_frame)
        self.username_entry.pack(fill=X, padx=(5, 100), expand=True)

        # password
        password_frame = ttk.Frame(self.frame)
        password_frame.pack(fill=X)
        password_label = Label(password_frame, text="Password", width=15)
        password_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.password_entry = Entry(password_frame, show="*")
        self.password_entry.pack(fill=X, padx=(5, 100), expand=True)

        # user type selection
        user_type_frame = ttk.Frame(self.frame)
        user_type_frame.pack(fill=X)
        user_type_label = Label(user_type_frame, text="User Type", width=15)
        user_type_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        dropdown_frame = ttk.Frame(user_type_frame)
        dropdown_frame.pack(anchor=W, padx=(5, 100))
        self.dropdown_value = StringVar(dropdown_frame)
        self.dropdown_value.set(self.user_type_options[0])  # default value
        dropdown_widget = OptionMenu(
            dropdown_frame,
            self.dropdown_value,
            *self.user_type_options
        )
        dropdown_widget.pack(anchor=W)


    def process_login(self):
        '''This function invokes when the okay button is pressed.'''
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self.dropdown_value.get()
        user_type_id = self.user_type_dict[user_type]
        db_data = db_operation.check_login(username, user_type_id)
        if db_data:
            passwd = db_data[0]
            print(sha3_256(f"{password}{SALT}".encode()), password)
            if passwd == sha3_256(f"{password}{SALT}".encode()).hexdigest():
                print("matching")
            else:
                messagebox.showerror("Login Failed.", "Username or Password is incorrect.")
                return
        else:
            messagebox.showerror("Login Failed", "No matching data found on db.")
            return
        if user_type == "Admin":
            self.window.destroy()
            newroot = Tk()
            newroot.title("Admin Page")
            AdminMainView(newroot)
            newroot.mainloop()
        elif user_type == "Professor":
            self.window.destroy()
            newroot = Tk()
            newroot.title("Professor View")
            ProfessorMainView(newroot, db_data)
            newroot.mainloop()
        else:
            self.window.destroy()
            newroot = Tk()
            newroot.title("Professor View")
            MainViewStudent(newroot, db_data)
            newroot.mainloop()



    def get_input_list(self):
        return [
            self.username_entry,
            self.password_entry,
        ]

    def clear_form(self):
        '''clear all the input fields'''
        for input_field in self.get_input_list():
            # clear the input data
            input_field.delete(0, 'end')
        self.dropdown_value.set(self.user_type_options[-1])  # set to default value: ie, student


if __name__ == "__main__":
    root = Tk()
    # root.geometry('425x185+700+300')
    application = LoginScreen(root)
    root.mainloop()
