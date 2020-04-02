from unittest import TestCase
from src.models.db import *
from src.models.registration import *
from src.config import *


class TestRegistrationDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Registration Connection: OK")

    def test_get_registrations(self):
        connection = self._connect()
        dao = RegistrationDataAccess(dbconnect=connection)
        object = dao.get_registration('1', 1)
        self.assertEqual('1'.upper(),
                         object.student.upper())
        self.assertEqual('Pending'.upper(),
                         object.status.upper())
        connection.close()

    def test_get_registration(self):
        connection = self._connect()
        dao = RegistrationDataAccess(dbconnect=connection)
        objects = dao.get_registrations()
        self.assertEqual('1'.upper(),
                         objects[0].student.upper())
        self.assertEqual('Pending'.upper(),
                         objects[0].status.upper())
        connection.close()

    def test_get_pending_registrations(self):
        connection = self._connect()
        dao = RegistrationDataAccess(dbconnect=connection)
        objects = dao.get_pending_registrations(1)
        self.assertEqual('1'.upper(),
                         objects[0]['student'].upper())
        self.assertEqual('Viet Aal'.upper(),
                         objects[0]['name'].upper())
        connection.close()

    def test_add_registration(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from project_registration where student=\'3\'')
        connection.get_connection().commit()
        dao = RegistrationDataAccess(dbconnect=connection)
        obj = Registration(student_id='3', project_id=1, status='Passed')
        dao.add_registration(obj)
        object = dao.get_registration('3', 1)
        self.assertEqual('3'.upper(),
                         object.student.upper())
        self.assertEqual('Passed'.upper(),
                         object.status.upper())
        connection.get_cursor().execute('DELETE from project_registration where student=\'3\'')
        connection.get_connection().commit()
        connection.close()

    def test_update_registration(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from project_registration where student=\'3\'')
        connection.get_connection().commit()
        dao = RegistrationDataAccess(dbconnect=connection)
        obj = Registration(student_id='3', project_id=1, status='Pending')
        dao.add_registration(obj)
        object = dao.get_registration('3', 1)
        self.assertEqual('3'.upper(),
                         object.student.upper())
        self.assertEqual('Pending'.upper(),
                         object.status.upper())
        dao.update_registration('3',1,'Passed')
        object = dao.get_registration('3', 1)
        self.assertEqual('3'.upper(),
                         object.student.upper())
        self.assertEqual('Passed'.upper(),
                         object.status.upper())
        connection.get_cursor().execute('DELETE from project_registration where student=\'3\'')
        connection.get_connection().commit()
        connection.close()

    def test_delete_registration(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from project_registration where student=\'3\'')
        connection.get_connection().commit()
        dao = RegistrationDataAccess(dbconnect=connection)
        obj = Registration(student_id='3', project_id=1, status='Passed')
        dao.add_registration(obj)
        objects1 = dao.get_registrations()
        dao.delete_registration('3')
        objects2 = dao.get_registrations()
        self.assertGreater(len(objects1), len(objects2))

        connection.get_cursor().execute('DELETE from project_registration where student=\'3\'')
        connection.get_connection().commit()
        connection.close()

    def test_domain_status(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from Project_Registration where student=\'3\'')
        connection.get_connection().commit()
        dao = RegistrationDataAccess(dbconnect=connection)
        obj1 = Registration(student_id='3', project_id=1, status='Failed')
        dao.add_registration(obj1)
        connection.get_cursor().execute('DELETE from Project_Registration where student=\'3\'')
        connection.get_connection().commit()

        obj2 = Registration(student_id='3', project_id=1, status='Pending')
        dao.add_registration(obj2)
        connection.get_cursor().execute('DELETE from Project_Registration where student=\'3\'')
        connection.get_connection().commit()

        obj3 = Registration(student_id='3', project_id=1, status='Passed')
        dao.add_registration(obj3)
        connection.get_cursor().execute('DELETE from Project_Registration where student=\'203182020\'')
        connection.get_connection().commit()

        obj4 = Registration(student_id='3', project_id=1, status='Progress')
        obj5 = Registration(student_id='3', project_id=1, status=None)

        with self.assertRaises(Exception) as context:
            dao.add_registration(obj4)
        self.assertTrue('' in str(context.exception),
                        'project registration exception for domain status not raised or wrong exception')
        connection.get_cursor().execute('DELETE from Project_Registration where student=\'20182020\'')
        connection.get_connection().commit()

        with self.assertRaises(Exception) as context:
            dao.add_registration(obj5)
        self.assertTrue('' in str(context.exception),
                        'project registration exception for domain status not raised or wrong exception')
