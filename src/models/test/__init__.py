import unittest
import psycopg2
from src.config import *

__all__ = ["test_academic_year", "test_attachment", "test_click", "test_document", "test_employee", "test_guide", "test_like",
           "test_link", "test_registration", "test_project", "test_query", "test_research_group",
           "test_session", "test_student", "test_tag", "test_type"]

if __name__ == "__main__":
    connection1 = psycopg2.connect(user=config_data['dbuser'], password=config_data['dbpass'],
                                   host=config_data['dbhost'], dbname='postgres')
    connection1.autocommit = True
    # Check if database already exists
    cursor = connection1.cursor()
    cursor.execute('DROP DATABASE IF EXISTS test_db')
    cursor.execute('CREATE DATABASE test_db owner len')
    # Create database
    connection2 = psycopg2.connect(user=config_data['dbuser'], password=config_data['dbpass'],
                                   host=config_data['dbhost'], dbname='test_db')
    connection2.autocommit = True
    # Run database schema
    connection2.cursor().execute(open("../../../sql/schema.sql", "r").read())
    connection2.cursor().execute(open("../../../sql/search_view.sql", "r").read())
    connection2.cursor().execute(open("./test_db_inserts.sql", "r").read())
    # Discover all the tests and run
    suite = unittest.TestSuite()
    for t in __all__:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))
    unittest.TextTestRunner().run(suite)
    # Destroy database
    connection2.close()
    connection1.cursor().execute("DROP DATABASE test_db")

