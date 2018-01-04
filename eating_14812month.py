
import sqlite3
import pandas as pd
import numpy as np

#connect to the database. You may need to adjust the path
# conn = sqlite3.connect('babysleep.db')
# c = conn.cursor()

# Pull in the parameters and put them in a tuple fo the SQL commmand
params = json.load(open('/users/heegeradmin/internal/babysleepCode/babysleepParams.json'))
min_duration = params.get('eating').get('min_duration')
max_duration = params.get('eating').get('max_duration')
durations = (min_duration, max_duration)
print min_duration
print max_duration


##############
### Eating_eventsLogged by month and hour
##############


###################################
# MONTH 1
###################################

# proportion of diaper events by hour of day for a particular month. The subquerey gets the monthly totals. Those are joined on to the main data set based on kidID and filtered for age and activity type. The data is grouped by kidID and hour. Finally, the activity for each hour is counted and divided by the monthly total.
# I am not grouping by month becasue I need to change the header for each different month and so I need to tell the months, so I am running each month seperately
c.execute('SELECT k2.kidID, k2.activityHour, 1.0*count(k2.activity) / month.total \
            FROM Kids AS k2 \
            LEFT JOIN \
              (select k.kidID AS id, k.activityAgeMonths AS age, count(k.activity) AS total \
                FROM Kids AS k \
                WHERE k.activity == '"'Bottle'"' OR k.activity == '"'Nursing'"' OR k.activity == '"'Solid Food'"' \
                AND (k.activityAgeMonths BETWEEN 0 AND 11) \
                Group by k.kidID, k.activityAgeMonths) \
                AS month \
             ON k2.kidID = month.id \
                AND k2.activityAgeMonths = month.age \
             WHERE k2.activityAgeMonths == 0 AND (k2.activity == '"'Bottle'"' OR k2.activity == '"'Nursing'"' OR k2.activity == '"'Solid Food'"') \
                AND (k2.DurationMin BETWEEN ? AND ?) \
             GROUP BY k2.kidID, k2.activityHour', durations)
data = c.fetchall() # output is list of tuples

# convert list of tuples to dict then to dataframe
keys = ['kidID','hour','Proportion',]
dataDict = [dict(zip(keys,row)) for row in data]
dfData = pd.DataFrame(dataDict)
dfData = dfData.pivot(index='hour', columns='kidID', values='Proportion') #pivot the dataframe into right format for web
dfData.columns = ['m1k' + str(col) for col in dfData.columns] # append the prefix for the web

dfmeta = pd.DataFrame(dfData.median(axis=1), columns={'Var2'})

dfDiaper = dfData


###################################
# MONTH 4
###################################
c.execute('SELECT k2.kidID, k2.activityHour, 1.0*count(k2.activity) / month.total \
            FROM Kids AS k2 \
            LEFT JOIN \
              (select k.kidID AS id, k.activityAgeMonths AS age, count(k.activity) AS total \
                FROM Kids AS k \
                Where k.activity == '"'Bottle'"' OR k.activity == '"'Nursing'"' OR k.activity == '"'Solid Food'"' \
                AND (k.activityAgeMonths BETWEEN 0 AND 11) \
                Group by k.kidID, k.activityAgeMonths) \
                AS month \
             ON k2.kidID = month.id \
                AND k2.activityAgeMonths = month.age \
             WHERE k2.activityAgeMonths == 3 AND (k2.activity == '"'Bottle'"' OR k2.activity == '"'Nursing'"' OR k2.activity == '"'Solid Food'"') \
                AND (k2.DurationMin BETWEEN ? AND ?) \
             GROUP BY k2.kidID, k2.activityHour', durations)
data = c.fetchall() # output is list of tuples

# convert list of tuples to dict then to dataframe
keys = ['kidID','hour','Proportion',]
dataDict = [dict(zip(keys,row)) for row in data]
dfData = pd.DataFrame(dataDict)
dfData = dfData.pivot(index='hour', columns='kidID', values='Proportion') #pivot the dataframe into right format for web
dfData.columns = ['m2k' + str(col) for col in dfData.columns] # append the prefix for the web

dfmeta.insert(1, 'Var3', dfData.mean(axis=1))

dfDiaper = dfDiaper.join(dfData, how='left', lsuffix='app', rsuffix='web', sort=False) # join months 1 and 4


###################################
# MONTH 8
###################################
c.execute('SELECT k2.kidID, k2.activityHour, 1.0*count(k2.activity) / month.total \
            FROM Kids AS k2 \
            LEFT JOIN \
              (select k.kidID AS id, k.activityAgeMonths AS age, count(k.activity) AS total \
                FROM Kids AS k \
                Where k.activity == '"'Bottle'"' OR k.activity == '"'Nursing'"' OR k.activity == '"'Solid Food'"' \
                AND (k.activityAgeMonths BETWEEN 0 AND 11) \
                Group by k.kidID, k.activityAgeMonths) \
                AS month \
             ON k2.kidID = month.id \
                AND k2.activityAgeMonths = month.age \
             WHERE k2.activityAgeMonths == 7 AND (k2.activity == '"'Bottle'"' OR k2.activity == '"'Nursing'"' OR k2.activity == '"'Solid Food'"') \
                AND (k2.DurationMin BETWEEN ? AND ?) \
             GROUP BY k2.kidID, k2.activityHour', durations)
data = c.fetchall() # output is list of tuples

# convert list of tuples to dict then to dataframe
keys = ['kidID','hour','Proportion',]
dataDict = [dict(zip(keys,row)) for row in data]
dfData = pd.DataFrame(dataDict)
dfData = dfData.pivot(index='hour', columns='kidID', values='Proportion') #pivot the dataframe into right format for web
dfData.columns = ['m3k' + str(col) for col in dfData.columns] # append the prefix for the web

dfmeta.insert(2, 'Var4', dfData.mean(axis=1))

dfDiaper = dfDiaper.join(dfData, how='left', lsuffix='app', rsuffix='web', sort=False)  # join months 1 and 4 and 8


###################################
# MONTH 12
###################################
c.execute('SELECT k2.kidID, k2.activityHour, 1.0*count(k2.activity) / month.total \
            FROM Kids AS k2 \
            LEFT JOIN \
              (select k.kidID AS id, k.activityAgeMonths AS age, count(k.activity) AS total \
                FROM Kids AS k \
                Where k.activity == '"'Bottle'"' OR k.activity == '"'Nursing'"' OR k.activity == '"'Solid Food'"' \
                AND (k.activityAgeMonths BETWEEN 0 AND 11) \
                Group by k.kidID, k.activityAgeMonths) \
                AS month \
             ON k2.kidID = month.id \
                AND k2.activityAgeMonths = month.age \
             WHERE k2.activityAgeMonths == 11 AND (k2.activity == '"'Bottle'"' OR k2.activity == '"'Nursing'"' OR k2.activity == '"'Solid Food'"') \
                AND (k2.DurationMin BETWEEN ? AND ?) \
             GROUP BY k2.kidID, k2.activityHour', durations)
data = c.fetchall() # output is list of tuples

# convert list of tuples to dict then to dataframe
keys = ['kidID','hour','Proportion',]
dataDict = [dict(zip(keys,row)) for row in data]
dfData = pd.DataFrame(dataDict)
dfData = dfData.pivot(index='hour', columns='kidID', values='Proportion') #pivot the dataframe into right format for web
dfData.columns = ['m12k' + str(col) for col in dfData.columns] # append the prefix for the web

dfmeta.insert(3, 'Var5', dfData.mean(axis=1))

dfDiaper = dfDiaper.join(dfData, how='left', lsuffix='app', rsuffix='web', sort=False) # join months 1 and 4 and 8 and 12




##############################
## OUTPUT
##############################

# JOIN THE META INFO WIITH THE MONTH INFO
dfOutput = dfmeta.join(dfDiaper, how='left', lsuffix='app', rsuffix='web', sort=False)
dfOutput  = dfOutput.reindex(dfOutput .index.rename('Age'))

# output to tsv
dfOutput.to_csv(outFile + 'eating_14812month.tsv', sep='\t', na_rep='NaN')

# close the database connection
# conn.close() # close the connection to the database