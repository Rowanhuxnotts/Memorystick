# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 14:56:47 2025

@author: lpxrh14
"""
# %% Initialisation

import glob
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib as plt
from scipy.stats import f_oneway
from scipy.stats import ttest_ind

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

# Create list of all file names
AllFileNames =  []
for File in glob.glob(SearchTxt):
    CSVCheck = File.split(".")
    if CSVCheck[2] == "csv":
        AllFileNames.append(File)
        
DataFrames = []
for File in AllFileNames:
    df = pd.read_csv(File)
    NoDupeDF = RemoveDupePresses(df)
    DataFrames.append(NoDupeDF)
    
AllData = pd.concat(DataFrames)
# %% Calculations
fig, ax = plt.subplots()
ax.scatter(AllData['index'],AllData['TrialTime'])

# Mixed percept probability %
# p(mixed percept) = #mixed percepts/#non mixed percepts

