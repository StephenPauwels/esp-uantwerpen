"""@package
This package enables the search query usage for the database.
"""


class Query:
    """
    This class defines a search query.
    """

    def __init__(self, session_id, time_of_query, search_terms):
        """
        Search query initializer.
        :param session_id: The session ID where the queries were entered.
        :param time_of_query: The time the search queries were used.
        :param search_terms: The search queries themselves.
        """
        self.session = session_id
        self.time_of_query = time_of_query
        self.search_terms = search_terms

    def to_dict(self):
        """
        Converts object to a dictionary.
        :return: Dictionary of the object data.
        """
        return vars(self)


class QueryDataAccess:
    """
    This class interacts with the query component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initiates the QueryDataAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def get_queries(self):  # TODO #2 error for empty fetch
        """
        Fetches all the queries from the database.
        :return: A list with all the query objects.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT session, time_of_query, search_terms '
                       'FROM query')
        query_objects = list()
        for row in cursor:
            query_obj = Query(row[0], row[1], row[2])
            query_objects.append(query_obj)
        return query_objects

    def get_query(self, session_id):  # # TODO #2 error for empty fetch + what if more objects?
        """
        Fetches all the queries from a session.
        :param session_id: The session ID to fetch all the queries for.
        :return: A Query object.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT session, time_of_query, search_terms '
                       'FROM query '
                       'WHERE session=%s', (session_id,))
        row = cursor.fetchone()
        return Query(row[0], row[1], row[2])

    def add_query(self, obj):
        """
        Adds a new query to the database.
        :param obj: The new query object.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO query(session, time_of_query, search_terms) '
                           'VALUES(%s,%s,%s)',
                           (obj.session, obj.time_of_query, obj.search_terms))
            self.dbconnect.commit()
            return obj
        except:
            self.dbconnect.rollback()
            raise
