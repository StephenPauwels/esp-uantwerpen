"""@package
This package enables the session usage for the database.
"""


class Session:
    """
    This class defines a browser session.
    """

    def __init__(self, session_id, student, start_of_session):
        """
        Session initializer.
        :param session_id: The session ID.
        :param student: The student that made the session.
        :param start_of_session: The timestamp marking the start of the session.
        """
        self.session_id = session_id
        self.student = student
        self.start_of_session = start_of_session

    def to_dict(self):
        """
        Converts object to a dictionary.
        :return: Dictionary of the object data.
        """
        return vars(self)


class SessionDataAccess:
    """
    This class interacts with the Session component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initiates the SessionDataAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def get_sessions(self):  # TODO #2 catching empty fetch?
        """
        Fetches all the sessions from the database.
        :return: A list of all the sessions in the database.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT session_id, student, start_of_session FROM session')
        session_objects = list()
        for row in cursor:
            session_obj = Session(row[0], row[1], row[2])
            session_objects.append(session_obj)
        return session_objects

    def get_session(self, session_id):  # TODO #2 catching empty fetch?
        """
        Fetches a specific session from the database.
        :param session_id: The session ID to fetch.
        :return: The fetched session object.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT session_id, student, start_of_session FROM session '
                       'WHERE session_id=%s', (session_id,))
        row = cursor.fetchone()
        return Session(row[0], row[1], row[2])

    def add_session(self, obj):
        """
        Adds a session to the database.
        :param obj: The new session.
        :return: The newly made session object
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO session(student, start_of_session) VALUES(%s,%s)',
                           (obj.student, obj.start_of_session))
            # Get session ID and return updated object
            cursor.execute('SELECT LASTVAL()')
            iden = cursor.fetchone()[0]
            obj.session_id = iden
            self.dbconnect.commit()
            return obj  # TODO return already made object?
        except:
            self.dbconnect.rollback()
            raise

    def get_student_clicks(self, student_id):  # TODO correct location? + #2 catching empty fetch?
        """
        Fetches the student clicks.
        :param student_id: The student ID.
        :return: Dictionary with project_id as a key, and amount of clicks a value.
        """
        cursor = self.dbconnect.get_cursor()

        cursor.execute('SELECT COUNT(time_of_click), project '
                       'FROM project_click JOIN session s on project_click.session = s.session_id '
                       'WHERE s.student = %s '
                       'GROUP BY project '
                       'ORDER BY COUNT(time_of_click) DESC',
                       (student_id,))

        result = dict()
        for row in cursor:
            result[row[1]] = row[0]
        return result
