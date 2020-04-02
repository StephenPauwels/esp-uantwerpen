from unittest import TestCase
from src.models.db import *
from src.models.click import *
from src.models.session import *
from src.config import *


class TestClickDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Document Connection: OK")

    def test_add_project_click(self):
        connection = self._connect()
        dao = ClickDataAccess(dbconnect=connection)
        connection.get_cursor().execute('DELETE from project_click where project=2')
        connection.get_connection().commit()
        dao.add_project_click(2, 2)
        # print(objects[-1].to_dct())
        dao2 = SessionDataAccess(dbconnect=connection)
        object = dao2.get_student_clicks('3')
        # print(objects[-1].to_dct())
        self.assertEqual(1, object[2])
        connection.close()
