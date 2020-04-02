from unittest import TestCase
from src.models.db import *
from src.models.link import *
from src.config import *


class TestLinkDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Link Connection: OK")

    def test_get_links(self):
        connection = self._connect()
        dao = LinkDataAccess(dbconnect=connection)
        objects = dao.get_links()
        self.assertEqual(1, objects[0].project_1)
        self.assertEqual(2,
                         objects[0].project_2)
        connection.close()

    def test_get_link(self):
        connection = self._connect()
        dao = LinkDataAccess(dbconnect=connection)
        object = dao.get_link(1,2)
        self.assertEqual(1, object.project_1)
        self.assertEqual(2,
                         object.project_2)
        connection.close()

    def test_get_links_for_project(self):
        connection = self._connect()
        dao = LinkDataAccess(dbconnect=connection)
        objects = dao.get_links_for_project(1)
        self.assertEqual(1, objects[0].project_1)
        self.assertEqual(2,
                         objects[0].project_2)
        connection.close()

    def test_add_link(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from link where project_2=3')
        connection.get_connection().commit()
        dao = LinkDataAccess(dbconnect=connection)
        obj = Link(2, 3, 0.12)
        dao.add_link(obj)
        objects = dao.get_links()
        self.assertEqual(2, objects[-1].project_1)
        self.assertEqual(3,
                         objects[-1].project_2)
        connection.get_cursor().execute('DELETE from link where project_2=3')
        connection.get_connection().commit()
        connection.close()

    def test_update_match_percent(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from link where project_2=3')
        connection.get_connection().commit()
        dao = LinkDataAccess(dbconnect=connection)
        obj = Link(2, 3, 0.12)
        dao.add_link(obj)
        objects = dao.get_links()
        self.assertAlmostEqual(0.12, objects[-1].match_percent, delta=0.1)
        dao.update_match_percent(2,3, 0.5)
        objects = dao.get_links()
        self.assertAlmostEqual(0.52, objects[-1].match_percent, delta=0.1)
        connection.get_cursor().execute('DELETE from link where project_2=3')
        connection.get_connection().commit()
        connection.close()

    def test_domain_match_percent(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from link where project_2=3')
        connection.get_connection().commit()
        dao = LinkDataAccess(dbconnect=connection)
        obj = Link(2, 3, 0.12)
        dao.add_link(obj)
        connection.get_cursor().execute('DELETE from link where project_2=3')
        connection.get_connection().commit()
        obj = Link(2, 3, 0)
        dao.add_link(obj)
        connection.get_cursor().execute('DELETE from link where project_2=3')
        connection.get_connection().commit()
        obj = Link(2, 3, 1)
        dao.add_link(obj)
        connection.get_cursor().execute('DELETE from link where project_2=3')
        connection.get_connection().commit()
        obj = Link(2, 3, 1.1)

        with self.assertRaises(Exception) as context:
            dao.add_link(obj)
        self.assertTrue('' in str(context.exception),
                        'employee exception for not null is_active not raised or wrong exception')
        connection.close()
