from unittest import TestCase
from src.models.db import *
from src.models.type import *
from src.config import *


class TestTypeDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Type Connection: OK")

    def test_get_types(self):
        connection = self._connect()
        dao = TypeDataAccess(dbconnect=connection)
        objects = dao.get_types(True)
        self.assertEqual('test_type'.upper(),
                         objects[0].type_name.upper())
        connection.close()

    def test_add_type(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from type where type_name=\'test_ins\'')
        connection.get_connection().commit()
        dao = TypeDataAccess(dbconnect=connection)
        obj = Type(type_name='test_ins', active=True)
        dao.add_type(obj)
        objects = dao.get_types(True)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].type_name.upper())
        connection.get_cursor().execute('DELETE from type where type_name=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_remove_type(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from type where type_name=\'test_ins\'')
        connection.get_connection().commit()
        dao = TypeDataAccess(dbconnect=connection)
        obj = Type(type_name='test_ins', active=True)
        dao.add_type(obj)
        objects = dao.get_types(True)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].type_name.upper())
        dao.remove_type('test_ins')
        objects = dao.get_types(True)
        self.assertNotEqual('test_ins'.upper(),
                         objects[-1].type_name.upper())
        connection.get_cursor().execute('DELETE from type where type_name=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_update_type(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from type where type_name=\'test_ins\'')
        connection.get_connection().commit()
        dao = TypeDataAccess(dbconnect=connection)
        obj = Type(type_name='test_ins', active=True)
        dao.add_type(obj)
        objects = dao.get_types(True)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].type_name.upper())
        obj = Type(type_name='test_ins2', active=True)
        dao.update_type('test_ins', obj)
        objects = dao.get_types(True)
        self.assertEqual('test_ins2'.upper(),
                         objects[-1].type_name.upper())
        connection.get_cursor().execute('DELETE from type where type_name=\'test_ins2\'')
        connection.get_connection().commit()
        connection.close()

    def test_set_active(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from type where type_name=\'test_ins\'')
        connection.get_connection().commit()
        dao = TypeDataAccess(dbconnect=connection)
        obj = Type(type_name='test_ins', active=True)
        dao.add_type(obj)
        objects = dao.get_types(True)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].type_name.upper())
        self.assertTrue(objects[-1].is_active)
        obj = Type(type_name='test_ins', active=False)
        dao.set_active('test_ins', False)
        objects = dao.get_types(False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].type_name.upper())
        self.assertFalse(objects[-1].is_active)
        connection.get_cursor().execute('DELETE from type where type_name=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()
