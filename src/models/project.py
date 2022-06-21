"""@package
This package enables the project usage for the database.
"""

import re
from datetime import date
from src.models.type import Type
from src.models import EmployeeDataAccess, GuideDataAccess, LikeDataAccess


def extract_text(html):
    """
    Removes the tags from a HTML string.
    :param html: The HTML to refactor.
    :return: The refactored HTML string.
    """
    return re.sub(extract_text.regex, "", html)


"""Compile regex only once to increase speed"""
extract_text.regex = re.compile("<.*?>", re.IGNORECASE)


class Project:
    """
    This class defines a project.
    """

    def __init__(self, project_id, title, max_students, description_id, research_group, is_active, last_updated,
                 view_count, extension, creation_date=date.today().strftime("%Y-%m-%d")):
        """
        Project initializer.
        :param project_id: The project ID.
        :param title: The title of the project.
        :param max_students: The maxumum amount of student that can participate in the project.
        :param description_id: The ID of the document containing the desciption.
        :param research_group: The ID of the connected research group.
        :param is_active: Active status of the project.
        :param last_updated: Timestamp when the project was last updated.
        :param view_count: Amount of views the project has.
        :param extension: Boolean to indicate whether an extension to next year is needed.
        """
        """Columns in Project table"""
        self.project_id = project_id
        self.title = title
        self.max_students = max_students
        self.description_id = description_id
        self.research_group = research_group
        self.is_active = is_active
        self.last_updated = last_updated
        self.view_count = view_count
        self.extension = extension
        self.creation_date = creation_date

        """Data from other tables"""
        self.html_content_eng = None
        self.html_content_nl = None
        self.tags = None
        self.types = None
        self.employees = None
        self.registrations = None
        self.attachments = None
        self.liked = False

    def to_dict(self):
        """
        Converts object to a dictionary.
        :return: Dictionary of the object data.
        """
        value = vars(self)
        if type(self.employees) is list:
            value["employees"] = [obj.to_dict() for obj in self.employees]
        value['last_updated'] = value['last_updated'].timestamp()
        return value


class ProjectDataAccess:
    """
    This class interacts with the Project component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initiates the ProjectDataAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def get_project_ids(self, active_only=False):  # TODO #2 error for empty fetch
        """
        Fetches all the project ID's from the database.
        :param active_only: Indicate whether the ID's of only active projects are needed.
        :return: List of project ID's
        """
        cursor = self.dbconnect.get_cursor()

        if active_only:
            cursor.execute('SELECT project_id FROM project WHERE is_active = TRUE')
        else:
            cursor.execute('SELECT project_id FROM project')

        return [row[0] for row in cursor]

    def get_projects(self, active_only, details=False):  # TODO #2 error for empty fetch
        """
        Fetches all the projects and their data.
        :param active_only: Indicate whether the ID's of only active projects are needed.
        :param details: Indicate whether the full description and employee list is needed.
        :return: A list with project objects.
        """
        projects = list()
        for project_id in self.get_project_ids(active_only):
            project = self.get_project(project_id, active_only)

            if not details:
                self.minimize_project(project)

            projects.append(project)

        return projects

    def get_projects_from_promotor(self, promotor_id, details=False):
        projects = list()
        for project_id in self.get_project_ids(False):
            p = self.get_project(project_id, False)
            for emp in p.employees:
                if emp.guidance_type == "Promotor" and emp.employee.e_id == promotor_id:
                    if not details:
                        self.minimize_project(p)

                    projects.append(p)

        return projects

    def is_promotor(self, project_id, promotor_id):
        p = self.get_project(project_id, False)
        for emp in p.employees:
            if emp.guidance_type == "Promotor" and emp.employee.e_id == promotor_id:
                return True
        return False


    @staticmethod
    def minimize_project(project):
        """Remove tags and cut the html to 400 chars"""
        if project.html_content_nl is not None:
            project.html_content_nl = extract_text(project.html_content_nl)[0:400]
        if project.html_content_eng is not None:
            project.html_content_eng = extract_text(project.html_content_eng)[0:400]

        new_guides = dict()
        for guide in project.employees:
            guidance = guide.guidance_type

            """Add list if not present"""
            if not new_guides.get(guidance):
                new_guides[guidance] = []

            # Add name
            new_guides[guidance].append(guide.employee.name)

        project.employees = new_guides

    def get_project(self, project_id, active_only):
        """
        Fetches all the data of a given project.
        :param project_id: The project ID to fetch info for.
        :param active_only: Fetch only active projects.
        :return: A list with project objects.
        """
        """Get all the project data"""
        cursor = self.dbconnect.get_cursor()

        """Data from project table"""
        cursor.execute('SELECT project_id, title, max_students, description_id, research_group, is_active, '
                       'last_updated, view_count, extension_needed, creation_date FROM project'
                       ' WHERE project_id=%s', (project_id,))
        row = cursor.fetchone()
        project = Project(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

        """Types"""
        types = list()
        for project_type in self.get_project_types(project_id):
            if not active_only or project_type.is_active:
                types.append(project_type.type_name)
        project.types = types

        """Tags"""
        project.tags = self.get_project_tags(project_id)

        """Get guides, add employee info"""
        guides = GuideDataAccess(self.dbconnect).get_guides_for_project(project_id)
        for guide in guides:
            guide.employee = EmployeeDataAccess(self.dbconnect).get_employee(guide.employee)
        project.employees = guides

        """Registrations"""
        cursor.execute('SELECT student, name, status, type, date FROM project_registration JOIN student s on '
                       'project_registration.student = s.student_id WHERE project=%s', (project_id,))
        registrations = list()
        for row in cursor:
            registrations.append({"student_nr": row[0], "name": row[1], "status": row[2], "type": row[3],
                                  "last_updated": row[4]})
        project.registrations = registrations

        """Descriptions"""
        cursor.execute('SELECT html_content_eng, html_content_nl FROM document WHERE document_id = %s',
                       (project.description_id,))
        row = cursor.fetchone()
        project.html_content_eng = row[0]
        project.html_content_nl = row[1]

        """Attachments"""
        cursor.execute('SELECT name, file_location FROM attachment WHERE document_id=%s', (project.description_id,))
        attachments = list()
        for row in cursor:
            attachments.append({'name': row[0], 'file_location': row[1]})
        project.attachments = attachments

        return project

    def get_project_types(self, project_id):
        """
        Fetches the types for a given project.
        :param project_id: The project ID to fetch the types for.
        :return: A list of type objects.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT type, t.is_active FROM project_has_type JOIN type t '
                       'on project_has_type.type = t.type_name WHERE project=%s', (project_id,))

        return [Type(row[0], row[1]) for row in cursor]

    def get_project_tags(self, project_id):
        """
        Fetches the tags for a given project.
        :param project_id: The project ID to fetch the tags for.
        :return: A list of tags names.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT tag FROM project_has_tag WHERE project=%s', (project_id,))
        return [row[0] for row in cursor]

    def get_most_viewed_projects(self, nr_of_projects, active_only):
        """
        Fetches the top most viewed projects.
        :param nr_of_projects: The length of the top.
        :param active_only: Only fetch active projects.
        :return: A list with project objects.
        """
        cursor = self.dbconnect.get_cursor()

        if active_only:
            cursor.execute('SELECT project_id FROM project WHERE is_active = true ORDER BY view_count DESC')
        else:
            cursor.execute('SELECT project_id FROM project ORDER BY view_count DESC')

        projects = list()
        i = 0
        for row in cursor:
            if i >= nr_of_projects:
                break
            projects.append(self.get_project(row[0], active_only))
            i += 1

        return projects

    def update_search_index(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('REFRESH MATERIALIZED VIEW search_index; ')
        self.dbconnect.commit()

    def search(self, search_query, active_only):
        """
        Fetches the searched projects.
        :param search_query: The search query.
        :param active_only: Only fetch active projects.
        :return: A list with project ID's.
        """
        cursor = self.dbconnect.get_cursor()
        if active_only:
            cursor.execute("SELECT project_id, ts_rank(document, plainto_tsquery('english', %s)) "
                           "FROM search_index "
                           "WHERE document @@ plainto_tsquery('english', %s) AND is_active = true "
                           "ORDER BY ts_rank(document, plainto_tsquery('english', %s)) DESC;",
                           (search_query, search_query, search_query))
        else:
            cursor.execute("SELECT project_id, ts_rank(document, plainto_tsquery('english', %s)) "
                           "FROM search_index "
                           "WHERE document @@ plainto_tsquery('english', %s) "
                           "ORDER BY ts_rank(document, plainto_tsquery('english', %s)) DESC;",
                           (search_query, search_query, search_query))

        search_results = list()
        for row in cursor:
            search_results.append({"id": row[0], "rank": row[1]})

        projects = []
        for result in search_results:
            project = self.get_project(result["id"], active_only)
            self.minimize_project(project)
            project = project.to_dict()
            project["recommendation"] = result['rank']
            projects.append(project)

        return projects

    def get_oldest_and_newest(self):
        """
        Fetches the oldest and newest timestamp from the last_updated attribute.
        :return: The oldest and newest timestamp.
        """
        cursor = self.dbconnect.get_cursor()

        cursor.execute('SELECT last_updated FROM project ORDER BY last_updated DESC LIMIT 1')
        newest = cursor.fetchone()[0]

        cursor.execute('SELECT last_updated FROM project ORDER BY last_updated ASC LIMIT 1')
        oldest = cursor.fetchone()[0]

        return oldest, newest

    def add_project(self, obj):
        """
        Adds a project to the database.
        :param obj: The new project object.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO Project(title, max_students, description_id, research_group, '
                           'is_active, extension_needed, creation_date) VALUES(%s,%s,%s,%s,%s,%s, CURRENT_DATE)',
                           (obj.title, obj.max_students, obj.description_id,
                            obj.research_group, obj.is_active, obj.extension))
            # Get id and return updated object
            cursor.execute('SELECT LASTVAL()')
            iden = cursor.fetchone()[0]
            obj.project_id = iden
            self.dbconnect.commit()
            return obj
        except:
            self.dbconnect.rollback()
            raise

    def add_view_count(self, project_id, amount):
        """
        Increments the project view counter.
        :param project_id: The project ID to increment the counter for.
        :param amount: The amount to increment the counter with
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT view_count FROM project WHERE project_id=%s', (project_id,))
        count = cursor.fetchone()[0] + amount
        try:
            cursor.execute('UPDATE project SET view_count = %s WHERE project_id=%s', (count, project_id))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def add_type(self, project_id, project_type):
        """
        Adds a type to a project in the database.
        :param project_id: The project to add a type for.
        :param project_type: The new project type.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO project_has_type(project, type) VALUES(%s,%s)',
                           (project_id, project_type))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    # def add_active_year(self, project_id, year):
    #     """
    #     Links a project with an academic year.
    #     :param project_id: The project to link with a year.
    #     :param year: The year to link.
    #     :raise: Exception if the database has to roll back.
    #     """
    #     cursor = self.dbconnect.get_cursor()
    #     try:
    #         cursor.execute('INSERT INTO project_has_year(project, year) VALUES(%s,%s)',
    #                        (project_id, year))
    #         self.dbconnect.commit()
    #     except:
    #         self.dbconnect.rollback()
    #         raise

    def add_project_tag(self, project_id, tag):
        """
        Add a tag to a project.
        :param project_id: The project to add a tag for.
        :param tag: The new tag.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO project_has_tag(project, tag) VALUES(%s,%s)',
                           (project_id, tag))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def set_research_group(self, project_id, group_id):
        """
        Sets the research group of a given project.
        :param project_id: The project ID to set the research group for.
        :param group_id: The new research group ID.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('UPDATE project SET research_group = %s WHERE project_id = %s', (group_id, project_id))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def set_active(self, project_id, active):
        """
        Sets the active status of a project.
        :param project_id: The project ID to update the status for.
        :param active: The new status of the project.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('UPDATE project SET is_active = %s WHERE project_id = %s', (active, project_id))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def update_project(self, project_id, title, max_students, research_group, is_active):
        """
        Updates the info for a project.
        :param project_id: The project ID to update the info for.
        :param title: The new title.
        :param max_students: The new maxumum amount of students that can register.
        :param research_group: The new research group.
        :param is_active: The new activity status of the group.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute(
                'UPDATE project SET title = %s, max_students = %s, research_group = %s, is_active = %s, last_updated = NOW() '
                'WHERE project_id=%s',
                (title, max_students, research_group, is_active, project_id))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    # def mark_all_projects_for_extension(self):
    #     """
    #     Marks all active projects for extension.
    #     :raise: Exception if something went wrong when updating the database.
    #     """
    #     cursor = self.dbconnect.get_cursor()
    #     try:
    #         cursor.execute('UPDATE project SET extension_needed = TRUE WHERE is_active = TRUE')
    #         self.dbconnect.commit()
    #     except:
    #         self.dbconnect.rollback()
    #         raise

    # def extend_project(self, project_id):
    #     """
    #     Extend a project to the next year.
    #     :param project_id: The project to update.
    #     :raise: Exception if the database has to roll back.
    #     """
    #     cursor = self.dbconnect.get_cursor()
    #     try:
    #         cursor.execute('UPDATE project SET extension_needed = FALSE WHERE project_id=%s', (project_id,))
    #         self.dbconnect.commit()
    #     except:
    #         self.dbconnect.rollback()
    #         raise

    def remove_tags(self, project_id):  # TODO move to tag file?
        """
        Removes all the tags from a project in the database.
        :param project_id: The project to remove all tags from.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM project_has_tag WHERE project=%s', (project_id,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def remove_tag(self, project_id, tag):  # TODO move to tag file?
        """
        Adds a tag to a project in the database.
        :param project_id: The project to add a tag for.
        :param tag: The tag to remove from the project.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM project_has_tag '
                           'WHERE project=%s AND tag=%s;',
                           (project_id, tag))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def remove_types(self, project_id):  # TODO move to type file?
        """
        Removes all types from a project in the database.
        :param project_id: The project to remove all types for.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM project_has_type WHERE project=%s', (project_id,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def remove_type(self, project_id, project_type):
        """
        Removes a type from a project in the database.
        :param project_id: The project to remove a type from.
        :param project_type: The type to remove from the project.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM project_has_type '
                           'WHERE project=%s AND type=%s;',
                           (project_id, project_type))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    # def delete_project_extension(self, project_id):
    #     """
    #     Sets a project to inactive and makes it so that an extension is not needed anymore.
    #     :param project_id: The project to update.
    #     :raise: Exception if the database has to roll back.
    #     """
    #     cursor = self.dbconnect.get_cursor()
    #     try:
    #         cursor.execute('UPDATE project SET extension_needed = %s, is_active = FALSE WHERE project_id=%s',
    #                        (False, project_id))
    #         self.dbconnect.commit()
    #     except:
    #         self.dbconnect.rollback()
    #         raise

    # def enforce_extensions(self):
    #     """
    #     Sets all projects where an extension was needed to inactive
    #     :raise: Exception if the database has to roll back.
    #     """
    #     cursor = self.dbconnect.get_cursor()
    #     try:
    #         cursor.execute('UPDATE project SET extension_needed = FALSE, is_active = FALSE WHERE extension_needed = TRUE')
    #         self.dbconnect.commit()
    #     except:
    #         self.dbconnect.rollback()
    #         raise
