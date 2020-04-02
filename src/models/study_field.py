"""@package
This package enables the project study field usage for the database.
"""


class StudyField:
    """
    This class defines a Study Field.
    e.g.: Computer Science, Mathematics, ...
    """

    def __init__(self, field_name, is_active):
        """
        Study field initializer.
        :param field_name: The study field name.
        :param is_active: Indicates whether study field is active or not.
        """
        self.field_name = field_name
        self.is_active = is_active

    def to_dict(self):
        """
        Converts object to a dictionary.
        :return: Dictionary of the object data.
        """
        return vars(self)


class StudyFieldDataAccess:
    """
    This class interacts with the StudyField component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initiates the StudyFieldDataAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def get_study_fields(self, active_only):
        """
        Fetches all the study fields from the database.
        :param active_only: Only return active study fields.
        :return A list with all the study fields.
        """
        cursor = self.dbconnect.get_cursor()

        if active_only:
            cursor.execute('SELECT field_name, is_active FROM study_field WHERE is_active = TRUE')
        else:
            cursor.execute('SELECT field_name, is_active FROM study_field')

        return [StudyField(row[0], row[1]) for row in cursor]

    def add_study_field(self, obj):
        """
        Adds a new study field to the database.
        :param obj: New study field object.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO study_field(field_name, is_active) VALUES(%s, %s)',
                           (obj.field_name, True))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def update_study_field(self, field_name, obj):
        """
        Updated a study field in the database.
        :param field_name: The name of the study field to be updated.
        :param obj: The new study field object.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('UPDATE study_field SET field_name = %s WHERE field_name=%s;',
                           (obj.field_name, field_name))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def set_active(self, field_name, active):
        """
        Changes the active status of a study field.
        :param field_name: The study field to change.
        :param active: The new active status.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('UPDATE study_field SET is_active = %s WHERE field_name = %s',
                           (active, field_name))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise
