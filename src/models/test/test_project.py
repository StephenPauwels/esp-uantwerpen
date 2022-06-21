from unittest import TestCase
from src.models.db import *
from src.models.project import *
from src.config import *


class TestProjectDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Project Connection: OK")

    def test_get_project_ids(self):
        connection = self._connect()
        dao = ProjectDataAccess(dbconnect=connection)
        objects = dao.get_project_ids(True)
        self.assertEqual(1,
                         objects[0])
        connection.close()

    def test_get_projects(self):
        connection = self._connect()
        dao = ProjectDataAccess(dbconnect=connection)
        objects = dao.get_projects(True, False)
        self.assertEqual('RoboPro'.upper(),
                         objects[0].title.upper())
        connection.close()

    def test_get_project(self):
        connection = self._connect()
        dao = ProjectDataAccess(dbconnect=connection)
        object = dao.get_project(1, True)
        self.assertEqual('RoboPro'.upper(),
                         object.title.upper())
        connection.close()

    def test_get_project_types(self):
        connection = self._connect()
        dao = ProjectDataAccess(dbconnect=connection)
        objects = dao.get_project_types(1)
        self.assertEqual('test_type'.upper(),
                         objects[0].type_name.upper())
        connection.close()

    def test_get_project_tags(self):
        connection = self._connect()
        dao = ProjectDataAccess(dbconnect=connection)
        objects = dao.get_project_tags(1)
        self.assertEqual('test_tag'.upper(),
                         objects[0].upper())
        connection.close()

    def test_add_project(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        dao = ProjectDataAccess(dbconnect=connection)
        obj = Project(title='test_ins', project_id=None, max_students=2, description_id=1,research_group='Boos', is_active=True, last_updated=None, view_count=5, extension=None)
        dao.add_project(obj)
        objects = dao.get_projects(True, False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].title.upper())
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_add_view_count(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        dao = ProjectDataAccess(dbconnect=connection)
        obj = Project(title='test_ins', project_id=None, max_students=2, description_id=1, research_group='Boos',
                      is_active=True, last_updated=None, view_count=None, extension=None)
        objects = dao.get_projects(True, False)
        dao.add_view_count(objects[-1].project_id, 3)
        objects = dao.get_projects(True, False)
        self.assertEqual(3,
                         objects[-1].view_count)
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_update_project(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        dao = ProjectDataAccess(dbconnect=connection)
        obj = Project(title='test_ins', project_id=None, max_students=2, description_id=1, research_group='Boos',
                      is_active=True, last_updated=None, view_count=None, extension=None)
        dao.add_project(obj)
        objects = dao.get_projects(True, False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].title.upper())
        self.assertEqual('Boos'.upper(),
                         objects[-1].research_group.upper())
        self.assertEqual(2,
                         objects[-1].max_students)
        dao.update_project(objects[-1].project_id, objects[-1].title, 1, 'Konijn', True)
        objects = dao.get_projects(True, False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].title.upper())
        self.assertEqual('Konijn'.upper(),
                         objects[-1].research_group.upper())
        self.assertEqual(1,
                         objects[-1].max_students)
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_set_research_group(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        dao = ProjectDataAccess(dbconnect=connection)
        obj = Project(title='test_ins', project_id=None, max_students=2, description_id=1, research_group='Boos',
                      is_active=True, last_updated=None, view_count=None, extension=None)
        dao.add_project(obj)
        objects = dao.get_projects(True, False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].title.upper())
        self.assertEqual('Boos'.upper(),
                         objects[-1].research_group.upper())
        dao.set_research_group(objects[-1].project_id, 'Konijn')
        objects = dao.get_projects(True, False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].title.upper())
        self.assertEqual('Konijn'.upper(),
                         objects[-1].research_group.upper())
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_set_active(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        dao = ProjectDataAccess(dbconnect=connection)
        obj = Project(title='test_ins', project_id=None, max_students=2, description_id=1, research_group='Boos',
                      is_active=True, last_updated=None, view_count=None, extension=None)
        dao.add_project(obj)
        objects = dao.get_projects(True, False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].title.upper())
        dao.set_active(objects[-1].project_id, False)
        objects = dao.get_projects(False, False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].title.upper())
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_mark_all_projects_for_extension(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        dao = ProjectDataAccess(dbconnect=connection)
        obj = Project(title='test_ins', project_id=None, max_students=2, description_id=1, research_group='Boos',
                      is_active=True, last_updated=None, view_count=None, extension=False)
        dao.add_project(obj)
        objects = dao.get_projects(True, False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].title.upper())
        self.assertEqual(False,
                         objects[-1].extension)
#        dao.mark_all_projects_for_extension()
        objects = dao.get_projects(True, False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].title.upper())
        self.assertEqual(True,
                         objects[-1].extension)
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_delete_project_extension(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        dao = ProjectDataAccess(dbconnect=connection)
        obj = Project(title='test_ins', project_id=None, max_students=2, description_id=1, research_group='Boos',
                      is_active=True, last_updated=None, view_count=None, extension=True)
        dao.add_project(obj)
        objects = dao.get_projects(True, False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].title.upper())
        self.assertEqual(True,
                         objects[-1].extension)
#        dao.delete_project_extension(objects[-1].project_id)
        objects = dao.get_projects(False, False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].title.upper())
        self.assertEqual(False,
                         objects[-1].extension)
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_extend_project(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        dao = ProjectDataAccess(dbconnect=connection)
        obj = Project(title='test_ins', project_id=None, max_students=2, description_id=1, research_group='Boos',
                      is_active=True, last_updated=None, view_count=None, extension=True)
        dao.add_project(obj)
        objects = dao.get_projects(True, False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].title.upper())
        self.assertEqual(True,
                         objects[-1].extension)
#        dao.extend_project(objects[-1].project_id)
        objects = dao.get_projects(True, False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].title.upper())
        self.assertEqual(False,
                         objects[-1].extension)
        connection.get_cursor().execute('DELETE from project where title=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_add_active_year(self):
        connection = self._connect()
        connection.autocommit = True
        dao = ProjectDataAccess(dbconnect=connection)
#        connection.get_cursor().execute('DELETE from project_has_year where year=2020')
        connection.get_connection().commit()
#        connection.get_cursor().execute('DELETE FROM academic_year where year=2020')
        connection.get_connection().commit()
#        connection.get_cursor().execute('INSERT INTO academic_year(year) VALUES (2020)')
        connection.get_connection().commit()
        dao.add_active_year(1, 2020)
        object = dao.get_project(1, True)
        self.assertEqual(2020, object.active_years[0])
#        connection.get_cursor().execute('DELETE from project_has_year where year=2020')
        connection.get_connection().commit()
#        connection.get_cursor().execute('DELETE FROM academic_year where year=2020')
        connection.get_connection().commit()
        connection.close()

    def test_add_project_tag(self):
        connection = self._connect()
        dao = ProjectDataAccess(dbconnect=connection)
        connection.get_cursor().execute('DELETE from project_has_tag where tag=\'test_ins\'')
        connection.get_connection().commit()
        connection.get_cursor().execute('DELETE FROM TAG where tag=(\'test_ins\')')
        connection.get_connection().commit()
        objects = dao.get_project_tags(1)
        self.assertEqual('test_tag'.upper(),
                         objects[0].upper())
        connection.get_cursor().execute('INSERT INTO tag(tag) VALUES (\'test_ins\')')
        connection.get_connection().commit()
        dao.add_project_tag(1, 'test_ins')
        objects = dao.get_project_tags(1)
        self.assertEqual('test_ins'.upper(),
                         objects[0].upper())
        connection.get_cursor().execute('DELETE from project_has_tag where tag=\'test_ins\'')
        connection.get_connection().commit()
        connection.get_cursor().execute('DELETE FROM TAG where tag=(\'test_ins\')')
        connection.get_connection().commit()
        connection.close()

    def test_remove_tags(self):
        connection = self._connect()
        dao = ProjectDataAccess(dbconnect=connection)
        connection.get_cursor().execute('DELETE from project_has_tag where tag=\'test_ins\'')
        connection.get_connection().commit()
        connection.get_cursor().execute('DELETE FROM TAG where tag=(\'test_ins\')')
        connection.get_connection().commit()
        connection.get_cursor().execute('INSERT INTO tag(tag) VALUES (\'test_ins\')')
        connection.get_connection().commit()
        dao.add_project_tag(2, 'test_ins')
        objects = dao.get_project_tags(2)
        self.assertEqual('test_ins'.upper(),
                         objects[0].upper())
        self.assertGreater(len(objects),0)
        dao.remove_tags(2)
        objects = dao.get_project_tags(2)
        self.assertEqual(0, len(objects))
        connection.get_cursor().execute('DELETE from project_has_tag where tag=\'test_ins\'')
        connection.get_connection().commit()
        connection.get_cursor().execute('DELETE FROM TAG where tag=(\'test_ins\')')
        connection.get_connection().commit()
        connection.close()

    def test_remove_tag(self):
        connection = self._connect()
        dao = ProjectDataAccess(dbconnect=connection)
        connection.get_cursor().execute('DELETE from project_has_tag where tag=\'test_ins\'')
        connection.get_connection().commit()
        connection.get_cursor().execute('DELETE FROM TAG where tag=(\'test_ins\')')
        connection.get_connection().commit()
        connection.get_cursor().execute('INSERT INTO tag(tag) VALUES (\'test_ins\')')
        connection.get_connection().commit()
        dao.add_project_tag(1, 'test_ins')
        objects1 = dao.get_project_tags(1)
        self.assertEqual('test_ins'.upper(),
                         objects1[0].upper())
        dao.remove_tag(1, 'test_ins')
        objects2 = dao.get_project_tags(1)
        self.assertGreater(len(objects1), len(objects2))
        self.assertNotEqual('test_ins'.upper(),
                         objects2[0].upper())
        connection.get_cursor().execute('DELETE from project_has_tag where tag=\'test_ins\'')
        connection.get_connection().commit()
        connection.get_cursor().execute('DELETE FROM TAG where tag=(\'test_ins\')')
        connection.get_connection().commit()
        connection.close()

    def test_add_type(self):
        connection = self._connect()
        dao = ProjectDataAccess(dbconnect=connection)
        connection.get_cursor().execute('DELETE from project_has_type where type=\'test_ins\'')
        connection.get_connection().commit()
        connection.get_cursor().execute('DELETE FROM type where type_name=(\'test_ins\')')
        connection.get_connection().commit()
        objects = dao.get_project_types(1)
        self.assertEqual('test_type'.upper(),
                         objects[0].type_name.upper())
        connection.get_cursor().execute('INSERT INTO Type(type_name, is_active) VALUES (\'test_ins\', true)')
        connection.get_connection().commit()
        dao.add_type(1, 'test_ins')
        objects = dao.get_project_types(1)
        self.assertEqual('test_ins'.upper(),
                         objects[0].type_name.upper())
        connection.get_cursor().execute('DELETE from project_has_type where type=\'test_ins\'')
        connection.get_connection().commit()
        connection.get_cursor().execute('DELETE FROM type where type_name=(\'test_ins\')')
        connection.get_connection().commit()
        connection.close()

    def test_remove_types(self):
        connection = self._connect()
        dao = ProjectDataAccess(dbconnect=connection)
        connection.get_cursor().execute('DELETE from project_has_type where type=\'test_ins\'')
        connection.get_connection().commit()
        connection.get_cursor().execute('DELETE FROM type where type_name=(\'test_ins\')')
        connection.get_connection().commit()
        connection.get_cursor().execute('INSERT INTO Type(type_name, is_active) VALUES (\'test_ins\', true)')
        connection.get_connection().commit()
        dao.add_type(2, 'test_ins')
        objects = dao.get_project_types(2)
        self.assertEqual('test_ins'.upper(),
                         objects[0].type_name.upper())
        self.assertGreater(len(objects), 0)
        dao.remove_types(2)
        objects = dao.get_project_types(2)
        self.assertEqual(len(objects), 0)
        connection.get_cursor().execute('DELETE from project_has_type where type=\'test_ins\'')
        connection.get_connection().commit()
        connection.get_cursor().execute('DELETE FROM type where type_name=(\'test_ins\')')
        connection.get_connection().commit()
        connection.close()

    def test_remove_type(self):
        connection = self._connect()
        dao = ProjectDataAccess(dbconnect=connection)
        connection.get_cursor().execute('DELETE from project_has_type where type=\'test_ins\'')
        connection.get_connection().commit()
        connection.get_cursor().execute('DELETE FROM type where type_name=(\'test_ins\')')
        connection.get_connection().commit()
        connection.get_cursor().execute('INSERT INTO Type(type_name, is_active) VALUES (\'test_ins\', true)')
        connection.get_connection().commit()
        dao.add_type(1, 'test_ins')
        objects1 = dao.get_project_types(1)
        self.assertEqual('test_ins'.upper(),
                         objects1[0].type_name.upper())
        dao.remove_type(1, 'test_ins')
        objects2 = dao.get_project_types(1)
        self.assertGreater(len(objects1), len(objects2))
        connection.get_cursor().execute('DELETE from project_has_type where type=\'test_ins\'')
        connection.get_connection().commit()
        connection.get_cursor().execute('DELETE FROM type where type_name=(\'test_ins\')')
        connection.get_connection().commit()
        connection.close()

    def test_get_most_viewed_projects(self):
        connection = self._connect()
        dao = ProjectDataAccess(dbconnect=connection)
        dao.add_view_count(1, 4)
        dao.add_view_count(2,5)
        object = dao.get_most_viewed_projects(1,True)
        self.assertEqual(2, object[0].project_id)
        connection.close()

    def test_get_oldest_and_newest(self):
        connection = self._connect()
        dao = ProjectDataAccess(dbconnect=connection)
        objects = dao.get_oldest_and_newest()
        self.assertGreater(objects[1], objects[0])
        connection.close()

