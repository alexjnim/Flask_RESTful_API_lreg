### don't run this code, app.py will run this if a sqlite database cannot be found to create a database to store the data
### here we are building the sqlite database with the raw database

import sqlite3
import pandas as pd

connection = sqlite3.connect('data/data.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)
query = "INSERT INTO users VALUES (NULL, ?, ?)"
cursor.execute(query, ("test", "password"))

data = pd.read_csv('data/heart.csv')
data.to_sql("heart", connection, if_exists="replace")

connection.commit()

connection.close()
