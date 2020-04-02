"""@package
This package enables the project registration usage for the database.
"""


class Registration:
    """
    This class defines the student registration for a project.
    """

    def __init__(self, student_id, project_id, status):
        """
        Registration initializer.
        :param student_id: Student ID.
        :param project_id: Project ID form the project the student registered for.
        :param status: The status of the registration. (Pending, Passed, Rejected)
        """
        self.student = student_id
        self.project = project_id
        self.status = status

    def to_dict(self):
        """
        Converts object to a dictionary.
        :return: Dictionary of the object data.
        """
        return vars(self)


class RegistrationDataAccess:
    """
    This class interacts with the registration component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initiates the RegistrationDataAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def get_registrations(self):  # TODO #2 error for empty fetch
        """
        Fetches all the project registrations in the database.
        :return: Al list with all the resgitration objects.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT student, project, status '
                       'FROM Project_Registration')
        project_regsitartion_objects = list()
        for row in cursor:
            project_regsitartion_obj = Registration(row[0], row[1], row[2])
            project_regsitartion_objects.append(project_regsitartion_obj)
        return project_regsitartion_objects

    def get_registration(self, student_id, project_id):  # TODO #2 error for empty fetch
        """
        Fetches a specific project registration from the database.
        :param student_id: The ID of the student that has a registration.
        :param project_id: The ID of the project that the student registered for.
        :return: The registration object.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT student, project, status FROM Project_Registration '
                       'WHERE student=%s AND project=%s', (student_id, project_id))
        row = cursor.fetchone()
        return Registration(row[0], row[1], row[2])

    def get_pending_registrations(self, project_id):  # TODO #2 error for empty fetch
        """
        Fetch the pending registrations for a given project.
        :param project_id: The project ID.
        :return: A list of project registrations.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT student, name FROM project_registration JOIN student '
                       'ON project_registration.student = student_id '
                       'WHERE project=%s AND status=%s',
                       (project_id, "Pending"))
        registrations = list()
        for row in cursor:
            registrations.append({"student": row[0], "name": row[1]})
        return registrations

    def add_registration(self, obj):
        """
        Adds a project registration to the database.
        :param obj: The new registration object.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO Project_Registration(student, project, status) '
                           'VALUES(%s,%s,%s)',
                           (obj.student, obj.project, obj.status))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def update_registration(self, student_id, project_id, new_status):
        """
        Updates the status of a registration.
        :param student_id: The student ID for which a registration exists.
        :param project_id: The project ID of the registration.
        :param new_status: The new status of the registration.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('UPDATE Project_Registration '
                           'SET status = %s '
                           'WHERE project=%s AND student=%s',
                           (new_status, project_id, student_id))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def delete_registration(self, student_id):
        """
        Delete a registration for a given student.
        :param student_id: The ID of the student to delete all registrations for.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM project_registration '
                           'WHERE student=%s', (student_id,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def get_csv_data(self):
        """
        Fetch all data with correct csv data
        :return: {list} data.
        """

        cursor = self.dbconnect.get_cursor()
        cursor.execute("select S.student_id, S.name, PR.status, P.title, string_agg(E.name, ' - ' ORDER BY E.name) "
                       "from project_registration PR "
                       "left join student S on S.student_id = PR.student "
                       "left join guide G on G.project = PR.project "
                       "left join project P on P.project_id = PR.project "
                       "left join employee E on E.id = G.employee "
                       "group by PR.status, S.student_id, S.name, P.title")
        data = list()
        data.append({"student_id": 'student_id',
                     "student_name": 'student_name',
                     "status": 'status',
                     "title": 'title',
                     "employee_name": 'employee_name'})

        for row in cursor:
            data.append({"student_id": row[0],
                         "student_name": row[1],
                         "status": row[2],
                         "title": row[3],
                         "employee_name": row[4]})
        return data
