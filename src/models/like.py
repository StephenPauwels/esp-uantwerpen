"""@package
This package enables the like usage for the database.
"""


class Like:
    """
    This class defines a project like.
    """

    def __init__(self, student_id, project):
        """
        Like initializer.
        :param student_id: The ID of the student that produced the like.
        :param project: The project the student liked.
        """
        self.student = student_id
        self.project = project

    def to_dict(self):
        """
        Converts object to a dictionary.
        :return: Dictionary of the object data.
        """
        return vars(self)


class LikeDataAccess:
    """
    This class interacts with the like component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initiates the LikeDataAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def is_liked(self, project_id, student_id):
        """
        Checks whether a given student liked a given project.
        :param project_id: The ID of the project.
        :param student_id: The ID of the student.
        :return: True if the student liked the project. False otherwise.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT project FROM "like" WHERE project = %s AND student = %s',
                       (project_id, student_id))
        result = cursor.fetchone()
        return result is not None

    def add_like(self, obj):
        """
        Adds a like to the database.
        :param obj: The new like object.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO "like"(student, project) VALUES(%s,%s)',
                           (obj.student, obj.project))
            self.dbconnect.commit()
            return obj
        except:
            self.dbconnect.rollback()
            raise

    def remove_like(self, student_id, project_id):
        """
        Removes a like from the database.
        :param student_id: The ID of the student that removed the like.
        :param project_id: The ID of the project.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM "like" WHERE student=%s AND project=%s',
                           (student_id, project_id))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def get_student_likes(self, student_id):
        """
        Fetches the likes for a given student.
        :param student_id: The ID of the student.
        :return: A set with project ID's.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT project FROM "like" '
                       'WHERE student=%s', (student_id,))
        likes = set()
        for row in cursor:
            likes.add(row[0])
        return likes
