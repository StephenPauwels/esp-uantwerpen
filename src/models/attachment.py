"""@package
This package enables the attachment usage for the database.
"""


class Attachment:
    """
    This class defines an attachment of a document.
    """

    def __init__(self, name, file_location, document_id):
        """
        Attachment initializer.
        :param name: The name of the attachment file.
        :param file_location: The location of the attachment file.
        :param document_id: The ID of the document the attachment is linked to.
        """
        self.name = name
        self.file_location = file_location
        self.document_id = document_id

    def to_dict(self):
        """
        Converts object to a dictionary.
        :return: Dictionary of the object data.
        """
        return vars(self)


class AttachmentDataAccess:
    """
    This class interacts with the Attachment component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initialises the DocumentDataAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def get_attachments(self, document_id):
        """
        Fetches the attachments for a given document.
        :param document_id: The ID of the document to fetch the attachments for.
        :return: A list of attachment objects.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT name, file_location, document_id FROM attachment WHERE document_id=%s', (document_id,))
        return [Attachment(row[0], row[1], row[2]) for row in cursor]

    def add_attachment(self, obj):
        """
        Adds an attachment to the database.
        :param obj: The new attachment object.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO attachment(name, file_location, document_id) VALUES(%s,%s,%s)',
                           (obj.name, obj.file_location, obj.document_id))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def remove_attachment(self, location):
        """
        Removes an attachment from the database.
        :param location: The location the attachment is at.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM attachment WHERE file_location=%s', (location,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def remove_attachments(self, document_id):
        """
        Remove all attachments for a given document.
        :param document_id: The document ID to remove all attachments for.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM attachment WHERE document_id=%s', (document_id,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise
