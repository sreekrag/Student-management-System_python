from application.lib import students


class HandleUserInputs:

    def __init__(self):
        self.student_bean = students.StudentsBean()
        self.student = students.ProcessStudentDetails()
        self.data_keys = ['student_id', 'first_name', 'last_name', 'major', 'phone', 'gpa', 'date_of_birth']

    def add_student(self):
        self.student_id = input('Enter Student ID:')
        self.first_name = input('Enter Student First Name:')
        self.last_name = input('Enter Student Last Name:')
        self.major = input('Enter Student Major:')
        self.phone = input('Enter Student Phone:')
        self.gpa = input('Enter Student GPA:')
        self.date_of_birth = input('Enter Student DOB:')

        self.student_bean.set_student_details(self.student_id, self.first_name, self.last_name, self.major, self.phone, self.gpa, self.date_of_birth)
        student_object = self.student_bean.get_student_object()
        self.student.save_student_details(student_object)

    def search_student(self, search_field, search_key):
        student_details = self.student.get_students_details()
        result = []
        if len(student_details) > 0:
            keys = [* student_details[0].keys()]
            result = [student for student in student_details if student[keys[search_field-1]] == search_key]
            
        return result

    def get_students_list(self):
        student_details = self.student.get_students_details()
        return student_details

    def sort_students(self):
        print('SELECT FIELD SORT')
        print('1. STUDENT ID')
        print('2. FIRST NAME')
        print('3. LAST NAME')
        print('4. MAJOR')
        print('5. PHONE')
        print('6. GPA')
        print('7. DATE OF BIRTH')
        sort_field = int(input('Choose :'))
        sort_order = input('Enter sort order(ASC or DESC): ')
        student_details = self.student.get_students_details()
        keys = [* student_details[0].keys()]
        result = sorted(student_details, key = lambda i: i[keys[sort_field - 1]],reverse= (sort_order == 'DESC'))
        return result

    def update_student_details(self):
        result = self.search_student()
        if len(result) >0 :
            self.print_result(result)
            self.first_name = input('Enter Student First Name:')
            self.last_name = input('Enter Student Last Name:')
            self.major = input('Enter Student Major:')
            self.phone = input('Enter Student Phone:')
            self.gpa = input('Enter Student GPA:')
            self.date_of_birth = input('Enter Student DOB:')

            self.student_bean.set_student_details(result[0].get('student_id'), self.first_name, self.last_name, self.major, self.phone, self.gpa, self.date_of_birth)
            student_object = self.student_bean.get_student_object()
            self.student.update_student_details(student_object)
        else:
            print('No Student with given details found')


    def print_result(self, results):
        print('STUDENT ID\t FIRST NAME\t LAST NAME\t MAJOR\t PHONE\t GPA\t DATE OF BIRTH\n')
        for student_obj in results:
            print('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(student_obj.get('student_id'),student_obj.get('first_name'),student_obj.get('last_name'),student_obj.get('major'),student_obj.get('phone'),student_obj.get('gpa'),student_obj.get('date_of_birth')))
        print('\n\n')
        return





# handle_user_input = HandleUserInputs()

# while True:
#     print('______ STUDENTS MANAGEMENT ______')
#     print('1. ADD NEW STUDENT')
#     print('2. SEARCH STUDENT')
#     print('3. VIEW STUDENTS LIST')
#     print('4. SORT STUDENTS LIST')
#     print('5. UPDATE STUDENTS')
#     print('6. EXIT')
#     print('select your choice: ')
#     selection =  input()
#     if selection == '1':
#         handle_user_input.add_student()
#     elif selection == '2':
#         search_result = handle_user_input.search_student()
#         handle_user_input.print_result(search_result)
#     elif selection == '3':
#         student_list = handle_user_input.get_students_list()
#         handle_user_input.print_result(student_list)
#     elif selection == '4':
#         sorted_list = handle_user_input.sort_students()
#         handle_user_input.print_result(sorted_list)
#     elif selection == '5':
#         handle_user_input.update_student_details()
#         student_list = handle_user_input.get_students_list()
#         handle_user_input.print_result(student_list)
#     elif selection == '6':
#         break
#     else :
#         print('wrong selection try again')
