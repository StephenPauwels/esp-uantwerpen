from unittest import TestCase
from src.models.db import *
from src.models.session import *
from src.config import *


class TestSessionDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Session Connection: OK")

    def test_get_sessions(self):
        connection = self._connect()
        dao = SessionDataAccess(dbconnect=connection)
        objects = dao.get_sessions()
        self.assertEqual('1',
                         objects[0].student)
        connection.close()

    def test_get_session(self):
        connection = self._connect()
        dao = SessionDataAccess(dbconnect=connection)
        object = dao.get_session(1)
        self.assertEqual('1',
                         object.student)
        connection.close()

    def test_add_session(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from session where student=\'3\'')
        connection.get_connection().commit()
        dao = SessionDataAccess(dbconnect=connection)
        obj = Session(session_id=None, student='3', start_of_session='1/8/2019')
        dao.add_session(obj)
        objects = dao.get_sessions()
        self.assertEqual('3',
                         objects[-1].student)
        connection.get_cursor().execute('DELETE from session where student=\'3\'')
        connection.get_connection().commit()
        connection.close()

    def test_get_student_clicks(self):
        connection = self._connect()
        dao = SessionDataAccess(dbconnect=connection)
        object = dao.get_student_clicks('1')
        self.assertEqual(1, object[1])
        connection.close()
