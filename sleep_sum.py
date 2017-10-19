# total sleep duration over 12 months

# # average sleep duration over 12 months

# import sqlite3
# import pandas as pd
# import numpy as np

# #connect to the database. You may need to adjust the path
# conn = sqlite3.connect('babysleep.db')
# c = conn.cursor()

# DAY
c.execute('SELECT k.kidID, k.activityAgeMonths, 1.0*SUM(k.durationMin)/30 \
            FROM Kids AS k \
            WHERE k.activity == '"'Sleep'"' AND (k.activityHour BETWEEN 5 AND 18) AND (k.activityAgeMonths >= 0 AND k.activityAgeMonths <= 11)\
            GROUP BY k.kidID, k.activityAgeMonths')
data = c.fetchall() # output is list of tuples

# convert list of tuples to dict then to dataframe
keys = ['kidID','Age','value',]
dataDict = [dict(zip(keys,row)) for row in data]
dfData2 = pd.DataFrame(dataDict)
dfData2 = dfData2.pivot(index='Age', columns='kidID', values='value') #pivot the dataframe into right format for web
dfData2.columns = ['day' + 'k' + str(col) for col in dfData2.columns] # append the prefix for the web

# calculate the meta information
dfmeta = pd.DataFrame(dfData2.median(axis=1), columns={'sleepDay'})
dfmeta['sleepDaySTD1'] = dfmeta['sleepDay'] + dfData2.std(axis=1) 
dfmeta['sleepDaySTD2'] = dfmeta['sleepDay'] - dfData2.std(axis=1)

dfmetaAll = dfmeta
dfDataAll = dfData2



# Night
c.execute('SELECT k.kidID, k.activityAgeMonths, 1.0*SUM(k.durationMin)/30 \
            FROM Kids AS k \
            WHERE k.activity == '"'Sleep'"' AND (k.activityHour < 5 OR k.activityHour >= 17) AND (k.activityAgeMonths >= 0 AND k.activityAgeMonths <= 11)\
            GROUP BY k.kidID, k.activityAgeMonths')
data = c.fetchall() # output is list of tuples

# convert list of tuples to dict then to dataframe
keys = ['kidID','Age','value',]
dataDict = [dict(zip(keys,row)) for row in data]
dfData2 = pd.DataFrame(dataDict)
dfData2 = dfData2.pivot(index='Age', columns='kidID', values='value') #pivot the dataframe into right format for web
dfData2.columns = ['night' + 'k' + str(col) for col in dfData2.columns] # append the prefix for the web

# calculate the meta information
dfmeta = pd.DataFrame(dfData2.median(axis=1), columns={'sleepNight'})
dfmeta['sleepNightSTD1'] = dfmeta['sleepNight'] + dfData2.std(axis=1) 
dfmeta['sleepNightSTD2'] = dfmeta['sleepNight'] - dfData2.std(axis=1)

# join th meta data set and the value data set
dfmetaAll = dfmetaAll.join(dfmeta, how='left', lsuffix='app', rsuffix='web', sort=False)
dfDataAll = dfDataAll.join(dfData2, how='left', lsuffix='app', rsuffix='web', sort=False)



# Total
c.execute('SELECT k.kidID, k.activityAgeMonths, 1.0*SUM(k.durationMin)/30 \
            FROM Kids AS k \
            WHERE k.activity == '"'Sleep'"' AND (k.activityAgeMonths >= 0 AND k.activityAgeMonths <= 11)\
            GROUP BY k.kidID, k.activityAgeMonths')
data = c.fetchall() # output is list of tuples

# convert list of tuples to dict then to dataframe
keys = ['kidID','Age','value',]
dataDict = [dict(zip(keys,row)) for row in data]
dfData2 = pd.DataFrame(dataDict)
dfData2 = dfData2.pivot(index='Age', columns='kidID', values='value') #pivot the dataframe into right format for web
dfData2.columns = ['total' + 'k' + str(col) for col in dfData2.columns] # append the prefix for the web

# calculate the meta information
dfmeta = pd.DataFrame(dfData2.median(axis=1), columns={'sleepTotal'})
dfmeta['sleepTotalSTD1'] = dfmeta['sleepTotal'] + dfData2.std(axis=1) 
dfmeta['sleepTotalSTD2'] = dfmeta['sleepTotal'] - dfData2.std(axis=1)

# join th meta data set and the value data set
dfmetaAll = dfmetaAll.join(dfmeta, how='left', lsuffix='app', rsuffix='web', sort=False)
dfDataAll = dfDataAll.join(dfData2, how='left', lsuffix='app', rsuffix='web', sort=False)



#join the meta information to values
dfOutput = dfmetaAll.join(dfDataAll, how='left', lsuffix='app', rsuffix='web', sort=False)

# set the index to range from 1-12, not 0-11
dfOutput.index = np.arange(1, len(dfOutput) + 1)
dfOutput  = dfOutput.reindex(dfOutput.index.rename('Age'))

# output to tsv
dfOutput.to_csv(outFile + 'sleep_sum.tsv', sep='\t', na_rep='NaN')

# close the database connection
# conn.close() # close the connection to the database