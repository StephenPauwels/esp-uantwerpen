from unittest import TestCase
from src.models.db import *
from src.models.employee import *
from src.config import *


class TestEmployeeDataAccess(TestCase):
    def _connect(self):
        connection = DBConnection(dbname='test_db', dbuser=config_data['dbuser'],
                                  dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return connection

    def test_connection(self):
        connection = self._connect()
        connection.close()
        print("Employee Connection: OK")

    def test_get_employees(self):
        connection = self._connect()
        dao = EmployeeDataAccess(dbconnect=connection)
        objects = dao.get_employees(True)
        self.assertEqual('D Trump'.upper(),
                         objects[-1].name.upper())
        connection.close()

    def test_get_employee(self):
        connection = self._connect()
        dao = EmployeeDataAccess(dbconnect=connection)
        object = dao.get_employee(1)
        self.assertEqual('D Trump'.upper(),
                         object.name.upper())
        connection.close()

    def test_get_employee_by_name(self):
        connection = self._connect()
        dao = EmployeeDataAccess(dbconnect=connection)
        object = dao.get_employee_by_name('D Trump')
        self.assertEqual('D Trump'.upper(),
                         object.name.upper())
        self.assertEqual('Boos'.upper(),
                         object.research_group.upper())
        connection.close()

    def test_add_employee(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from employee where name=\'test_ins\'')
        connection.get_connection().commit()
        dao = EmployeeDataAccess(dbconnect=connection)
        obj = Employee(name='test_ins', e_id=2, email=None, extra_info=None, office=None, picture_location=None, research_group='Boos', title='PhD', is_active=True, is_intern=True)
        dao.add_employee(obj)
        objects = dao.get_employees(True)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].name.upper())
        connection.get_cursor().execute('DELETE from employee where name=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_update_employee(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from employee where name=\'test_ins\'')
        connection.get_connection().commit()
        dao = EmployeeDataAccess(dbconnect=connection)
        obj = Employee(name='test_ins', e_id=None, email=None, extra_info=None, office=None, picture_location=None,
                       research_group='Boos', title='PhD', is_active=True, is_intern=True)
        dao.add_employee(obj)
        objects = dao.get_employees(True)
        # print(objects[-1].to_dct())
        self.assertEqual('test_ins'.upper(),
                         objects[-1].name.upper())
        self.assertEqual(True, objects[-1].is_intern)
        self.assertEqual('PhD', objects[-1].title)
        self.assertEqual('Boos', objects[-1].research_group)
        obj2 = Employee(name='test_ins', e_id=objects[-1].e_id, email=None, extra_info=None, office=None, picture_location=None,
                       research_group='Konijn', title='Professor', is_active=True, is_intern=False)
        dao.update_employee(obj2)
        objects = dao.get_employees(True)
        self.assertEqual(False, objects[-1].is_intern)
        self.assertEqual('Professor', objects[-1].title)
        self.assertEqual('Konijn', objects[-1].research_group)
        connection.get_cursor().execute('DELETE from employee where name=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_update_research_group(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from employee where name=\'test_ins\'')
        connection.get_connection().commit()
        dao = EmployeeDataAccess(dbconnect=connection)
        obj = Employee(name='test_ins', e_id=None, email=None, extra_info=None, office=None, picture_location=None,
                       research_group='Boos', title='PhD', is_active=True, is_intern=True)
        dao.add_employee(obj)
        objects = dao.get_employees(True)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].name.upper())
        self.assertEqual('Boos', objects[-1].research_group)
        dao.update_research_group(objects[-1].e_id, 'Konijn')
        objects = dao.get_employees(True)
        self.assertEqual('Konijn', objects[-1].research_group)
        connection.get_cursor().execute('DELETE from employee where name=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_set_active(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from employee where name=\'test_ins\'')
        connection.get_connection().commit()
        dao = EmployeeDataAccess(dbconnect=connection)
        obj = Employee(name='test_ins', e_id=None, email=None, extra_info=None, office=None, picture_location=None,
                       research_group='Boos', title='PhD', is_active=True, is_intern=True)
        dao.add_employee(obj)
        objects = dao.get_employees(True)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].name.upper())
        dao.set_active(objects[-1].e_id, False)
        objects = dao.get_employees(False)
        self.assertEqual('test_ins'.upper(),
                         objects[-1].name.upper())
        connection.get_cursor().execute('DELETE from employee where name=\'test_ins\'')
        connection.get_connection().commit()
        connection.close()

    def test_domain_title(self):
        connection = self._connect()
        connection.get_cursor().execute('DELETE from Employee where name=\'test112\'')
        connection.get_cursor().execute('DELETE from Employee where name=\'test21\'')
        connection.get_cursor().execute('DELETE from Employee where name=\'test113\'')

        connection.get_connection().commit()
        dao = EmployeeDataAccess(dbconnect=connection)
        obj1 = Employee(name='test112', email=None, office='GR23', extra_info=None, picture_location=None,
                        research_group='Boos',
                        title='Professor', is_intern=False, is_active=False, e_id=None)
        dao.add_employee(obj1)
        obj2 = Employee(name='test21', email=None, office='GR23', extra_info=None, picture_location=None,
                        research_group='Boos',
                        title='PhD', is_intern=False, is_active=True, e_id=None)
        dao.add_employee(obj2)
        obj3 = Employee(name='test113', email=None, office='GR23', extra_info=None, picture_location=None,
                        research_group='Boos',
                        title='Bakker', is_intern=False, is_active=None, e_id=None)
        with self.assertRaises(Exception) as context:
            dao.add_employee(obj3)
        self.assertTrue('' in str(context.exception),
                        'employee exception for not null is_active not raised or wrong exception')
        connection.get_cursor().execute('DELETE from Employee where name=\'test112\'')
        connection.get_cursor().execute('DELETE from Employee where name=\'test21\'')
        connection.get_cursor().execute('DELETE from Employee where name=\'test113\'')

        connection.get_connection().commit()
        connection.close()
