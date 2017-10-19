# use merge_csp.py before this

import sqlite3
import pandas as pd
import numpy as np

inFile = "webform_views_register_your_baby_for_the_research_study20170901120022.csv"

# load web csv
hdrWeb = (['rID','sID', 'uID', 'instructions', 'instructions1', 'instructions2','instructions3', 'email', 
        'kID','instructionsKid','DOB','gender','firstName','middleInitial','instructions4',
        'instructions5','instructions6','timeStamp','ip'])
register_info_data = pd.read_csv(inFile, header=0, names=hdrWeb,error_bad_lines=False,quotechar='\'',encoding="ISO-8859-1")

# data cleaning on kID
register_info_data['kID'] = pd.to_numeric(register_info_data['kID'], errors='force') # convert ID from string to float
register_info_data = register_info_data.dropna(subset=['kID']) # drop kidIDs that are NaNs 
register_info_data['kID'] = register_info_data['kID'].astype(int) # convert kidID to int

#convert DOB to datetime
register_info_data['DOB'] = pd.to_datetime(register_info_data['DOB'])


# load app data
hdrApp = ['kidID', 'entryID', 'startTime', 'endTime', 'activity','durationMin','quantity','extraData','text','notes','caregiver','childName']
appInFile = "clean_all_fix201709.csv"
appData = pd.read_csv(appInFile, header=0, names=hdrApp,error_bad_lines=False,warn_bad_lines=False,quotechar='"') # quoting=3

# Inner join the two data sets so that onl kids with entries in both are included
mergedData = appData.join(register_info_data.set_index('kID'), on='kidID', how='inner', lsuffix='app', rsuffix='web')

#convert activity date strings to datetime data type
mergedData['startTime'] = pd.to_datetime(mergedData['startTime'])
mergedData['endTime'] = pd.to_datetime(mergedData['endTime'])
mergedData['activityHour'] = mergedData['startTime'].dt.hour + 1 # add the startTime as hour interger


#calculate age for each activity 
mergedData['activityAgeDays'] = mergedData['startTime'] - mergedData['DOB'] # in days (datetime type)
mergedData['activityAgeDays']= (mergedData['activityAgeDays'] / np.timedelta64(1, 'D')).astype(int) # convert to integer
mergedData['activityAgeWeeks']= (mergedData['activityAgeDays'] / 7).astype(int) # age in weeks (0 indexed)
mergedData['activityAgeMonths']= (mergedData['activityAgeDays'] / 30).astype(int) # age in months (0 indexed)


## APPEND TO DATABASE
# create new db and make connection
conn = sqlite3.connect('babysleep.db')
conn.text_factory = str

mergedData.to_sql(con=conn, name='Kids', if_exists='replace', flavor='sqlite', index=False)

# delete duplicate entries
c.execute('DELETE FROM Kids WHERE rowid NOT IN \
(SELECT MIN(rowid) FROM Kids \
  GROUP BY entryID)') 
c.execute('vacuum')

conn.close()