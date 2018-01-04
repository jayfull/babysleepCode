import sqlite3
import csv
import os

inFileDB = '/users/heegeradmin/internal/babysleepDatabase/babysleep.db' #data base location

csvWriter = csv.writer(open("babysleepDB.csv", "w")) # output file for csv dump

# create new db and make connection
conn = sqlite3.connect(inFileDB)
conn.text_factory = str
c = conn.cursor()

# SQL query to select all rows in database
c.execute('SELECT * \
	FROM Kids') 
rows = c.fetchall() 

os.chdir('/users/heegeradmin/internal/babysleepDatabase/')

csvWriter.writerows(rows) # write out the query to the csv