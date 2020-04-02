"""
Installation script
Drops all tables and initializes the database
Usage:
    python3 install.py (filename)
Optional parameter filename: name of sql file that will be executed after initializing
This is useful for start data
"""

from src.models.db import get_db
from src.controllers.tags import construct_tag_database
from src.utils.similarity import construct_link_database
from src.controllers.profile import give_random_pictures
from sys import argv

conn = get_db()
cursor = conn.get_cursor()
connection = conn.get_connection()

print("drop all")

with open("sql/drop_all.sql", "r") as file:
    sql = file.read()

cursor.execute(sql)
connection.commit()

print("schema")

with open("sql/schema.sql", 'r') as file:
    sql = file.read()

cursor.execute(sql)
connection.commit()

if len(argv) == 1:
    exit(0)

old_data_filename = argv[1]

print("import data")

with open(old_data_filename, 'r') as file:
    sql = file.read()

cursor.execute(sql)
connection.commit()

cursor.execute("REFRESH MATERIALIZED VIEW search_index;")
connection.commit()

print("tags")
construct_tag_database()

print("links")
construct_link_database()

print("pics")
give_random_pictures()

