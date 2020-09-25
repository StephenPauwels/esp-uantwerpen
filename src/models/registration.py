"""@package
This package enables the project registration usage for the database.
"""

from datetime import date


class Registration:
    """
    This class defines the student registration for a project.
    """

    def __init__(self, student_id, project_id, reg_type, status, reg_date=date.today().strftime("%Y-%m-%d")):
        """
        Registration initializer.
        :param student_id: Student ID.
        :param project_id: Project ID form the project the student registered for.
        :param reg_type: Registration for a certain type.
        :param status: The status of the registration. (Pending, Passed, Rejected).
        :param reg_date: Date of the last change made to the status of the registration.
        """
        self.student = student_id
        self.project = project_id
        self.reg_type = reg_type
        self.status = status
        self.reg_date = reg_date

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
        cursor.execute('SELECT student, project, type, status, date '
                       'FROM Project_Registration')
        project_registration_objects = list()
        for row in cursor:
            project_registration_obj = Registration(row[0], row[1], row[2], row[3], row[4])
            project_registration_objects.append(project_registration_obj)
        return project_registration_objects

    def get_registration(self, student_id, project_id):  # TODO #2 error for empty fetch
        """
        Fetches a specific project registration from the database.
        :param student_id: The ID of the student that has a registration.
        :param project_id: The ID of the project that the student registered for.
        :return: The registration object.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT student, project, type, status, date FROM Project_Registration '
                       'WHERE student=%s AND project=%s', (student_id, project_id))
        row = cursor.fetchone()
        return Registration(row[0], row[1], row[2], row[3], row[4])

    def get_pending_registrations(self, project_id):  # TODO #2 error for empty fetch
        """
        Fetch the pending registrations for a given project.
        :param project_id: The project ID.
        :return: A list of project registrations.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT student, name, type, date FROM project_registration JOIN student '
                       'ON project_registration.student = student_id '
                       'WHERE project=%s AND status=%s',
                       (project_id, "Pending"))
        registrations = list()
        for row in cursor:
            registrations.append({"student": row[0], "name": row[1], "type": row[2],
                                  "date": {"day": row[3].day, "month": row[3].month, "year": row[3].year}})
        return registrations

    def add_registration(self, obj):
        """
        Adds a project registration to the database.
        :param obj: The new registration object.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO Project_Registration(student, project, type, status, date) '
                           'VALUES(%s,%s,%s,%s,%s)',
                           (obj.student, obj.project, obj.reg_type, obj.status, obj.reg_date))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def update_registration(self, student_id, project_id, new_status, new_type):
        """
        Updates the status of a registration.
        :param student_id: The student ID for which a registration exists.
        :param project_id: The project ID of the registration.
        :param new_status: The new status of the registration.
        :param new_type: The new type the student registered for.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            if new_status and new_type:
                cursor.execute('UPDATE Project_Registration '
                               'SET status = %s, type = %s, date = CURRENT_DATE '
                               'WHERE project=%s AND student=%s',
                               (new_status, new_type, project_id, student_id))
            elif new_status:
                cursor.execute('UPDATE Project_Registration '
                               'SET status = %s, date = CURRENT_DATE '
                               'WHERE project=%s AND student=%s',
                               (new_status, project_id, student_id))
            elif new_type:
                cursor.execute('UPDATE Project_Registration '
                               'SET type = %s '
                               'WHERE project=%s AND student=%s',
                               (new_type, project_id, student_id))
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

    def get_csv_data(self, years):
        """
        Fetch all data with correct csv data
        :return: {list} data.
        """
        date_select = 'where '
        for year in years:
            split = year.split("-")
            date_select += '(PR.date >= \'' + split[0] + '-04-01\' AND '
            date_select += 'PR.date <= \'' + split[1] + '-03-31\') OR '
        date_select = date_select[:-4]
        if len(years) == 0:
            date_select = ""

        cursor = self.dbconnect.get_cursor()
        cursor.execute("select S.student_id, S.name, PR.type, PR.status, PR.date, P.title, string_agg(E.name, ' - ' ORDER BY E.name) "
                       "from project_registration PR "
                       "left join student S on S.student_id = PR.student "
                       "left join guide G on G.project = PR.project "
                       "left join project P on P.project_id = PR.project "
                       "left join employee E on E.id = G.employee "
                       + date_select +
                       "group by PR.status, PR.type, PR.date,S.student_id, S.name, P.title ")
        data = list()
        data.append({"student_id": 'Student ID',
                     "student_name": 'Student Name',
                     "type": 'Type',
                     "status": 'Status',
                     "date": 'Last Change',
                     "title": 'Title',
                     "employee_name": 'Employee Name(s)'})

        for row in cursor:
            data.append({"student_id": row[0],
                         "student_name": row[1],
                         "type": row[2],
                         "status": row[3],
                         "date": str(row[4].day) + "/" + str(row[4].month) + "/" + str(row[4].year),
                         "title": row[5],
                         "employee_name": row[6]})
        return data
