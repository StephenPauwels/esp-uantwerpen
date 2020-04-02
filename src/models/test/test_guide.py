from unittest import TestCase
from src.models.db import *
from src.models.guide import *
from src.config import *


class TestGuideDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Guide Connection: OK")

    def test_get_guides_for_project(self):
        connection = self._connect()
        dao = GuideDataAccess(dbconnect=connection)
        objects = dao.get_guides_for_project(1)
        self.assertEqual(1,
                         objects[0].employee)

        connection.close()

    def test_add_guide(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from guide where employee=2')
        connection.get_connection().commit()
        dao = GuideDataAccess(dbconnect=connection)
        obj = Guide(2, 1, 'Promotor')
        dao.add_guide(obj)
        objects = dao.get_guides_for_project(1)
        self.assertEqual(2,
                         objects[-1].employee)
        connection.get_cursor().execute('DELETE from guide where employee=2')
        connection.get_connection().commit()

        connection.close()

    def test_get_guides_project_info(self):
        connection = self._connect()
        dao = GuideDataAccess(dbconnect=connection)
        objects = dao.get_guides_project_info('D Trump')
        self.assertEqual(1,
                         objects[0]['project_id'])

        connection.close()

    def test_get_projects_for_employee(self):
        connection = self._connect()
        dao = GuideDataAccess(dbconnect=connection)
        objects = dao.get_projects_for_employee(1)
        self.assertEqual(1,
                         objects[0]['project_id'])

        connection.close()

    def test_remove_project_guides(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from guide where employee=2')
        connection.get_connection().commit()
        dao = GuideDataAccess(dbconnect=connection)
        obj = Guide(2, 2, 'Promotor')
        dao.add_guide(obj)
        objects = dao.get_guides_for_project(2)
        self.assertGreater(len(objects), 0)
        dao.remove_project_guides(2)
        objects = dao.get_guides_for_project(2)
        self.assertEqual(len(objects), 0)
        connection.get_cursor().execute('DELETE from guide where employee=2')
        connection.get_connection().commit()

        connection.close()

    def test_remove_guide(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from guide where employee=2')
        connection.get_connection().commit()
        dao = GuideDataAccess(dbconnect=connection)
        obj = Guide(2, 2, 'Promotor')
        dao.add_guide(obj)
        objects = dao.get_guides_for_project(2)
        self.assertEqual(len(objects), 1)
        dao.remove_guide(2,2)
        objects = dao.get_guides_for_project(2)
        self.assertEqual(len(objects), 0)
        connection.get_cursor().execute('DELETE from guide where employee=2')
        connection.get_connection().commit()

        connection.close()

    def test_domain_types(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from guide where employee=2')
        connection.get_connection().commit()
        dao = GuideDataAccess(dbconnect=connection)
        obj1 = Guide(employee=2, project=1, guidance_type='Promotor')
        dao.add_guide(obj1)
        obj2 = Guide(employee=2, project=1, guidance_type='Co-Promotor')
        dao.add_guide(obj2)
        obj3 = Guide(employee=2, project=1, guidance_type='Mentor')
        dao.add_guide(obj3)
        obj4 = Guide(employee=2, project=1, guidance_type=None)
        obj5 = Guide(employee=2, project=1, guidance_type='Other')

        with self.assertRaises(Exception) as context:
            dao.add_guide(obj4)
        self.assertTrue('' in str(context.exception),
                        'guides exception for domain type not raised or wrong exception')

        with self.assertRaises(Exception) as context:
            dao.add_guide(obj5)
        self.assertTrue('' in str(context.exception),
                        'guides exception for domain type not raised or wrong exception')
