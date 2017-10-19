# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 17:33:29 2015

@author: wayne
"""

# import numpy as np [12]
import pandas as pd
import matplotlib

# setup io file names
inFile = "nyu-170901-1"
inFile2 = "clean_all_fix.csv"
outFile = "clean_all_fix201709.csv"

# load csv
hdr = ['kidID', 'entryID', 'startTime', 'endTime', 'activity','durationMin','quantity','extraData','text','notes','caregiver','childName']
data = pd.read_csv(inFile, header=0, names=hdr,error_bad_lines=False,warn_bad_lines=False,quotechar='"') # quoting=3
data2 = pd.read_csv(inFile2, header=0, names=hdr,error_bad_lines=False,warn_bad_lines=False,quotechar='"') # quoting=3

data_merged = [data, data2]
data_merged = pd.concat(data_merged)

# clean and organize data
# convert timestamps to date/time datatype
data_merged['startTime'] = pd.to_datetime(data_merged['startTime'],errors='coerce')
data_merged['endTime'] = pd.to_datetime(data_merged['endTime'],errors='coerce')

# sort by kidID -> startTime
data_merged.sort_index(by=['kidID', 'startTime'])

# get sleep duration data from 1 kid
# df = data_merged['durationMin']

# filter duration data and plot
# filtered = df[(data_merged['activity'] == "Sleep")]
# filtered.plot(kind='hist', alpha=0.5)

# g = data_merged.groupby('startTime')

# save merged file to csv
data_merged.to_csv(outFile)
