"""@package
This package enables the student usage for the database.
"""


class Student:
    """
    This class defines a student.
    """

    def __init__(self, student_name, student_id):
        """
        Student initializer.
        :param student_name: The name of the student.
        :param student_id: The ID of the student.
        """
        self.name = student_name
        self.student_id = student_id

    def to_dict(self):
        """
        Converts object to a dictionary.
        :return: Dictionary of the object data.
        """
        return vars(self)


class StudentDataAccess:
    """
    This class interacts with the Student component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initiates the StudentDataAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def get_students(self):  # TODO #2 catching empty fetch?
        """
        Fetches all the students from the database.
        :return: A list with all the students.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT name, student_id FROM student')
        return [Student(row[0], row[1]) for row in cursor]

    def get_student(self, student_id):  # TODO #2 catching empty fetch?
        """
        Fetches a specific student from the database.
        :param student_id: The student ID from the student to fecth.
        :return: The fetched student object.
        """
        cursor = self.dbconnect.get_cursor()

        try:
            cursor.execute('SELECT name, student_id FROM student WHERE student_id=%s', (student_id,))
            row = cursor.fetchone()
            return Student(row[0], row[1])
        except:
            self.dbconnect.rollback()
            raise

    def add_student(self, obj):  # TODO #1 objects instead of data
        """
        Adds a student to the database.
        :param obj: The new student.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO student(name, student_id) VALUES(%s,%s)',
                           (obj.name, obj.student_id))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise
