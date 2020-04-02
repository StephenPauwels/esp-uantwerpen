import psycopg2
from src.config import config_data
from flask import g

# @package
#  This package will stand in for the connection with the database.


# Returns a connection to the database
# The connection is stored in a special Flask variable called 'g', which is unique for each request
# This way there is only one connection per request, no matter how many times this function is called
def get_db():
    try:
        if 'db' not in g:
            g.db = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'], dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])
        return g.db
    except:
        return DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'], dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])


# Closes the connection
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# This class stands in for the connection with the database.
class DBConnection:

    # Connection initialiser
    #  @param self object pointer
    #  @param dbname database name
    #  @param dbuser database user
    #  @param dbpass database password
    #  @param dbhost database host
    def __init__(self, dbname, dbuser, dbpass, dbhost):
        try:
            self.conn = psycopg2.connect(
                "dbname='{}' user='{}' host='{}' password='{}'".format(dbname, dbuser, dbhost, dbpass))
        except:
            print('ERROR: Unable to connect to database')
            raise Exception('Unable to connect to database')

    def __del__(self):
        self.close()

    # Closes the connection
    #  @param self object pointer
    def close(self):
        self.conn.close()

    # Returns the connection
    #  @param self object pointer
    def get_connection(self):
        return self.conn

    # Gets the database cursor
    #  @param self object pointer
    def get_cursor(self):
        return self.conn.cursor()

    # Commits the database changes
    #  @param self object pointer
    def commit(self):
        return self.conn.commit()

    # Rolls back the database
    #  @param self object pointer
    def rollback(self):
        return self.conn.rollback()


