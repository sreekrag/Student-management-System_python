from tkinter import (
    X,
    W,
    E,
    LEFT,
    BOTH,
    Label,
    Entry,
    Button,
    BOTTOM,
    StringVar,
    OptionMenu,
    HORIZONTAL,
    Radiobutton,
)
from tkinter import ttk

from application.lib.db_ops import db_operation


class ViewStudent:

    column_replace = {
    "STUDENT_ID": "s.student_number",
    "FIRST_NAME": "usr.first_name",
    "LAST_NAME": "usr.last_name",
    "USERNAME": "usr.username",
    "EMAIL_ID": "usr.email_id",
    }

    def __init__(self, tab_controller, window):
        self.tab_controller = tab_controller
        self.window = window
        self.frame = ttk.Labelframe(tab_controller, text="View-Data")
        self.frame.pack(fill=X)
        self.tab_controller.add(self.frame, text='View Data')


        # FILTER OPTIONS
        self.filter_by_option = [
            "STUDENT_ID",
            "FIRST_NAME",
            "LAST_NAME",
            "USERNAME",
            "EMAIL_ID",
        ]
        # SORT KEYS
        self.sort_keys = [
            "STUDENT_ID",
            "FIRST_NAME",
            "LAST_NAME",
            "USERNAME",
            "EMAIL_ID",
        ]
        # StudentsBean obj
        self.data_keys = ['student_id', 'first_name', 'last_name', 'major', 'phone', 'gpa', 'date_of_birth']

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
        filter_sort_frame.pack(padx=20, pady=10, side=LEFT, fill=X)
        self.create_dropdown_layout(filter_sort_frame)
        # horizontal separator
        h_sep = ttk.Separator(filter_sort_frame, orient=HORIZONTAL)
        h_sep.pack(fill=X, padx=5, pady=10)
        self.create_sort_radio_btn_layout(filter_sort_frame)
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


    def search_result_frame(self, parent_frame):
        headers = (
            'ID',
            'STUDENT ID',
            'USERNAME',
            'FIRST NAME',
            'LAST NAME',
            'EMAIL_ID'
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
        search_field = self.searchbox_entry.get()
        dropdown_data = self.dropdown_value.get()
        sort_key = self.sort_value.get()
        self.clear_data()
        results = db_operation.admin_view_students(
            search_key=search_field,
            sort_key=self.column_replace[sort_key],
            filter_key=self.column_replace[dropdown_data]
        )
        print(results)
        if results:
            for row in results:
                self.tree.insert('', 'end', values=row)