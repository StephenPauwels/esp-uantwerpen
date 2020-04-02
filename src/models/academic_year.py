"""@package
This package enables the academic year usage for the database.
"""


class AcademicYearDataAccess:
    """
    This class interacts with the AcademicYear component of the database.
    """

    def __init__(self, dbconnect):
        """
        Initiates the AcademicYearAccess object.
        :param dbconnect: The database connection.
        """
        self.dbconnect = dbconnect

    def get_academic_years(self):
        """
        Fetches all the academic years from the database.
        :return: List with all the academic years.
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT year FROM academic_year')
        return [row[0] for row in cursor]

    def add_academic_year(self, year):
        """
        Adds an academic year to the database.
        :param year: The new academic year.
        :raise: Exception if the database has to roll back.
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO academic_year(year) VALUES(%s)',
                           (year,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise
