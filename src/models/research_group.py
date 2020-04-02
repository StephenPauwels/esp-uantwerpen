""""@package
This package enables the research group usage for the database.
"""

from src.models.employee import EmployeeDataAccess


class ResearchGroup:
    """
    This class defines a research group
    """

    def __init__(self, name, abbreviation, logo_location, description_id, address, telephone_number,
                 is_active):
        """
        ResearchGroup initializer.
        :param name: Research group name.
        :param abbreviation: Research group abbreviation.
        :param logo_location: Location of group logo.
        :param description_id: ID of the group description.
        :param address: Research group address.
        :param telephone_number: Research group telephone number.
        :param study_field: Research group study field.
        :param is_active: Status of research group.
        """
        self.name = name
        self.abbreviation = abbreviation
        self.logo_location = logo_location
        self.address = address
        self.telephone_number = telephone_number
        self.is_active = is_active
        self.description_id = description_id
        self.description_eng = None
        self.description_nl = None
        self.contact_person = None

    def to_dict(self):
        """
        Converts object to a dictionary.
        :return: Dictionary of the object data.
        """
        return vars(self)


class ResearchGroupDataAccess:
    """
    This class interacts with the ResearchGroup component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initiates the ResearchGroupDataAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def get_group_names(self, active_only):  # TODO #2 error for empty fetch
        """
        Fetches all research group names.
        :param active_only: Only return active research groups.
        :return: A list with all the active and/or non-active research group names.
        """
        cursor = self.dbconnect.get_cursor()

        if active_only:
            cursor.execute('SELECT name FROM research_group WHERE is_active = TRUE')
        else:
            cursor.execute('SELECT name FROM research_group')

        return [row[0] for row in cursor]

    def get_research_groups(self, active_only):  # TODO #2 catching empty?
        """
        Fetches all research groups from the database.
        :param active_only: Only return active research groups.
        :return: A list with all the active and/or non-active research groups.
        """
        return [self.get_research_group(name) for name in self.get_group_names(active_only)]

    def get_research_group(self, group_name):  # TODO #2
        """
        Retrieves all the data of a given research group.
        :param group_name: The name of the research group to fetch.
        :return: Research group object.
        """
        cursor = self.dbconnect.get_cursor()

        """General info"""
        cursor.execute(
            'SELECT name, abbreviation, logo_location, description_id, address, telephone_number'
            ', is_active FROM research_group WHERE name=%s', (group_name,))
        row = cursor.fetchone()
        group = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

        """Descriptions"""
        cursor.execute('SELECT html_content_nl, html_content_eng FROM document WHERE document_id=%s',
                       (group.description_id,))
        row = cursor.fetchone()
        if row is not None:
            group.description_nl = row[0]
            group.description_eng = row[1]

        """Contact person"""
        cursor.execute('SELECT contact_person FROM contact_person WHERE research_group=%s', (group_name,))
        row = cursor.fetchone()
        if row is not None:
            employee = EmployeeDataAccess(self.dbconnect).get_employee(row[0])
            group.contact_person = employee.name

        return group

    def add_research_group(self, obj):
        """
        Adds a research group to the database.
        :param obj: The new research group.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO research_group(name, abbreviation, logo_location, description_id, address, '
                           'telephone_number, is_active) VALUES(%s,%s,%s,%s,%s,%s,%s)',
                           (obj.name, obj.abbreviation, obj.logo_location, obj.description_id, obj.address,
                            obj.telephone_number, obj.is_active))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def update_research_group(self, group_name, obj):
        """
        Updates a research group in the database.
        :param group_name: The original name of the group.
        :param obj: New research group.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('UPDATE research_group '
                           'SET name = %s, abbreviation = %s, logo_location = %s, description_id = %s, '
                           'address = %s, telephone_number = %s, is_active = %s '
                           'WHERE name=%s',
                           (obj.name, obj.abbreviation, obj.logo_location, obj.description_id, obj.address,
                            obj.telephone_number, obj.is_active, group_name))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def set_active(self, group_name, active):
        """
        Changes the status of the group.
        :param group_name: The group to change.
        :param active: The new active status.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('UPDATE research_group '
                           'SET is_active = %s '
                           'WHERE name=%s',
                           (active, group_name))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def set_contact_person(self, group_name, contact_person_id):
        """
        Sets the contact person of a group.
        :param group_name: The research group name.
        :param contact_person_id: The ID of contact person of the group.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE from contact_person '
                           'WHERE research_group = %s',
                           (group_name, ))
            self.dbconnect.commit()

            employee = EmployeeDataAccess(self.dbconnect).get_employee_by_name(contact_person_id)
            cursor.execute('INSERT INTO contact_person VALUES (%s, %s)', (employee.e_id, group_name))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise
