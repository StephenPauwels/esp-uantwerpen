"""@package
This package enables the employee usage for the database.
"""


class Employee:
    """
    This class defines an employee.
    """

    def __init__(self, employee_id, name, email, office, extra_info, picture_location, research_group, title, is_external,
                 is_admin, is_active):
        """
        Employee initializer.
        :param employee_id: The ID of the employee.
        :param name: The name of the employee.
        :param email: The email of the employee.
        :param office: The employee office.
        :param extra_info: Extra info (extra address, mail...)
        :param picture_location: The profile picture location.
        :param research_group: The research group the employee belongs to.
        :param title: The academic title of the employee.
        :param is_external: Whether the employee is internal or external.
        :param is_active: Whether the employee is active or not.
        """
        self.e_id = employee_id
        self.name = name
        self.email = email
        self.office = office
        self.extra_info = extra_info
        self.picture_location = picture_location
        self.research_group = research_group
        self.title = title
        self.is_external = is_external
        self.is_admin = is_admin
        self.is_active = is_active

    def to_dict(self):
        """
        Converts object to a dictionary.
        :return: Dictionary of the object data.
        """
        return vars(self)


class EmployeeDataAccess:
    """
    This class interacts with the Employee component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initiates the EmployeeDataAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def get_employees(self, active_only):
        """
        Fetches all the employees from the database.
        :param active_only: Fetch only active employees.
        :return: A list with employee objects.
        """
        cursor = self.dbconnect.get_cursor()

        if active_only:
            cursor.execute(
                'SELECT id, name, email, office, extra_info, picture_location, research_group, title, is_external, '
                'is_admin, is_active FROM employee WHERE is_active = TRUE')
        else:
            cursor.execute(
                'SELECT id, name, email, office, extra_info, picture_location, research_group, title, is_external, '
                'is_admin, is_active FROM employee')

        employees = list()
        for row in cursor:
            obj = Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            employees.append(obj)
        return employees

    def get_employee(self, employee_id):
        """
        Fetches the given employee.
        :param employee_id: The ID of the employee to fetch the info for.
        :return: An employee object.
        """
        cursor = self.dbconnect.get_cursor()

        try:
            cursor.execute('SELECT id, name, email, office, extra_info, picture_location, research_group, title, is_external,'
                           ' is_admin, is_active FROM employee WHERE LOWER(id)=LOWER(%s)', (employee_id,))
            row = cursor.fetchone()
            return Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])

        except:
            self.dbconnect.rollback()
            raise

    def get_employee_by_name(self, name):
        """
        Fetches the employee info by name.
        :param name: The name of the employee.
        :return: An employee object.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT id, name, email, office, extra_info, picture_location, research_group, title, is_external,'
                       ' is_admin, is_active FROM employee WHERE name=%s', (name,))
        row = cursor.fetchone()
        return Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])

    def add_employee(self, obj):
        """
        Adds an employee to the database.
        :param obj: The new employee object.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO employee(id, name, email, office, extra_info, picture_location, research_group, '
                           'title, is_external, is_admin, is_active) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);',
                           (obj.e_id, obj.name, obj.email, obj.office, obj.extra_info, obj.picture_location, obj.research_group,
                            obj.title, obj.is_external, obj.is_admin, obj.is_active))

            self.dbconnect.commit()
            return obj
        except:
            self.dbconnect.rollback()
            raise

    def update_employee(self, obj):
        """
        Updates the info of an employee.
        :param obj: The new employee.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('UPDATE employee '
                           'SET name = %s, email = %s, office = %s, extra_info = %s, picture_location = %s, '
                           'research_group = %s, title = %s, is_external = %s, is_admin = %s, is_active = %s '
                           'WHERE id = %s;',
                           (obj.name, obj.email, obj.office, obj.extra_info, obj.picture_location, obj.research_group,
                            obj.title, obj.is_external, obj.is_admin, obj.is_active, obj.e_id))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def update_research_group(self, employee_id, new_research_group):
        """
        Sets the research group if an employee.
        :param employee_id: The ID of the employee.
        :param new_research_group: The new research group of the employee.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('UPDATE employee '
                           'SET research_group = %s '
                           'WHERE id=%s;',
                           (new_research_group, employee_id))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def set_active(self, employee_id, active):
        """
        Changes the active status of the employee.
        :param employee_id: The ID of the employee.
        :param active: The new active status.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('UPDATE employee '
                           'SET is_active = %s '
                           'WHERE id=%s;',
                           (active, employee_id))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise
