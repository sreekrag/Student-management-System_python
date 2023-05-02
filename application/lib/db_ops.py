from hashlib import sha3_256
import mysql.connector as mysql

from application.lib.constants import SALT


class DbOperations:

    def __init__(self):
        self.connection = self.get_connection()

    def get_hashed_password(self, password):
        return sha3_256(f"{password}{SALT}".encode()).hexdigest()

    def get_connection(self):
        return mysql.connect(
            host="localhost",
            user="root",
            passwd="toor",
            database="student_app"
        )

    def check_login(
            self,
            username,
            user_type,
    ):
        cursor = self.connection.cursor()
        query = f"""
            SELECT password, id, username, email_id, first_name, last_name FROM Users WHERE username='{username}' AND user_type={user_type}
        """
        cursor.execute(query)
        records = cursor.fetchone()
        return records


    def admin_add_student(
            self,
            student_number,
            first_name,
            last_name,
            email_id,
            username,
            password,
    ):

        hashed_passwd = self.get_hashed_password(password)
        query1 = f"""
            INSERT INTO Users(first_name, last_name, username, password, email_id, user_type) 
            VALUES ('{first_name}', '{last_name}', '{username}', '{hashed_passwd}', '{email_id}', 3)
        """
        query2 = """
            INSERT INTO Students(user_id, student_number)
            VALUES (%s, %s)
        """
        cursor = self.connection.cursor()
        q1_result = cursor.execute(query1)
        user_id = cursor.lastrowid
        values = (user_id, f"{student_number}")
        q2_result = cursor.execute(query2, values)
        self.connection.commit()
        cursor.close()
        return True


    def admin_view_students(
            self,
            search_key,
            sort_key,
            filter_key,
            all=True,
    ):
        if not search_key.strip():
            # get all the data from db, sort by sort key, limit 10
            query = f"""
                SELECT usr.id, s.student_number, usr.username, usr.first_name , usr.last_name, usr.email_id FROM Students s 
                JOIN Users usr 
                ON s.user_id = usr.id 
                ORDER BY {sort_key}
                LIMIT 10
                ;
            """
        else:
            query = f"""
                SELECT usr.id, s.student_number, usr.username, usr.first_name , usr.last_name, usr.email_id FROM Students s 
                JOIN Users usr 
                ON s.user_id = usr.id 
                WHERE {filter_key} LIKE '%{search_key}%'
                ORDER BY {sort_key}
                LIMIT 10
                ;
            """
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(query)
        if all:
            records = cursor.fetchall()
        else:
            records = cursor.fetchone()
        cursor.close()
        return records


    def admin_view_update_students(
            self,
            user_id,
            username,
            password,
            first_name,
            last_name,
            email_id,
            studnet_id
    ):
        if not password:
            query = f"""
                UPDATE Students s JOIN Users usr ON (s.user_id = usr.id)
                SET 
                    usr.username = '{username}',
                    usr.first_name = '{first_name}',
                    usr.last_name = '{last_name}',
                    usr.email_id = '{email_id}',
                    s.student_number = '{studnet_id}'
                WHERE usr.id = {user_id}
            """
        else:
            hashed_password = self.get_hashed_password(password)
            query = f"""
                UPDATE Students s JOIN Users usr ON (s.user_id = usr.id)
                SET 
                    usr.username = '{username}',
                    usr.password = '{hashed_password}',
                    usr.first_name = '{first_name}',
                    usr.last_name = '{last_name}',
                    usr.email_id = '{email_id}',
                    s.student_number = '{studnet_id}'
                WHERE usr.id = {user_id}
            """
        print(query)
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return True


    def admin_delete_student(self, user_id, student_id):
        query = f"""
            DELETE FROM Users
                WHERE (
                    id = {user_id} 
                AND 
                    {student_id} NOT IN (SELECT student_id from Grade)
                )
        """
        print(query)
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return True


    def admin_add_professor(
            self,
            employee_id,
            first_name,
            last_name,
            email_id,
            username,
            password,
    ):
        hashed_passwd = self.get_hashed_password(password)
        query1 = f"""
            INSERT INTO Users(first_name, last_name, username, password, email_id, user_type) 
            VALUES ('{first_name}', '{last_name}', '{username}', '{hashed_passwd}', '{email_id}', 2)
        """
        query2 = """
            INSERT INTO Professors(user_id, employee_number)
            VALUES (%s, %s)
        """
        cursor = self.connection.cursor()
        cursor.execute(query1)
        user_id = cursor.lastrowid
        values = (user_id, f"{employee_id}")
        cursor.execute(query2, values)
        self.connection.commit()
        cursor.close()


    def admin_view_professor(
            self,
            search_key,
            sort_key,
            filter_key,
            all=True,
    ):
        if not search_key.strip():
            # get all the data from db, sort by sort key, limit 10
            query = f"""
                SELECT usr.id, p.employee_number, usr.username, usr.first_name , usr.last_name, usr.email_id FROM Professors p
                JOIN Users usr 
                ON p.user_id = usr.id 
                ORDER BY {sort_key}
                LIMIT 10
                ;
            """
        else:
            query = f"""
                SELECT usr.id, p.empoloyee_number, usr.username, usr.first_name , usr.last_name, usr.email_id FROM Professors p
                JOIN Users usr 
                ON p.user_id = usr.id 
                WHERE {filter_key} LIKE '%{search_key}%'
                ORDER BY {sort_key}
                LIMIT 10
                ;
            """
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(query)
        if all:
            records = cursor.fetchall()
        else:
            records = cursor.fetchone()
        cursor.close()
        return records


    def admin_view_update_professors(
            self,
            user_id,
            username,
            password,
            first_name,
            last_name,
            email_id,
            employee_id
    ):
        if not password:
            query = f"""
                UPDATE Professors p JOIN Users usr ON (p.user_id = usr.id)
                SET 
                    usr.username = '{username}',
                    usr.first_name = '{first_name}',
                    usr.last_name = '{last_name}',
                    usr.email_id = '{email_id}',
                    p.employee_number = '{employee_id}'
                WHERE usr.id = {user_id}
            """
        else:
            hashed_password = self.get_hashed_password(password)
            query = f"""
                UPDATE Professors p JOIN Users usr ON (p.user_id = usr.id)
                SET 
                    usr.username = '{username}',
                    usr.password = '{hashed_password}',
                    usr.first_name = '{first_name}',
                    usr.last_name = '{last_name}',
                    usr.email_id = '{email_id}',
                    p.employee_number = '{empolyee_id}'
                WHERE usr.id = {user_id}
            """
        print(query)
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return True


    def admin_delete_professor(self, user_id, employee_id):
        query = f"""
            DELETE FROM Users
                WHERE (
                    id = {user_id} 
                AND 
                    {employee_id} NOT IN (SELECT professor_id from Grade)
                )
        """
        print(query)
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return True

    def admin_add_course(
            self,
            course_id,
            course_name,
            professor_id,
    ):
        query = f"""
            INSERT INTO Course(course_number, course_name, professor_id) 
            VALUES ({course_id}, '{course_name}', 
                (
                    SELECT user_id FROM Professors where user_id={professor_id}
                )
            )
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        user_id = cursor.lastrowid
        self.connection.commit()
        cursor.close()


    def admin_view_courses(
            self,
            search_key,
            sort_key,
            filter_key,
            all=True,
    ):
        if not search_key.strip():
            # get all the data from db, sort by sort key, limit 10
            query = f"""
                SELECT c.course_number, c.course_name, p.user_id FROM Professors p
                JOIN Course c
                ON p.user_id = c.professor_id
                ORDER BY {sort_key}
                LIMIT 10
                ;
            """
        else:
            query = f"""
                SELECT c.course_number, c.course_name, p.user_id FROM Professors p
                JOIN Course c
                ON p.user_id = c.professor_id
                WHERE {filter_key} LIKE '%{search_key}%'
                ORDER BY {sort_key}
                LIMIT 10
                ;
            """
        print(query)
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(query)
        if all:
            records = cursor.fetchall()
        else:
            records = cursor.fetchone()
        cursor.close()
        return records


    def admin_view_update_course(
            self,
            course_id,
            course_name,
            professor_id,
    ):
        if not password:
            query = f"""
                UPDATE Professors p JOIN Course c ON (p.user_id = c.professor_id)
                SET 
                    c.course_name= '{course_name}',
                    p.user_id = {professor_id}
                WHERE c.course_number = {course_id}
            """
        else:
            hashed_password = self.get_hashed_password(password)
            query = f"""
                UPDATE Professors p JOIN Users usr ON (p.user_id = usr.id)
                SET 
                    usr.username = '{username}',
                    usr.password = '{hashed_password}',
                    usr.first_name = '{first_name}',
                    usr.last_name = '{last_name}',
                    usr.email_id = '{email_id}',
                    p.employee_number = '{empolyee_id}'
                WHERE usr.id = {user_id}
            """
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return True


    def admin_delete_course(self, course_id):
        query = f"""
            DELETE FROM Course
                WHERE (
                    course_number = {course_id} 
                AND 
                    {course_id} NOT IN (SELECT course_id from Grade)
                )
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return True


    def add_grades(
            self,
            student_id,
            student_first_name,
            student_last_name,
            course_id,
            course_name,
            grade,
            prof_user_id,
    ):
        student_select_query = f"""
            SELECT u.first_name, u.last_name FROM Users u
            JOIN Students s ON s.user_id = u.id
            WHERE s.student_number = {student_id}
        """
        course_select_query = f"""
            SELECT course_name FROM Course WHERE course_number = {course_id}
        """
        grade_query = f"""
            INSERT INTO Grade(course_id, student_id, professor_id, grade)
            VALUES ({course_id}, 
                    (SELECT user_id FROM Students where student_number = {student_id}), 
                    {prof_user_id}, {grade})
        """
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(student_select_query)
        student_data = cursor.fetchone()
        if not (student_first_name == student_data[0] and student_last_name == student_data[1]):
            cursor.close()
            raise Exception(f"Given {student_first_name}, {student_last_name} and {student_id} combination mismatch found.")
        cursor.execute(course_select_query)
        course_data = cursor.fetchone()
        if not (course_name == course_data[0]):
            cursor.close()
            raise Exception(f"Given {course_id} and {course_name} not matching.")
        cursor.execute(grade_query)
        self.connection.commit()
        cursor.close()
        return True

    def get_student_grades(self, user_id):
        query = f"""
            SELECT c.course_number, c.course_name, g.grade FROM Grade g
            JOIN Course c 
            ON g.course_id = c.course_number
            WHERE g.student_id = {user_id}
        """
        print(query)
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        return records

db_operation = DbOperations()