"""@package
This package enables the guide usage for the database.
"""

from src.models.registration import RegistrationDataAccess


class Guide:
    """
    This class contains the project guide info.
    """

    def __init__(self, employee_name, project_id, guidance_type):
        """
        Guide initializer
        :param employee_name: The name of the employee that guides the given project.
        :param project_id: The ID of the project.
        :param guidance_type: The guidance type of the employee (mentor, promotor...)
        """
        self.employee = employee_name
        self.project = project_id
        self.guidance_type = guidance_type

    def to_dict(self):
        """
        Converts object to a dictionary.
        :return: Dictionary of the object data.
        """
        value = vars(self)
        if type(self.employee) != str:
            value["employee"] = self.employee.to_dict()
        return value


class GuideDataAccess:
    """
    This class interacts with the Guide component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initialises the GuideDataAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def get_guides_for_project(self, project_id):
        """
        Fetches all the guides for a given project.
        :param project_id: The ID of the project.
        :return: A list with Guide objects.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT employee, project, guidance_type FROM guide WHERE project = %s', (project_id,))
        guides_objects = list()
        for row in cursor:
            guides_obj = Guide(row[0], row[1], row[2])
            guides_objects.append(guides_obj)
        return guides_objects

    def get_promotor_for_project(self, project_id):
        """
        Fetches the promotor for a given project.
        :param project_id: The ID of the project.
        :return: The employee_id of the promotor
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT employee, project, guidance_type FROM guide WHERE guidance_type=\'Promotor\' AND project = %s', (project_id,))
        return cursor.fetchone()

    def add_guide(self, obj):
        """
        Adds a guide to the database.
        :param obj: The new guide object.
        :raise: Exception when the database must be rolled back and adding the guide failed.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO guide(employee, project, guidance_type) VALUES(%s,%s,%s)', (obj.employee,
                                                                                                    obj.project,
                                                                                                    obj.guidance_type))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def get_guides_project_info(self, employee_name):
        """
        Fetches the registration and extension info for all the projects a given employee guides.
        :param employee_name: The employee to fetch the guide data for.
        :return: A list of projects for which the employee is a guide.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT id FROM employee WHERE name=%s', (employee_name,))
        row = cursor.fetchone()
        cursor.execute(
            'SELECT project_id, title, extension_needed FROM guide JOIN project p on guide.project = p.project_id '
            'WHERE employee=%s', (row[0],))
        projects = list()
        registration_access = RegistrationDataAccess(self.dbconnect)
        added_projects = []
        for row in cursor:
            if row[0] in added_projects:
                continue
            info = {"project_id": row[0], "title": row[1], "extension": row[2],
                    "registrations": registration_access.get_pending_registrations(row[0])}
            projects.append(info)
            added_projects.append(row[0])
        return projects

    def get_projects_for_employee(self, employee_id):
        """
        Fetches all the projects an employee guides.
        :param employee_id: The ID of the employee to fetch the info for.
        :return: A list of project ID's
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT DISTINCT project FROM guide WHERE employee = %s', (employee_id,))
        project_objects = list()
        for row in cursor:
            project_objects.append({"project_id": row[0]})
        return project_objects

    def remove_project_guides(self, project_id):
        """
        Removes the guides from a project.
        :param project_id: The project ID.
        :raise: Exception when database has to roll back and removal process failed.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM guide WHERE project=%s', (project_id,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def remove_guide(self, employee_id, project_id):
        """
        Removes a guide for a specific project.
        :param employee_id: The ID of the guide to remove.
        :param project_id: The ID of the project to remove the guide for.
        :raise: Exception when the database has to roll back and the removal failed.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM guide '
                           'WHERE employee=%s AND project=%s',
                           (employee_id, project_id))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise
