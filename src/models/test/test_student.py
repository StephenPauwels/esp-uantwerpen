from unittest import TestCase
from src.models.db import *
from src.models.student import *
from src.config import *


class TestStudentDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Student Connection: OK")

    def test_get_students(self):
        connection = self._connect()
        dao = StudentDataAccess(dbconnect=connection)
        object = dao.get_students()
        self.assertEqual('Viet Aal'.upper(),
                         object[0].name.upper())
        connection.close()

    def test_get_student(self):
        connection = self._connect()
        dao = StudentDataAccess(dbconnect=connection)
        object = dao.get_student('1')
        self.assertEqual('Viet Aal'.upper(),
                         object.name.upper())
        connection.close()

    def test_add_student(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from student where name=\'test_ins\'')
        connection.get_connection().commit()
        dao = StudentDataAccess(dbconnect=connection)
        obj = Student(student_name='test_ins', student_id='2')
        dao.add_student(obj)
        object = dao.get_student('2')
        self.assertEqual('test_ins'.upper(),
                         object.name.upper())
        connection.get_cursor().execute('DELETE from student where name=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()
