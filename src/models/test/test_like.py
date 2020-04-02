from unittest import TestCase
from src.models.db import *
from src.models.like import *
from src.config import *


class TestLikeDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Like Connection: OK")

    def test_is_liked(self):
        connection = self._connect()
        dao = LikeDataAccess(dbconnect=connection)
        object = dao.is_liked(1, '1')
        self.assertTrue(object)
        object = dao.is_liked(2, '1')
        self.assertFalse(object)
        connection.close()

    def test_add_like(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from "like" where student=\'3\'')
        connection.get_connection().commit()
        dao = LikeDataAccess(dbconnect=connection)
        obj = Like('3', 1)
        dao.add_like(obj)
        object = dao.is_liked(1, '3')
        self.assertTrue(object)
        connection.get_cursor().execute('DELETE from "like" where student=\'3\'')
        connection.get_connection().commit()
        connection.close()

    def test_remove_like(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from "like" where student=\'3\'')
        connection.get_connection().commit()
        dao = LikeDataAccess(dbconnect=connection)
        obj = Like('3', 1)
        dao.add_like(obj)
        object = dao.is_liked(1, '3')
        self.assertTrue(object)
        dao.remove_like('3', 1)
        object = dao.is_liked(1, '3')
        self.assertFalse(object)
        connection.get_cursor().execute('DELETE from "like" where student=\'3\'')
        connection.get_connection().commit()
        connection.close()

    def test_get_student_likes(self):
        connection = self._connect()
        dao = LikeDataAccess(dbconnect=connection)
        objects = dao.get_student_likes('1')
        self.assertTrue(1 in objects)
        connection.close()

