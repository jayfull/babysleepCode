import sqlite3
import pandas as pd

#connect to the database. You may need to adjust the path
conn = sqlite3.connect('babysleep.db')
c = conn.cursor()


#check the columns of the Kids table in the database
c.execute('select * from Kids')
names = list(map(lambda x: x[0], c.description))
names = [description[0] for description in c.description]
print names

## get number of kids in the database
# c.execute('SELECT COUNT (DISTINCT kidID) \
# 	FROM Kids') 
# data = c.fetchall() 
# print data

# close the database connection
conn.close() # close the connection to the database