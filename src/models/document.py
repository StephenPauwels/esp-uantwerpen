"""@package
This package enables the document usage for the database.
"""


class Document:
    """
    This class defines a document (description, pdf file...).
    """

    def __init__(self, document_id, html_content_eng, html_content_nl):
        """
        Document initializer.
        :param document_id: The ID of the document.
        :param html_content_eng: If description, the english HTML content.
        :param html_content_nl: If description, the dutch HTML content.
        """
        self.document_id = document_id
        self.html_content_eng = html_content_eng
        self.html_content_nl = html_content_nl

    def to_dict(self):
        """
        Converts object to a dictionary.
        :return: Dictionary of the object data.
        """
        return vars(self)


class DocumentDataAccess:
    """
    This class interacts with the Document component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initialises the DocumentDataAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def add_document(self, obj):
        """
        Adds a document to the database.
        :param obj: The new document object.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO document(html_content_eng, html_content_nl) VALUES(%s,%s)',
                           (obj.html_content_eng, obj.html_content_nl))

            # get id and return updated object
            cursor.execute('SELECT LASTVAL()')
            iden = cursor.fetchone()[0]
            obj.document_id = iden

            self.dbconnect.commit()
            return obj
        except:
            self.dbconnect.rollback()
            raise

    def update_document(self, obj):
        """
        Updates a document in the database.
        :param obj: The new document object.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('UPDATE document SET html_content_nl = %s, html_content_eng = %s WHERE document_id = %s',
                           (obj.html_content_nl, obj.html_content_eng, obj.document_id))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise

    def get_documents(self):
        """
        Fetches all the documents in the database.
        :return: A list with all the document objects.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT document_id, html_content_eng, html_content_nl FROM Document')
        document_objects = list()
        for row in cursor:
            document_obj = Document(row[0], row[1], row[2])
            document_objects.append(document_obj)
        return document_objects

    def get_document(self, document_id):
        """
        Fetches a specific document from the database.
        :param document_id: The ID of the document.
        :return: The document object.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT document_id, html_content_eng, html_content_nl FROM Document '
                       'WHERE document_id=%s', (document_id,))
        row = cursor.fetchone()
        return Document(row[0], row[1], row[2])

    def copy_document(self, document_id):
        doc = self.get_document(document_id)
        return self.add_document(doc).document_id

