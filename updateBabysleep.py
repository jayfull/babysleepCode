import sqlite3
import pandas as pd
import numpy as np
import glob
import os
import sys

######################
####### Inputs #######
######################
os.chdir("/Users/Jay/Dropbox/work/molcajete/babysleep/1017_update/")
list_of_files = glob.glob('webform_views_register_your_baby_for_the_research*') # * means all if need specific format then *.csv
inFileWeb = max(list_of_files, key=os.path.getctime) # get the latest file
print inFileWeb
# inFileWeb = "~/Dropbox/work/molcajete/babysleep/1017_update/webform_views_register_your_baby_for_the_research_study20171001180017.csv"
inFileApp = sys.argv[1]
print inFileApp +'test'
# inFileApp = "~/Dropbox/work/molcajete/babysleep/1017_update/nyu-171001-1.csv"
inFileDB = '/Users/Jay/Dropbox/work/molcajete/babysleep/0917_update/babysleep.db'
outFile = '/Users/Jay/Dropbox/work/molcajete/babysleep/1017_update/'


######################
##### Web Data #######
######################

# load web csv
hdrWeb = (['rID','sID', 'uID', 'instructions', 'instructions1', 'instructions2','instructions3', 'email', 
        'kID','instructionsKid','DOB','gender','firstName','middleInitial','instructions4',
        'instructions5','instructions6','timeStamp','ip'])
register_info_data = pd.read_csv(inFileWeb, header=0, names=hdrWeb,error_bad_lines=False,quotechar='\'',encoding="ISO-8859-1")


# data cleaning on kID
register_info_data['kID'] = pd.to_numeric(register_info_data['kID'], errors='force') # convert ID from string to float
register_info_data = register_info_data.dropna(subset=['kID']) # drop kidIDs that are NaNs 
register_info_data['kID'] = register_info_data['kID'].astype(int) # convert kidID to int

#convert DOB to datetime
register_info_data['DOB'] = pd.to_datetime(register_info_data['DOB'])

print 'test comptete'
# sys.exit()


######################
##### App Data #######
######################

# load app data
hdr = ['kidID', 'entryID', 'startTime', 'endTime', 'activity','durationMin','quantity','extraData','text','notes','caregiver','childName']
appData = pd.read_csv(inFileApp, header=0, names=hdr,error_bad_lines=False,warn_bad_lines=False,quotechar='"') # quoting=3

appData['startTime'] = pd.to_datetime(appData['startTime'],errors='coerce')
appData['endTime'] = pd.to_datetime(appData['endTime'],errors='coerce')




######################
##### Merge Data #####
######################

# Inner join the two data sets so that onl kids with entries in both are included
mergedData = appData.join(register_info_data.set_index('kID'), on='kidID', how='inner', lsuffix='app', rsuffix='web')

#convert activity date strings to datetime data type
mergedData['startTime'] = pd.to_datetime(mergedData['startTime'])
mergedData['endTime'] = pd.to_datetime(mergedData['endTime'])
mergedData['activityHour'] = mergedData['startTime'].dt.hour + 1 # add the startTime as hour interger


#calculate age for each activity 
mergedData['activityAgeDays'] = mergedData['startTime'].values - mergedData['DOB'].values # in days (datetime type)
mergedData['activityAgeDays']= (mergedData['activityAgeDays'].values / np.timedelta64(1, 'D')).astype(int) # convert to integer
mergedData['activityAgeWeeks']= (mergedData['activityAgeDays'] / 7).astype(int) # age in weeks (0 indexed)
mergedData['activityAgeMonths']= (mergedData['activityAgeDays'] / 30).astype(int) # age in months (0 indexed)




##############################
##### Append to Database #####
##############################

# create new db and make connection
conn = sqlite3.connect(inFileDB)
conn.text_factory = str
c = conn.cursor()



#append data to database
mergedData.to_sql(con=conn, name='Kids', if_exists='append', flavor='sqlite', index=False)
conn.commit()

# delete duplicate entries
conn.execute('DELETE FROM Kids WHERE rowid NOT IN \
(SELECT MIN(rowid) FROM Kids \
  GROUP BY entryID)') 
conn.execute('vacuum')
conn.commit()




##############################
####### New Data Files #######
##############################

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