from unittest import TestCase
from src.models.db import *
from src.models.document import *
from src.config import *


class TestDocumentDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Document Connection: OK")

    def test_get_document(self):
        connection = self._connect()
        dao = DocumentDataAccess(dbconnect=connection)
        obj = dao.get_document(iden=1)
        self.assertEqual(
            'test_eng'.upper(),
            obj.html_content_eng.upper())
        self.assertEqual(
            'test_nl'.upper(),
            obj.html_content_nl.upper()
        )
        connection.close()

    def test_get_documents(self):
        connection = self._connect()
        dao = DocumentDataAccess(dbconnect=connection)
        objects = dao.get_documents()
        self.assertEqual(
            'test_eng'.upper(),
            objects[0].html_content_eng.upper())
        self.assertEqual(
            'test_nl'.upper(),
            objects[0].html_content_nl.upper()
        )
        connection.close()

    def test_add_document(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from Document where html_content_eng=\'test_eng_ins\'')
        connection.get_connection().commit()
        dao = DocumentDataAccess(dbconnect=connection)
        obj = Document(document_id=None, html_content_eng='test_eng_ins', html_content_nl='test_nl_ins')
        dao.add_document(obj)
        objects = dao.get_documents()
        self.assertEqual('test_eng_ins'.upper(),
                         objects[-1].html_content_eng.upper())
        self.assertEqual('test_nl_ins'.upper(),
                         objects[-1].html_content_nl.upper())
        connection.close()

    def test_update_document(self):
        connection = self._connect()
        dao = DocumentDataAccess(dbconnect=connection)
        obj = dao.get_document(iden=1)
        obj.html_content_nl="update_nl test"
        obj.html_content_eng="update_eng test"
        dao.update_document(obj)
        self.assertEqual(
            "update_eng test".upper(),
            obj.html_content_eng.upper())
        self.assertEqual(
            "update_nl test".upper(),
            obj.html_content_nl.upper()
        )
        connection.close()
