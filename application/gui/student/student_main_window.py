from tkinter import (
    X,
    W,
    E,
    END,
    LEFT,
    BOTH,
    Label,
    Entry,
    BOTTOM,
    HORIZONTAL,
)
from tkinter import ttk

from application.lib.db_ops import db_operation


class MainViewStudent:

    def __init__(self, window, initial_data):
        # password, id, username, email_id, first_name, last_name
        self.initial_data = initial_data
        self.window = window
        self.frame = ttk.Labelframe(self.window, text="View-Data")
        self.frame.pack(fill=X)

        self.create_layout()


    def create_input_layout(self, parent_frame):
        # first name
        first_name_frame = ttk.Frame(parent_frame)
        first_name_frame.pack(fill=X)
        first_name_label = Label(first_name_frame, text="First Name", width=15)
        first_name_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.first_name_entry = Entry(first_name_frame)
        self.first_name_entry.pack(fill=X, padx=(5, 100), expand=True)
        self.first_name_entry.insert(END, self.initial_data[-2])
        self.first_name_entry.config(state="disabled")

        # last name
        last_name_frame = ttk.Frame(parent_frame)
        last_name_frame.pack(fill=X)
        last_name_label = Label(last_name_frame, text="Last Name", width=15)
        last_name_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.last_name_entry = Entry(last_name_frame)
        self.last_name_entry.pack(fill=X, padx=(5, 100), expand=True)
        self.last_name_entry.insert(END, self.initial_data[-1])
        self.last_name_entry.config(state="disabled")

        # email_id
        email_id = ttk.Frame(parent_frame)
        email_id.pack(fill=X)
        email_label = Label(email_id, text="Email ID", width=15)
        email_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.email_entry = Entry(email_id)
        self.email_entry.pack(fill=X, padx=(5, 100), expand=True)
        self.email_entry.insert(END, self.initial_data[-3])
        self.email_entry.config(state="disabled")

        # username
        username = ttk.Frame(parent_frame)
        username.pack(fill=X)
        user_label = Label(username, text="Username", width=15)
        user_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.username_entry = Entry(username)
        self.username_entry.pack(fill=X, padx=(5, 100), expand=True)
        self.username_entry.insert(END, self.initial_data[-4])
        self.username_entry.config(state="disabled")


    def create_layout(self):
        # a frame to hold search, filter & sort frames
        user_input_wrapper_frame = ttk.Frame(self.frame)
        user_input_wrapper_frame.pack(fill=X)

        self.create_input_layout(user_input_wrapper_frame)

        # horizontal separator
        h_sep = ttk.Separator(self.frame, orient=HORIZONTAL)
        h_sep.pack(fill=X, padx=5, pady=3)

        # result show place holder
        table_wrapper_frame = ttk.Frame(self.frame)
        table_wrapper_frame.pack(fill=X, padx=15, side=BOTTOM)
        self.search_result_frame(table_wrapper_frame)

    def create_table_layout(self, parent_frame, headers):
        results_label = ttk.Label(parent_frame, text="Search Results")
        results_label.pack(fill=X)
        table_frame = ttk.Frame(parent_frame)
        table_frame.pack(fill=BOTH)
        columns = tuple(range(len(headers)))
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.pack(fill=X, anchor=W)
        for col, col_name in enumerate(headers):
            self.tree.heading(col, text=col_name)
            self.tree.column(col, width=100)
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scroll.pack(side='right', fill='y', anchor=E)

        self.tree.configure(yscrollcommand=scroll.set)
        self.search_student()


    def search_result_frame(self, parent_frame):
        headers = (
            'COURSE ID',
            'COURSE NAME',
            'GRADE',
        )
        self.create_table_layout(parent_frame, headers=headers)

    def clear_data(self):
        self.searchbox_entry.delete(0, 'end')
        # set default value
        self.dropdown_value.set(self.filter_by_option[0])
        self.sort_value.set(self.sort_keys[0])
        # removing table entries
        for data in self.tree.get_children():
            self.tree.delete(data)

    def search_student(self):
        '''Student searching main logic goes here.'''
        results = db_operation.get_student_grades(
            user_id=self.initial_data[1]
        )
        print(results)
        if results:
            for row in results:
                self.tree.insert('', 'end', values=row)
