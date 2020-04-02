from unittest import TestCase
from src.models.db import *
from src.models.query import *
from src.config import *


class TestQueryDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Query Connection: OK")

    def test_get_queries(self):
        connection = self._connect()
        dao = QueryDataAccess(dbconnect=connection)
        objects = dao.get_queries()
        self.assertEqual('NO'.upper(),
                         objects[0].search_terms.upper())
        self.assertEqual(1,
                         objects[0].session)
        connection.close()

    def test_get_query(self):
        connection = self._connect()
        dao = QueryDataAccess(dbconnect=connection)
        object = dao.get_query(1)
        self.assertEqual('NO'.upper(),
                         object.search_terms.upper())
        self.assertEqual(1,
                         object.session)
        connection.close()

    def test_add_query(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from query where search_terms=\'test_ins\'')
        connection.get_connection().commit()
        dao = QueryDataAccess(dbconnect=connection)
        obj = Query(session_id=1, time_of_query='23:09:55', search_terms='test_ins')
        dao.add_query(obj)
        objects = dao.get_queries()
        self.assertEqual('test_ins'.upper(),
                         objects[-1].search_terms.upper())
        self.assertEqual(1,
                         objects[-1].session)
        connection.get_cursor().execute('DELETE from query where search_terms=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()
