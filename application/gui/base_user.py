


class BaseUser:


    def create_input_layout(self):
        # student id
        student_id_frame = ttk.Frame(self.frame)
        student_id_frame.pack(fill=X)
        student_id_label = Label(student_id_frame, text="StudentID", width=15)
        student_id_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.student_id_entry = Entry(student_id_frame, validate="key", validatecommand=(
            self.student_id_validator, "%P"))
        self.student_id_entry.pack(fill=X, padx=(5, 100), expand=True)

        # first name
        first_name_frame = ttk.Frame(self.frame)
        first_name_frame.pack(fill=X)
        first_name_label = Label(first_name_frame, text="First Name", width=15)
        first_name_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.first_name_entry = Entry(first_name_frame)
        self.first_name_entry.pack(fill=X, padx=(5, 100), expand=True)

        # last name
        last_name_frame = ttk.Frame(self.frame)
        last_name_frame.pack(fill=X)
        last_name_label = Label(last_name_frame, text="Last Name", width=15)
        last_name_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.last_name_entry = Entry(last_name_frame)
        self.last_name_entry.pack(fill=X, padx=(5, 100), expand=True)

        # major
        major_frame = ttk.Frame(self.frame)
        major_frame.pack(fill=X)
        major_label = Label(major_frame, text="Major", width=15)
        major_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.major_entry = Entry(major_frame)
        self.major_entry.pack(fill=X, padx=(5, 100), expand=True)

        # phone
        phone_frame = ttk.Frame(self.frame)
        phone_frame.pack(fill=X)
        phone_label = Label(phone_frame, text="Phone", width=15)
        phone_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.phone_entry = Entry(phone_frame)
        self.phone_entry.pack(fill=X, padx=(5, 100), expand=True)

        # gpa
        gpa_frame = ttk.Frame(self.frame)
        gpa_frame.pack(fill=X)
        gpa_label = Label(gpa_frame, text="GPA", width=15)
        gpa_label.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.gpa_entry = Entry(gpa_frame, validate="key",
                               validatecommand=(self.gpa_validator, "%P"))
        self.gpa_entry.pack(fill=X, padx=(5, 100), expand=True)

        # date of birth
        dob_frame = ttk.Frame(self.frame)
        dob_frame.pack(fill=X)
        dob_label = Label(dob_frame, text="Date of Birth", width=15)
        dob_label.pack(side=LEFT, padx=10, pady=5)
        self.dob_entry = Entry(dob_frame)
        self.dob_entry.pack(fill=X, padx=(5, 100), expand=True)
