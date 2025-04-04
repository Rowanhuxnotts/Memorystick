# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 14:56:47 2025

@author: lpxrh14
"""
# %% Initialisation

import glob
import pandas as pd
from pandas.api.types import CategoricalDtype
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from scipy.stats import f_oneway
from scipy.stats import ttest_ind
import seaborn as sns

# %% Functions to deal with incoming data


def RemoveDupePresses(InFrame):
    # This function removes any repeated key presses
    # Returns: NewDF a dataframe
    NewDF = pd.DataFrame()
    ListOfSer=[]
    
    for x in range(len(InFrame)):
        if x != len(InFrame)-1 and InFrame.iloc[x]['PressedKey'] != InFrame.iloc[x+1]['PressedKey']:
            Ser = InFrame.iloc[x]
            Ser=Ser.to_frame().T
            ListOfSer.append(Ser)
                
    NewDF = pd.concat(ListOfSer)
    NewDF = NewDF.reset_index()
    return NewDF

#NewDF.drop(["index", "level_0"], axis=1) # Include later on


#   if InFrame.iloc[x]['TrialTime'] - InFrame.iloc[x-1]['TrialTime'] > 0.150:

# %% Participant details and parameters
# (Maybe change to input fields with default)

PartInitials = "RH"
Conditions = ['Left', 'Right']

FilePrefix = "DD_" + PartInitials + "*"

DataLocation = './data/'
SearchTxt = DataLocation + FilePrefix

# %% Read in data and make one dataframe called "AllData" to work off

# @TODO: make this a function

# Create list of all file names
AllFileNames =  []
for File in glob.glob(SearchTxt + ".csv"):
    # small thing: can check for bla*.csv in REGEX
    #CSVCheck = File.split(".")
    #if CSVCheck[2] == "csv":
    AllFileNames.append(File)
        
DataFrames = []
# also good idea to keep a number storing which run
# so enumerate(...)
for (irun,  File) in enumerate(AllFileNames):
    df = pd.read_csv(File)
    NoDupeDF = RemoveDupePresses(df)
    NoDupeDF['run'] = irun
    DataFrames.append(NoDupeDF)

AllData = pd.concat(DataFrames)
# %% Calculations

# data are stored as one big data fram
# group by run, then by condition and then take
# the difference to next event ROW.
#
# we assume that the duration of the previous event extends until the
# next button is pressed. So the last row / event has to be discarded

def calcuateDurations(data):
    #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.diff.html
    d = data.groupby(['run'])['TrialTime'].diff().shift(-1)
    # remove negative durations (edge artifact?)
    d[d < 0] = np.nan
    # has a None in last position (shift -1!)
    data['Duration'] = d
    return data #.reset_index(drop=True)

AllData = calcuateDurations(AllData)

# reorder the categories for PressedKey to be left, right, space
AllData['PressedKey'] = AllData['PressedKey'].astype(CategoricalDtype(ordered=True))
AllData['PressedKey'] = AllData['PressedKey'].cat.reorder_categories(['left', 'right', "space"])

# %% Visualisation

fig, ax = plt.subplots()
ax.scatter(AllData['index'],AllData['TrialTime'])

# %% do the histograms all data just split by left eye / right eye
sns.histplot(data = AllData, x="Duration", 
             hue="PressedKey", kde=True)
# Mixed percept probability %
# p(mixed percept) = #mixed percepts/#non mixed percepts

# %% easier to see / facet by eye and condition

g = sns.FacetGrid(AllData, col="Condition",  row="PressedKey")
g.map(sns.histplot, "Duration", kde=True)

# %%
g = sns.FacetGrid(AllData, row="PressedKey").set(title='Dominance times by Eye')
g.map(sns.histplot, "Duration", kde=True)


# %% Now do some maths on those numbers?

