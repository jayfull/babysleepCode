# # use update_babysleep_jay before this

# import sqlite3
# import pandas as pd
# import numpy as np

# #connect to the database. You may need to adjust the path
# conn = sqlite3.connect('babysleep.db')
# c = conn.cursor()


# #check the columns of the Kids table in the database
# c.execute('select * from Kids')
# names = list(map(lambda x: x[0], c.description))
# names = [description[0] for description in c.description]
# names


##############
### Diaper_eventsLogged
##############

#SQL query
c.execute('select 1.0*count(k.activity)/7, k.kidID, k.activityAgeWeeks \
            from Kids as k \
            Where k.activity == '"'Diaper'"' \
            AND  (k.activityAgeWeeks BETWEEN 0 AND 103) \
            Group by k.kidID, k.activityAgeWeeks')
data = c.fetchall() # output is list of tuples

# convert list of tuples to dict then to dataframe
keys = ['Diaper','kidID','Age',]
dataDict = [dict(zip(keys,row)) for row in data]
dfData = pd.DataFrame(dataDict)
dfData = dfData.pivot(index='Age', columns='kidID', values='Diaper') #pivot the dataframe into right format for web
dfData.columns = ['k' + str(col) for col in dfData.columns] # append the prefix for the web

# calculate the meta information
dfmeta = pd.DataFrame(dfData.median(axis=1), columns={'sleepLogs'})
dfmeta['sleepLogsSEM1'] = dfmeta['sleepLogs'] + dfData.std(axis=1)
dfmeta['sleepLogsSEM2'] = dfmeta['sleepLogs'] - dfData.std(axis=1)
dfmeta['sleepLogsBest'] = dfData.max(axis=1)

#join the meta information to values
dfOutput = dfmeta.join(dfData, how='left', lsuffix='app', rsuffix='web', sort=False)

# set the index to range from 1-12, not 0-11
dfOutput.index = np.arange(1, len(dfOutput) + 1)
dfOutput  = dfOutput.reindex(dfOutput.index.rename('Age'))

# output to tsv
dfOutput.to_csv(outFile + 'diaper_eventsLogged.tsv', sep='\t', na_rep='NaN')


# close the database connection
# conn.close() # close the connection to the database