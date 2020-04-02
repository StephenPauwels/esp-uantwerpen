"""@package
This package enables the project click usage for the database.
"""
import datetime


class Click:
    """
    This class defines a click in a session on a project.
    """

    def __init__(self, session_id, project_id, time_of_click):
        """
        Link initializer.
        :param session_id: The ID of the session where the click happened.
        :param project_id: The project the student clicked on.
        :param time_of_click: The time of the project click.
        """
        self.session = session_id
        self.project = project_id
        self.time_of_click = time_of_click

    def to_dict(self):
        """
        Converts object to a dictionary.
        :return: Dictionary of the object data.
        """
        return vars(self)


class ClickDataAccess:
    """
    This class interacts with the ClickDataAccess component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initialises the ClickDataAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def add_project_click(self, project_id, session_id):
        """
        Increments the project view counter.
        :param project_id: The ID of the project to add a click for.
        :param session_id: The ID of the session to add a click for.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        # Check if the click is already registered
        cursor.execute('SELECT *  FROM project_click WHERE project=%s AND session=%s', (project_id, session_id))
        if cursor.fetchone() is not None:
            return
        try:
            cursor.execute('INSERT INTO project_click(session, project, time_of_click) VALUES(%s,%s,%s)',
                           (session_id, project_id, datetime.datetime.now()))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise
