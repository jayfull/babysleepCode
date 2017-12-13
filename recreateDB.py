import sqlite3
import pandas as pd
import numpy as np
import glob
import os
import sys

inFileDB = sys.argv[1] # name of the DB must be given on the command line

# create new db and make connection
conn = sqlite3.connect(inFileDB)
conn.text_factory = str
c = conn.cursor()

import glob
files = glob.glob("/users/heegeradmin/internal/babysleepAppData/*.csv")

for file in files[0]:
	sys.argv = [file]
	# execfile("updateBabysleep.py")


# close the database connection
conn.close() # close the connection to the database