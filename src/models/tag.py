"""@package
This package enables the project tag usage for the database.
This does not have a Tag class because it is only a string and has no other attributes.
"""


class TagDataAccess:
    """
    This class interacts with the Tag component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initiates the TagDataAccess object.
        :param dbconnect: Database connection.
        """
        self.dbconnect = dbconnect

    def get_tags(self):  # TODO #2 catching empty fetch?
        """
        Fetches all tags from the database.
        :return: List with all the tags.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT tag FROM tag')
        return [row[0] for row in cursor]

    def add_tag(self, tag_name):
        """
        Adds a tag to the database.
        :param tag_name: The name of the Tag.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO tag(tag) VALUES(%s)', (tag_name,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def remove_tag(self, tag_name):
        """
        Removes a tag from the database.
        :param tag_name: The name of the Tag.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM tag WHERE tag = %s', (tag_name,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def update_tag(self, tag_name, new_tag_name):
        """
        Updates a tag in the database.
        :param tag_name: The current name of the Tag.
        :param new_tag_name: The new name of the Tag.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('UPDATE tag SET tag = %s WHERE tag = %s;', (new_tag_name, tag_name))
            # Get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise
