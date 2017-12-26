import sqlite3
import pandas as pd
import numpy as np
import glob
import os
import sys


os.chdir("/users/heegeradmin/internal/ParticipantDataDumps/")
list_of_files = glob.glob('webform_views_register_your_baby_for_the_research*') # * means all if need specific format then *.csv
inFileWeb = "/users/heegeradmin/internal/ParticipantDataDumps/" + max(list_of_files, key=os.path.getctime) # get the latest file
inFileDB = sys.argv[1] # name of the DB must be given on the command line
inFilesApp = glob.glob("/users/heegeradmin/internal/babysleepAppData/*.csv")
# print inFilesApp


os.chdir("/users/heegeradmin/internal/babysleepDatabase/")
# create new db and make connection
conn = sqlite3.connect(inFileDB)
conn.text_factory = str
c = conn.cursor()


os.chdir("/users/heegeradmin/internal/babysleepCode/")
for inFileApp in inFilesApp[:1]:
	sys.argv = [inFileWeb, inFileApp]
	print sys.argv
	execfile("dataToDB.py")


# close the database connection
conn.close() # close the connection to the database