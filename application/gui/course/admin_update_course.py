from tkinter import ttk
from tkinter import (
    X,
    END,
    LEFT,
    BOTH,
    HORIZONTAL,
)
from tkinter import messagebox

from application.gui.student.validators import (
    is_digit_validator,
)
from application.gui.course.admin_add_course import AddCourse
from application.gui.course.admin_view_course import ViewCourses
from application.lib.db_ops import db_operation


class UpdateCourses(AddCourse, ViewCourses):

    def __init__(self, tab_controller, window):
        self.tab_controller = tab_controller
        self.window = window
        self.frame = ttk.Labelframe(tab_controller, text="Update/Delete Course")
        self.frame.pack(fill=X)
        self.tab_controller.add(self.frame, text='Update/Delete Data')

        # register the validators
        self.course_id_validator = self.window.register(is_digit_validator)

        # FILTER OPTIONS
        self.filter_by_option = [
            "COURSE_ID",
            "COURSE_NAME",
            "PROFESSOR_ID"
        ]
        # SORT KEYS
        self.sort_keys = [
            "COURSE_ID",
            "COURSE_NAME",
            "PROFESSOR_ID"
        ]

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

        self.create_input_layout(modify_wrapper_frame)

        button_frame = ttk.Frame(modify_wrapper_frame)
        button_frame.pack(fill=X)
        button_ok = ttk.Button(button_frame, text='Update',
                               command=self.modify_professor_data)
        button_clear = ttk.Button(
            button_frame, text='Clear', command=self.clear_form)
        button_delete = ttk.Button(button_frame, text='Delete Course',
                                   command=self.delete_user)
        button_ok.pack()
        button_clear.pack()
        button_delete.pack()


    def get_input_list(self):
        return [
            self.course_id_entry,
            self.course_name_entry,
            self.professor_id_entry
        ]

    def clear_data(self):
        self.searchbox_entry.delete(0, 'end')
        # set default value
        self.dropdown_value.set(self.filter_by_option[0])
        # removing table entries
        self.course_id_entry.config(state="normal")
        for input_field in self.get_input_list():
            # clear the input data
            input_field.delete(0, 'end')

    def delete_user(self):
        answer = messagebox.askquestion('Delete User', 'Are you sure you want to DELETE the user?', icon='warning')
        if answer == "yes":
            course_id = self.course_id_entry.get()
            try:
                db_operation.admin_delete_course(
                    course_id=course_id,
                )
                messagebox.showinfo("Success", "Successfully delete Student info")
                self.clear_data()
            except Exception as e:
                messagebox.showerror("Delete Operation Failed", str(e))

    def search_courses(self):
        '''Student searching main logic goes here.'''
        search_field = self.searchbox_entry.get()
        dropdown_data = self.dropdown_value.get()
        self.clear_data()
        results = db_operation.admin_view_courses(
            search_key=search_field,
            sort_key="c.course_number",
            filter_key=self.column_replace[dropdown_data],
            all=False
        )
        # (course_number, course_name, professor_id)
        if results:
            print(results)
            self.course_id_entry.config(state="normal")
            for idx, entry in enumerate(self.get_input_list()):
                entry.insert(END, results[idx])
        self.course_id_entry.config(state="disabled")

    def modify_professor_data(self):
        '''This function invokes when the okay button is pressed.'''
        course_id = self.course_id_entry.get()
        course_name = self.course_name_entry.get()
        professor_id = self.professor_id_entry.get()

        # writing the student data
        try:
            db_operation.admin_view_update_course(
                course_id=course_id,
                course_name=course_name,
                professor_id=professor_id,
            )
            self.clear_data()
            messagebox.showinfo("Success", "Successfully Updated the Student info.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
