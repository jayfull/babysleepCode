import sqlite3
import pandas as pd
import numpy as np
import glob
import os
import sys

######################
####### Inputs #######
######################
os.chdir("/users/heegeradmin/internal/ParticipantDataDumps/")
list_of_files = glob.glob('webform_views_register_your_baby_for_the_research*') # * means all if need specific format then *.csv
inFileWeb = max(list_of_files, key=os.path.getctime) # get the latest file
inFileApp = sys.argv[1] # /users/heegeradmin/internal/babysleepAppData
inFileDB = '/users/heegeradmin/internal/babysleepDatabase/babysleep.db'
outFile = '/users/heegeradmin/Sites/sites/dashboard/assets/data/'

# sys.exit()


##############################
####### New Data Files #######
##############################

os.chdir("/users/heegeradmin/internal/babysleepCode/")

# generate TSV files
execfile("eating_14812month.py")
execfile("eating_eventsLogged.py")
execfile("diaper_14812month.py")
execfile("diaper_eventsLogged.py")
execfile("sleep_14812month.py")
execfile("sleep_eventsLogged.py")
execfile("sleep_boutDuration.py")
execfile("sleep_sum.py")


conn.close()

print "Babysleep update successfully completed."