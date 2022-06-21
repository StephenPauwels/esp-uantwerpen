from unittest import TestCase
from src.models.db import *
from src.models.research_group import *
from src.config import *


class TestResearchGroupDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Research Group Connection: OK")

    def test_get_group_names(self):
        connection = self._connect()
        connection.get_connection().commit()
        dao = ResearchGroupDataAccess(dbconnect=connection)
        objects = dao.get_group_names(True)
        self.assertEqual('Boos'.upper(),
                         objects[-1].upper())
        objects = dao.get_group_names(False)
        self.assertEqual('Konijn'.upper(),
                         objects[-1].upper())
        connection.close()

    def test_get_research_groups(self):
        connection = self._connect()
        connection.get_connection().commit()
        dao = ResearchGroupDataAccess(dbconnect=connection)
        objects = dao.get_research_groups(True)
        self.assertEqual('Boos'.upper(),
                         objects[-1].name.upper())
        objects = dao.get_research_groups(False)
        self.assertEqual('Konijn'.upper(),
                         objects[-1].name.upper())
        connection.close()

    def test_get_research_group(self):
        connection = self._connect()
        connection.get_connection().commit()
        dao = ResearchGroupDataAccess(dbconnect=connection)
        object = dao.get_research_group('Boos')
        self.assertEqual('Boos'.upper(),
                         object.name.upper())
        connection.close()

    def test_add_research_group(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from research_group where name=\'test_ins\'')
        connection.get_connection().commit()
        dao = ResearchGroupDataAccess(dbconnect=connection)
        obj = ResearchGroup(name='test_ins', abbreviation= "test", logo_location=None, description_id=1, address=None, telephone_number=None, is_active=True)
        dao.add_research_group(obj)
        objects = dao.get_research_groups(True)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].name.upper())
        connection.get_cursor().execute('DELETE from research_group where name=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_update_research_group(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from research_group where name=\'test_ins\'')
        connection.get_connection().commit()
        dao = ResearchGroupDataAccess(dbconnect=connection)
        obj = ResearchGroup(name='test_ins', abbreviation="test", logo_location=None, description_id=1, address=None,
                            telephone_number=None, is_active=True)
        dao.add_research_group(obj)
        objects = dao.get_research_groups(True)
        self.assertEqual('test'.upper(),
                         objects[-1].abbreviation.upper())
        obj2 = ResearchGroup(name='test_ins', abbreviation="test2", logo_location=None, description_id=1, address=None,
                            telephone_number=None, is_active=True)
        dao.update_research_group(obj.name, obj2)
        objects = dao.get_research_groups(True)
        self.assertEqual('test2'.upper(),
                         objects[-1].abbreviation.upper())
        connection.get_cursor().execute('DELETE from research_group where name=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_set_active(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from research_group where name=\'test_ins\'')
        connection.get_connection().commit()
        dao = ResearchGroupDataAccess(dbconnect=connection)
        obj = ResearchGroup(name='test_ins', abbreviation="test", logo_location=None, description_id=1, address=None,
                            telephone_number=None, is_active=True)
        dao.add_research_group(obj)
        objects = dao.get_research_groups(True)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].name.upper())
        dao.set_active(obj.name, False)
        objects = dao.get_research_groups(False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].name.upper())
        connection.get_cursor().execute('DELETE from research_group where name=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()
