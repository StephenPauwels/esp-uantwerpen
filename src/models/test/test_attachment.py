from unittest import TestCase
from src.models.db import *
from src.models.attachment import *
from src.config import *


class TestAttachmentDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Click Connection: OK")

    def test_get_attachments(self):
        connection = self._connect()
        dao = AttachmentDataAccess(dbconnect=connection)
        objects = dao.get_attachments(1)
        # print(objects[-1].to_dct())
        self.assertEqual('test attach'.upper(),
                         objects[0].name.upper())
        self.assertEqual(1,
                         objects[0].document_id)
        self.assertEqual('LOC test'.upper(),
                         objects[0].file_location.upper())
        connection.close()

    def test_add_attachment(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from Attachment where name=\'test_ins\'')
        connection.get_connection().commit()
        dao = AttachmentDataAccess(dbconnect=connection)
        obj = Attachment(name='test_ins', file_location='LOC', document_id=1)
        dao.add_attachment(obj)
        objects = dao.get_attachments(1)
        #print(objects[-1].to_dct())
        self.assertEqual('test_ins'.upper(),
                         objects[-1].name.upper())
        self.assertEqual(1,
                         objects[-1].document_id)
        connection.close()

    def test_remove_attachment(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from Attachment where name=\'test_ins\'')
        connection.get_connection().commit()
        dao = AttachmentDataAccess(dbconnect=connection)
        obj = Attachment(name='test_ins', file_location='LOC', document_id=1)
        dao.add_attachment(obj)
        objects = dao.get_attachments(1)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].name.upper())
        self.assertEqual('LOC'.upper(),
                         objects[-1].file_location.upper())
        dao.remove_attachment('LOC')
        objects = dao.get_attachments(1)
        # print(objects[-1].to_dct())
        self.assertEqual('test attach'.upper(),
                         objects[-1].name.upper())
        self.assertEqual(1,
                         objects[-1].document_id)
        self.assertEqual('LOC test'.upper(),
                         objects[-1].file_location.upper())
        connection.close()
