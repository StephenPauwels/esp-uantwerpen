"""@package
This package enables the link usage for the database.
"""


class Link:
    """
    This class defines a link between 2 projects.
    """

    def __init__(self, project_id_1, project_id_2, match_percent):
        """
        Link initializer.
        :param project_id_1: The ID of the first object.
        :param project_id_2: The ID of the second project.
        :param match_percent: The match percentage between the projects (between 0 and 1).
        """
        self.project_1 = project_id_1
        self.project_2 = project_id_2
        self.match_percent = match_percent

    def to_dict(self):
        """
        Converts object to a dictionary.
        :return: Dictionary of the object data.
        """
        return vars(self)


class LinkDataAccess:
    """
    This class interacts with the Link component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initiates the LinkDataAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def get_links(self):
        """
        Fetches all the links between projects.
        :return: A list with link objects.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT project_1, project_2, match_percent FROM link')
        link_objects = list()
        for row in cursor:
            link_obj = Link(row[0], row[1], row[2])
            link_objects.append(link_obj)
        return link_objects

    def get_link(self, project_id_1, project_id_2):
        """
        Fetches a specific link from the database.
        :param project_id_1: The ID of the first project.
        :param project_id_2: The ID of the second project.
        :return: A link object.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT project_1, project_2, match_percent FROM link '
                       'WHERE project_1=%s AND project_2=%s', (project_id_1, project_id_2))
        row = cursor.fetchone()
        return Link(row[0], row[1], row[2])

    def get_links_for_project(self, project_id):
        """
        Fecthes the linksfor a given project.
        :param project_id: The ID for the projects to fetch links for.
        :return: A list with link objects.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT project_1, project_2, match_percent FROM Link WHERE project_1=%s', (project_id,))
        projects = list()
        if cursor is None:
            return projects
        for x in cursor:
            projects.append(Link(x[0], x[1], x[2]))
        return projects

    def add_link(self, obj):
        """
        Adds a link to the database.
        :param obj: The new link object.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO link(project_1, project_2, match_percent) VALUES(%s,%s,%s)',
                           (obj.project_1, obj.project_2, obj.match_percent))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def update_match_percent(self, project_id_1, project_id_2, amount_to_add):
        """
        Updates the match percent of a project link.
        :param project_id_1: The ID of the first project.
        :param project_id_2: The ID of the second project.
        :param amount_to_add: The amount to add to the current match percent.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT match_percent FROM link WHERE project_1=%s AND project_2=%s', (project_id_1, project_id_2, ))
        if cursor.fetchone() is None:
            try:
                cursor.execute('INSERT INTO link(project_1, project_2, match_percent) VALUES(%s,%s,%s)',
                               (project_id_1, project_id_2, amount_to_add))
                self.dbconnect.commit()
            except:
                self.dbconnect.rollback()
                raise
            return
        """Cursor is closed so re-execute"""
        cursor.execute('SELECT match_percent FROM link WHERE project_1=%s AND project_2=%s', (project_id_1, project_id_2, ))
        percent = cursor.fetchone()[0] + amount_to_add
        if percent > 1:
            percent = 1
        try:
            cursor.execute('UPDATE link SET match_percent = %s WHERE project_1=%s AND project_2=%s',
                           (percent, project_id_1, project_id_2))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise
