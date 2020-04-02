import unittest
from src.models.db import *
from src.models.academic_year import *
from src.config import *


class TestAcademicYearDataAccess(unittest.TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Academic Year Connection: OK")

    def test_get_academic_years(self):
        connection = self._connect()
        dao = AcademicYearDataAccess(dbconnect=connection)
        objects = dao.get_academic_years()
        # print(objects[-1].to_dct())
        self.assertEqual(2021,
                         objects[-1])
        connection.close()

    def test_add_academic_year(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from academic_year where year=2027')
        connection.get_connection().commit()
        dao = AcademicYearDataAccess(dbconnect=connection)
        dao.add_academic_year(2027)
        objects = dao.get_academic_years()
        # print(objects[-1].to_dct())
        self.assertEqual(2027,
                         objects[-1])
        connection.get_cursor().execute('DELETE from academic_year where year=2027')
        connection.get_connection().commit()
        connection.close()

    def test_domain_year(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from academic_year where year=2000')
        connection.get_connection().commit()
        dao = AcademicYearDataAccess(dbconnect=connection)
        dao.add_academic_year(2000)
        connection.get_cursor().execute('DELETE from academic_year where year=1999')
        connection.get_connection().commit()

        with self.assertRaises(Exception) as context:
            dao.add_academic_year(1999)
        self.assertTrue('' in str(context.exception),
                        'year exception for not null is_active not raised or wrong exception')
        connection.get_cursor().execute('DELETE from academic_year where year=2000')
        connection.get_connection().commit()
        connection.close()

