from unittest import TestCase
from src.models.db import *
from src.models.tag import *
from src.config import *


class TestTagDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Tag Connection: OK")

    def test_get_tags(self):
        connection = self._connect()
        dao = TagDataAccess(dbconnect=connection)
        objects = dao.get_tags()
        self.assertEqual('test_tag'.upper(),
                         objects[-1].upper())
        connection.close()

    def test_add_tag(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from tag where tag=\'test_ins\'')
        connection.get_connection().commit()
        dao = TagDataAccess(dbconnect=connection)
        dao.add_tag('test_ins')
        objects = dao.get_tags()
        self.assertEqual('test_ins'.upper(),
                         objects[-1].upper())
        connection.get_cursor().execute('DELETE from tag where tag=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_remove_tag(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from tag where tag=\'test_ins\'')
        connection.get_connection().commit()
        dao = TagDataAccess(dbconnect=connection)
        dao.add_tag('test_ins')
        objects = dao.get_tags()
        self.assertEqual('test_ins'.upper(),
                         objects[-1].upper())
        dao.remove_tag('test_ins')
        objects = dao.get_tags()
        self.assertNotEqual('test_ins'.upper(),
                         objects[-1].upper())
        connection.get_cursor().execute('DELETE from tag where tag=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_update_tag(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from tag where tag=\'test_ins\'')
        connection.get_connection().commit()
        dao = TagDataAccess(dbconnect=connection)
        dao.add_tag('test_ins')
        objects = dao.get_tags()
        self.assertEqual('test_ins'.upper(),
                         objects[-1].upper())
        dao.update_tag('test_ins', 'test_ins2')
        objects = dao.get_tags()
        self.assertEqual('test_ins2'.upper(),
                            objects[-1].upper())
        connection.get_cursor().execute('DELETE from tag where tag=\'test_ins2\'')
        connection.get_connection().commit()
        connection.close()
