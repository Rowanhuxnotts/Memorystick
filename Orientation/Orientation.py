#! /usr/bin/env python
"""
Orientation.py

Partial replication of Wilson et al 2001
Radial, Concentric, and Spiral annuli are rivaled
againt a spiral annulus.

Requires:
    Participant param file (e.g. RH.csv) made my ContrastSens.py
    Participant Averages file (e.g. RHAverages.csv) that will need to be made manually (for now)

RH 30/01/25

"""

# Import modules
import psychopy # for version checking etc.
from psychopy import *
# Check version / deal with stimuli slightly differently
version = psychopy.__version__
psychopy_modern = False 
if str(version) < '2020.1.0':
    print("running in lab - older version of psychopy")
    psychopy_modern = False
else:   
    print("running somewhere else - modern version of psychopy")
    psychopy_modern = True
    psychopy.plugins.activatePlugins() # needed for modern version
    visual.PatchStim = visual.GratingStim # PatchStim migrated to GratingStim in newer versions

from numpy import *
from scipy import *
import time, copy 
from datetime import datetime
from numpy.random import shuffle
import csv
import random as rand

#--------------------------------------
#              Initialisation
#--------------------------------------

simulationMode = False

if simulationMode:
    print("Running in simulation mode")
    # present 3x smaller
    resX=1680/2.5
    resY=1050/2.5
    theMonitor = 'testMonitor' # ?? CHANGE??
    fullscrMode = False
    pos = [[50,50],[100+resX, 50]] # offset 2 windows
    allowGUI = True
    viewScale = [0.4, 0.4]
    from spiral import *

else:
    print("Running in experiment mode")
    resX=1680
    resY=1050
    theMonitor = 'testMonitor'
    pos = [[0,0],[0,0]] # DON'T offset 2 windows
    allowGUI = False
    viewScale = [1, 1]
    fullscrMode = True
    
# Experiment params
NumTrials = 5

# Get Date and start time
now = datetime.now()
Date = now.strftime('%d%m%y_%H%M')

# present a dialogue box for changing params
params = {'Observer':''}
paramsDlg2 = gui.DlgFromDict(params, title='Travelling Waves Basic', fixed=['date'])
Name = params['Observer']
Name=Name.upper()

# Read in participant parameter file
RowsParams = []
PartParamsCSVName= './ParticipantFiles/' + Name + '.csv'
try:
    with open(PartParamsCSVName) as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        for row in reader:
            RowsParams.append(row)
    PartParams = RowsParams[1]
    LEContrast = PartParams[8]
    REContrast = PartParams[9]
except:
    print("No participant parameter file, please run ContrastSens.py to generate file.")
    quit()

# Read in participant averages file
RowsAverages = []
AveragesCSVName= "./ParticipantFiles/" + Name + 'Averages.csv'
try:
    with open(AveragesCSVName) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            RowsAverages.append(row)
    RadAvSpeed = RowsAverages[0]
    SpirAvSpeed = RowsAverages[1]
    ConcAvSpeed = RowsAverages[2]
    
    RadAvSpeed = list(map(float, RadAvSpeed))
    SpirAvSpeed = list(map(float, SpirAvSpeed))
    ConcAvSpeed = list(map(float, ConcAvSpeed))
except:
    RadAvSpeed = []
    SpirAvSpeed = []
    ConcAvSpeed = []



ConditionList = ["RadialL", "RadialR", "SpiralL", "SpiralR", "ConcentricL", "ConcentricR"] 
 
Exp = data.TrialHandler(ConditionList,NumTrials, method='random', dataTypes=None, extraInfo=None,seed=None,originPath=None)

# Setup window (this works on old as well as new versions)
winL = visual.Window(size=(resX,resY), 
                     monitor=theMonitor, units='pix', 
                     bitsMode=None, fullscr=fullscrMode, 
                     allowGUI=allowGUI, color=0.0,screen=0, pos = pos[0], viewScale=viewScale)
winR = visual.Window(size=(resX,resY), 
                     monitor=theMonitor, units='pix', 
                     bitsMode=None, fullscr=fullscrMode, 
                     allowGUI=allowGUI, color=0.0,screen=1, pos = pos[1], viewScale=viewScale)

# Clock
Clock = core.Clock()
ResponseClock = core.Clock()
#--------------------------------------
#            Create stimlui 
#--------------------------------------

# Create stimlui initial stimuli
# RadialStim has changed / been moved in newer versions of psychopy, 
# so deal with this separately !
def createRadialStim(winL, winR, resY, aCycles = 27, c=-1, aRes = 35, units="pix", visWedge=(0,360), TvisWedge=(0,30), ori=(-10), contrast=(LEContrast, REContrast), Condition="RadialL", simulationMode=simulationMode):
    """
    creates radial patches and returns the radial stim, concentric stim, 
    spiral stim, and masks for L and R

    Forgive me for the unholy elif chain, I will work out a cleaner solution.
    """
    if simulationMode: # Change stim size in simulation vs lab
        SizeAdjust = 15
    else:
        SizeAdjust = 515
    # Refused to take the contrast[0] as a float without this...
    LECont = float(contrast[0])
    RECont = float(contrast[1])
    LECarrierCont = (LECont / 100) * 70
    RECarrierCont = (RECont / 100) * 70
    if simulationMode == False: # When in simulation mode a different module is used
        if Condition == "RadialL": # for displaying on lab
           LeftEye = visual.RadialStim(winL,size=resY-SizeAdjust,angularCycles=aCycles, color=c, angularRes=aRes, 
                                 units=units, radialCycles = 0, visibleWedge=visWedge, contrast=LECarrierCont)
        
           RightEye = visual.spiralStim(winR,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes = aRes,
                                  units=units, radialCycles=0, visibleWedge=visWedge, contrast = contrast[1])
    
           Trigger = visual.RadialStim(winL,size=resY-SizeAdjust,angularCycles=aCycles, color=-1,angularRes=35,
                                  units="pix", radialCycles=0, visibleWedge=(TvisWedge), 
                                  ori=ori, contrast = 0.9)
    
        elif Condition == "RadialR":
           LeftEye = visual.spiralStim(winL,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes=aRes, 
                                 units=units, radialCycles = 0, visibleWedge=visWedge, contrast = contrast[0])
        
           RightEye = visual.RadialStim(winR,size=resY-SizeAdjust,angularCycles=aCycles, color=c, angularRes = aRes,
                                  units=units, radialCycles= 0, visibleWedge=visWedge, contrast = RECarrierCont)
    
           Trigger = visual.RadialStim(winR,size=resY-SizeAdjust,angularCycles=aCycles, color=-1,angularRes=35,
                                  units="pix", radialCycles = 0, visibleWedge = (TvisWedge), 
                                  ori=ori, contrast = 0.9)
                                  
        elif Condition == "SpiralL":
           LeftEye = visual.spiralStim(winL,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes=aRes, 
                                 units=units, radialCycles = 0, visibleWedge=visWedge, contrast = LECarrierCont, carrier=True)
        
           RightEye = visual.spiralStim(winR,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes = aRes,
                                  units=units, radialCycles= 0, visibleWedge=visWedge, contrast = contrast[1])
    
           Trigger = visual.spiralStim(winL,size=resY-SizeAdjust,angularCycles=20, color=-1,angularRes=35,
                                  units="pix", radialCycles = 0, visibleWedge = (TvisWedge), 
                                  ori=ori, contrast = 0.9, carrier=True)
                                  
        elif Condition == "SpiralR":
           LeftEye = visual.spiralStim(winL,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes=aRes, 
                                 units=units, radialCycles = 0, visibleWedge=visWedge, contrast = contrast[0])
        
           RightEye = visual.spiralStim(winR,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes = aRes,
                                  units=units, radialCycles= 0, visibleWedge=visWedge, contrast = RECarrierCont, carrier=True)
    
           Trigger = visual.spiralStim(winR,size=resY-SizeAdjust,angularCycles=20, color=-1,angularRes=35,
                                  units="pix", radialCycles = 0, visibleWedge = (TvisWedge), 
                                  ori=ori, contrast = 0.9, carrier=True)
                                  
        elif Condition =="ConcentricL":
           LeftEye = visual.RadialStim(winL,size=resY-SizeAdjust,angularCycles=0, color=c, angularRes=aRes, 
                                 units=units, radialCycles = 8, visibleWedge=visWedge, contrast = LECarrierCont)
    
           RightEye = visual.spiralStim(winR,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes = aRes,
                                  units=units, radialCycles= 0, visibleWedge=visWedge, contrast = RECarrierCont)
    
           Trigger = visual.RadialStim(winL,size=resY-SizeAdjust,angularCycles=0, color=-1,angularRes=35,
                                  units="pix", radialCycles = 8, visibleWedge = (TvisWedge), 
                                  ori=ori, contrast = 0.9)
                                  
        elif Condition =="ConcentricR":
           LeftEye = visual.spiralStim(winL,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes=aRes, 
                                 units=units, radialCycles = 0, visibleWedge=visWedge, contrast = contrast[0])
        
           RightEye = visual.RadialStim(winR,size=resY-SizeAdjust,angularCycles=0, color=c, angularRes = aRes,
                                  units=units, radialCycles= 8, visibleWedge=visWedge, contrast = RECarrierCont)
                 
           Trigger = visual.RadialStim(winR,size=resY-SizeAdjust,angularCycles=0, color=-1,angularRes=35,
                                  units="pix", radialCycles = 8, visibleWedge = (TvisWedge), 
                                  ori=ori, contrast = 0.9)
    else: 
        if Condition == "RadialL": # for displaying on sim
            LeftEye = visual.RadialStim(winL,size=resY-SizeAdjust,angularCycles=aCycles, color=c, angularRes=aRes, 
                             units=units, radialCycles = 0, visibleWedge=visWedge, contrast=LECarrierCont)
    
            RightEye = spiralStim(winR,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes = aRes,
                              units=units, radialCycles=0, visibleWedge=visWedge, contrast = contrast[1])

            Trigger = visual.RadialStim(winL,size=resY-SizeAdjust,angularCycles=aCycles, color=-1,angularRes=35,
                              units="pix", radialCycles=0, visibleWedge=(TvisWedge), 
                              ori=ori, contrast = 0.9)

        elif Condition == "RadialR":
            LeftEye = spiralStim(winL,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes=aRes, 
                                 units=units, radialCycles = 0, visibleWedge=visWedge, contrast = contrast[0])
        
            RightEye = visual.RadialStim(winR,size=resY-SizeAdjust,angularCycles=aCycles, color=c, angularRes = aRes,
                                  units=units, radialCycles= 0, visibleWedge=visWedge, contrast = RECarrierCont)
    
            Trigger = visual.RadialStim(winR,size=resY-SizeAdjust,angularCycles=aCycles, color=-1,angularRes=35,
                                  units="pix", radialCycles = 0, visibleWedge = (TvisWedge), 
                                  ori=ori, contrast = 0.9)
                                  
        elif Condition == "SpiralL":
            LeftEye = spiralStim(winL,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes=aRes, 
                                 units=units, radialCycles = 0, visibleWedge=visWedge, contrast = LECarrierCont, carrier=True)
        
            RightEye = spiralStim(winR,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes = aRes,
                                  units=units, radialCycles= 0, visibleWedge=visWedge, contrast = contrast[1])
    
            Trigger = spiralStim(winL,size=resY-SizeAdjust,angularCycles=20, color=-1,angularRes=35,
                                  units="pix", radialCycles = 0, visibleWedge = (TvisWedge), 
                                  ori=ori, contrast = 0.9, carrier=True)
                                  
        elif Condition == "SpiralR":
            LeftEye = spiralStim(winL,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes=aRes, 
                                 units=units, radialCycles = 0, visibleWedge=visWedge, contrast = contrast[0])
        
            RightEye = spiralStim(winR,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes = aRes,
                                  units=units, radialCycles= 0, visibleWedge=visWedge, contrast = RECarrierCont, carrier=True)
    
            Trigger = spiralStim(winR,size=resY-SizeAdjust,angularCycles=20, color=-1,angularRes=35,
                                  units="pix", radialCycles = 0, visibleWedge = (TvisWedge), 
                                  ori=ori, contrast = 0.9, carrier=True)
                                  
        elif Condition =="ConcentricL":
            LeftEye = visual.RadialStim(winL,size=resY-SizeAdjust,angularCycles=0, color=c, angularRes=aRes, 
                                 units=units, radialCycles = 8, visibleWedge=visWedge, contrast = LECarrierCont)
    
            RightEye = spiralStim(winR,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes = aRes,
                                  units=units, radialCycles= 0, visibleWedge=visWedge, contrast = RECarrierCont)
    
            Trigger = visual.RadialStim(winL,size=resY-SizeAdjust,angularCycles=0, color=-1,angularRes=35,
                                  units="pix", radialCycles = 8, visibleWedge = (TvisWedge), 
                                  ori=ori, contrast = 0.9)
                                  
        elif Condition =="ConcentricR":
            LeftEye = spiralStim(winL,size=resY-SizeAdjust,angularCycles=20, color=c, angularRes=aRes, 
                                 units=units, radialCycles = 0, visibleWedge=visWedge, contrast = contrast[0])
        
            RightEye = visual.RadialStim(winR,size=resY-SizeAdjust,angularCycles=0, color=c, angularRes = aRes,
                                  units=units, radialCycles= 8, visibleWedge=visWedge, contrast = RECarrierCont)
                 
            Trigger = visual.RadialStim(winR,size=resY-SizeAdjust,angularCycles=0, color=-1,angularRes=35,
                                  units="pix", radialCycles = 8, visibleWedge = (TvisWedge), 
                                  ori=ori, contrast = 0.9)
    
    maskL = visual.RadialStim(winL,color=[0,0,0],size=(resY-SizeAdjust)*0.76,
                              angularCycles=aCycles,angularRes=aRes,units=units)
    
    maskR = visual.RadialStim(winR,color=[0,0,0],size=(resY-SizeAdjust)*0.76,
                              angularCycles=aCycles,angularRes=aRes,units=units)
    
    return LeftEye, maskL, RightEye, maskR, Trigger

    """
    # creates radial patches and returns the radial stim, concentric stim 
    # and masks for L and R (using modern syntax and more recent stim locations.)
    # """
    # tmp comment to simplify then will copy over from above
    # psychopy.plugins.activatePlugins() # needed for modern version
    # from psychopy import RadialStim
    # RadL = visual.RadialStim(winL,size=resY-175,angularCycles=aCycles, color=c, angularRes=aRes, units=units, radialCycles = 0, contrast = contrast[0])
    # maskL = visual.RadialStim(winL,color=[0,0,0],size=(resY-175)*0.745,angularCycles=aCycles,angularRes=aRes,units=units)
    # ConcR = visual.RadialStim(winR,size=resY-175,angularCycles=0, color=c, angularRes = aRes,units=units, radialCycles= 8, ori=300, contrast = contrast[1]) 
    # maskR = visual.RadialStim(winR,color=[0,0,0],size=(resY-175)*0.76,angularCycles=aCycles,angularRes=aRes,units=units)
    # return RadL, maskL, ConcR, maskR

LeftEye, maskL, RightEye, maskR, Trigger = createRadialStim(winL, winR, resY, Condition = "ConcentricL")

# End location

EndLocL2 = visual.PatchStim(winL, tex='None', units='pix', pos=[-140,-320], size=(6,60), color=[-1,-1,-1], ori=200)
EndLocL1 = visual.PatchStim(winL, tex='None', units='pix', pos=[140,-320], size=(6,60), color=[-1,-1,-1], ori=340)
EndLocR2 = visual.PatchStim(winR, tex='None', units='pix', pos=[-140,-320], size=(6,60), color=[-1,-1,-1], ori=200)
EndLocR1 = visual.PatchStim(winR, tex='None', units='pix', pos=[140,-320], size=(6,60), color=[-1,-1,-1], ori=340)

#Create fixation and fusion lock
#Dot
fixationL = visual.PatchStim(winL, texRes=512, tex='None', mask="circle",units='pix',rgb=-1, pos=[0,0], size=(40.0,40.0))
fixationR = visual.PatchStim(winR, texRes=512, tex='None', mask="circle",units='pix',rgb=-1, pos=[0,0], size=(40.0,40.0))

dotL = visual.PatchStim(winL, texRes=512, tex='None', mask="circle",units='pix',rgb=1, pos=[0,0], size=(20.0,20.0))
dotR = visual.PatchStim(winR, texRes=512, tex='None', mask="circle",units='pix',rgb=1, pos=[0,0], size=(20.0,20.0))

#Spokes
# to the right window    
BarTop = visual.PatchStim(winR, tex='none', units='pix', rgb=1.0, pos=(0,85),ori=0, size=(12,90))
BarLeft = visual.PatchStim(winR, tex='none', units='pix', rgb=1.0, pos=(-85,0),ori=0, size=(90,12))

# to the left window    
BarBottom = visual.PatchStim(winL, tex='none', units='pix', rgb=-1.0, pos=(-0,-85),ori=0, size=(12,90))
BarRight = visual.PatchStim(winL, tex='none', units='pix', rgb=-1.0, pos=(85,0),ori=0, size=(90,12))

#Fusion lock
LockSize=512
array = zeros([LockSize,LockSize])
for n in range(0, LockSize+1, 32):
    array[n:16+n,0:16]=1
    array[n-16:16+n-16,0:16]=-1
    array[n:16+n,LockSize-16:LockSize]=-1
    array[n-16:16+n-16,LockSize-16:LockSize]=1
    
    array[0:16,n:16+n]=1
    array[0:16, n-16:16+n-16]=-1
    array[LockSize-16:LockSize,n:16+n]=-1
    array[LockSize-16:LockSize, n-16:16+n-16]=1

fusionL = visual.PatchStim(winL, tex=array, 
    size=(1050,1050), units='pix',
    interpolate=False,
    autoLog=True)
fusionR = visual.PatchStim(winR, tex=array, 
    size=(1050,1050), units='pix',
    interpolate=False,
    autoLog=True) 

Fixation = [fixationL, fixationR, dotR, dotL, BarBottom, BarTop, BarLeft, BarRight, EndLocL1, EndLocL2, EndLocR1, EndLocR2]

# Break stimuli

BreakStimL = visual.RadialStim(winL,size=resY-350,angularCycles=0, color=1,angularRes=35,units="pix", radialCycles = 0, contrast = 1)
BreakStimR = visual.RadialStim(winR,size=resY-350,angularCycles=0, color=1,angularRes=35,units="pix", radialCycles = 0, contrast = 1)

#--------------------------------------
#                 Messages
#--------------------------------------

# Inscructions = 

# Check stimuli is fusing
FixationMsgL = visual.TextStim(winL, 'Please ensure stimuli is fusing. \nPress the Right arrow when the wave reaches the desitination point\nPress the Left arrow if the wave is not triggered\nPress any button to begin', pos=(0,250),  
    flipHoriz=True, height=40, wrapWidth=1000)
FixationMsgR = visual.TextStim(winR, 'Please ensure stimuli is fusing. \nPress the Right arrow when the wave reaches the desitination point\nPress the Left arrow if the wave is not triggered\nPress any button to begin', pos=(0,250),  
    flipHoriz=True, height=40, wrapWidth=1000)

#PauseMsgL = visual.TextStim(winL, 'Break in experiment \nPress any button to continue',  flipHoriz=True, height=40, wrapWidth=1000)
#PauseMsgR = visual.TextStim(winR, 'Break in experiment \nPress any button to continue',  flipHoriz=True, height=40, wrapWidth=1000)

EndMsgL = visual.TextStim(winL, 'Experiment Over \nThanks for Participating!',  flipHoriz=True, height=40, wrapWidth=1000)
EndMsgR = visual.TextStim(winR, 'Experiment Over \nThanks for Participating!',  flipHoriz=True, height=40, wrapWidth=1000)

#--------------------------------------
#           Presentation Loop
#--------------------------------------

#Check fusion
fusionL.draw()
fusionR.draw()
for x in Fixation:
    x.draw()
FixationMsgL.draw()
FixationMsgR.draw()
winL.flip()
winR.flip()
event.waitKeys()

# Initialise lists that will store output data
Direction = []
ResponseTime = []
StimOrientation = []
IsOddBall = []
WaveSpeeds = []
Keys = []

BreakNum = 0
OddballRand = rand.randint(5, 7)
OddballTrack = 0

for y in Exp:
    # Create stimuli
    LeftEye, maskL, RightEye, maskR, Trigger = createRadialStim(winL, winR, resY, Condition=y)

    fusionL.draw()
    fusionR.draw()
    for x in Fixation:
        x.draw()
    winL.flip()
    winR.flip()
    time.sleep(2)

#    Flash suppression
    fusionL.draw()
    fusionR.draw()
    if y[-1] == "L":
        LeftEye.draw()
        maskL.draw()
    else:
        RightEye.draw()
        maskR.draw()
    for x in Fixation:
        x.draw()

    winL.flip()
    winR.flip()
    time.sleep(1)

#   Present stimuli
    fusionL.draw()
    fusionR.draw()
    LeftEye.draw()
    maskL.draw()
    RightEye.draw()
    maskR.draw()
    for x in Fixation:
        x.draw()
    
    winL.flip()
    winR.flip()
    time.sleep(0.5)

#   Present trigger
    fusionL.draw()
    fusionR.draw()
    LeftEye.draw()
    RightEye.draw()
    Trigger.draw()
    maskL.draw()
    maskR.draw()
    
    for x in Fixation:
        x.draw()

    Clock.reset() # Start timing
    
    winL.flip()
    winR.flip()
    time.sleep(0.25)

# Remove Trigger and wait for response
    fusionL.draw()
    fusionR.draw()
    LeftEye.draw()
    maskL.draw()
    RightEye.draw()
    maskR.draw()

    for x in Fixation:
        x.draw()
    winL.flip()
    winR.flip()

    Keys = event.waitKeys()

#    Keys = []
#    while Keys == [] and Clock.getTime() < 3:
#        Keys = event.getKeys()
#    print(Keys)
#    if Keys == []:
#        Keys.append("Left")

# Add data from trial
    RespTime = Clock.getTime()
    ResponseTime.append(RespTime)
    StimOrientation.append(y)
    Keys = Keys[0]
    Keys = Keys.strip("[']")
    Direction.append(Keys)
    IsOddBall.append("N")
    if Keys == "right":
        if y[0] == 'R':
            RadAvSpeed.append(RespTime)
        elif y[0] == 'S':
            SpirAvSpeed.append(RespTime)
        elif y[0] == 'C':
            ConcAvSpeed.append(RespTime)
    if y[0] == "R":
        WaveSpeeds.append(mean(RadAvSpeed))
    elif y[0] == "S":
        WaveSpeeds.append(mean(SpirAvSpeed))
    elif y[0] == "C":
        WaveSpeeds.append(mean(ConcAvSpeed))
        
#    Clear Screen
    for x in Fixation:
        x.draw()
    winL.flip()
    winR.flip()
    
    
    ######################################################################################
    
    
    OddballTrack += 1
#    OddBall
    if OddballTrack == OddballRand:
        OddBallCondNum = rand.randint(0, 5)
        OddBallCondition = ConditionList[OddBallCondNum]
        # Main stimuli
        LeftEye, maskL, RightEye, maskR, Trigger = createRadialStim(winL, winR, 
            resY, Condition=OddBallCondition)
            
        fusionL.draw()
        fusionR.draw()
        for x in Fixation:
            x.draw()
        winL.flip()
        winR.flip()
        time.sleep(2)
        
#    Flash suppression
        fusionL.draw()
        fusionR.draw()
        if OddBallCondition[-1] == "L":
            LeftEye.draw()
            maskL.draw()
        else:
            RightEye.draw()
            maskR.draw()
        for x in Fixation:
            x.draw()
    
        winL.flip()
        winR.flip()
        time.sleep(1)

#   Present stimuli, only rival stim shown
        fusionL.draw()
        fusionR.draw()
        if OddBallCondition[-1] == "R":
            LeftEye.draw()
            maskL.draw()
        else:
            RightEye.draw()
            maskR.draw()
            
        for x in Fixation:
            x.draw()
        
        winL.flip()
        winR.flip()
        time.sleep(0.5)

    #   Present trigger
        fusionL.draw()
        fusionR.draw()
        if OddBallCondition[-1] == "L":
            LeftEye.draw()
        else:
            RightEye.draw()
        Trigger.draw()
        maskL.draw()
        maskR.draw()
        for x in Fixation:
            x.draw()        
        winL.flip()
        winR.flip()
        Clock.reset() # Start timing
        time.sleep(0.25)

# Set wave speed based on average travel time in each condition
        if y[0] == 'R':
            WedgeSize = 180 * mean(RadAvSpeed)
        elif y[0] == 'S':
            WedgeSize = 180 * mean(SpirAvSpeed)
        elif y[0] == 'C':
            WedgeSize = 180 * mean(ConcAvSpeed)
        
        Keys = []
        while Keys == []:
            a = WedgeSize*Clock.getTime()
            b = 360 - WedgeSize*Clock.getTime()
            if OddBallCondition[-1] == "L":
            # Clockwise oddball
                Clockwise, maskL, Unneeded, maskR, Trigger = createRadialStim(winL, winR, 
                    resY, visWedge = (0,a), Condition=OddBallCondition)
            # Counter-clockwise oddball
                CounterClockwise, maskL, Unneeded, maskR, Trigger = createRadialStim(winL, winR, 
                    resY, visWedge = (b,360),Condition=OddBallCondition)
            else:
            # Clockwise oddball
                Unneeded, maskL, Clockwise, maskR, Trigger = createRadialStim(winL, winR, 
                    resY, visWedge = (0,a), Condition=OddBallCondition)
            # Counter-clockwise oddball
                Unneeded, maskL, CounterClockwise, maskR, Trigger = createRadialStim(winL, winR, 
                    resY, visWedge = (b,360),Condition=OddBallCondition)
            
            fusionL.draw()
            fusionR.draw()
            Clockwise.draw()
            CounterClockwise.draw()
            
            if OddBallCondition[-1] == "R":
                LeftEye.draw()
            else:
                RightEye.draw()
            maskL.draw()
            maskR.draw()
            for x in Fixation:
                x.draw()
            winR.flip()
            winL.flip()
            Keys = event.getKeys()
#############################################################

        # Add data from trial
        RespTime = Clock.getTime()
        ResponseTime.append(RespTime)
        StimOrientation.append(OddBallCondition)
        Keys = Keys[0]
        Keys = Keys.strip("[']")
        Direction.append(Keys)
        IsOddBall.append("Y")
        OddballTrack = 0
        OddballRand = rand.randint(5, 7)
        if OddBallCondition[0] == "R":
            WaveSpeeds.append(mean(RadAvSpeed))
        elif OddBallCondition[0] == "S":
            WaveSpeeds.append(mean(SpirAvSpeed))
        elif OddBallCondition[0] == "C":
            WaveSpeeds.append(mean(ConcAvSpeed))
    BreakNum +=1
    if BreakNum == -1: # Currently skipped
        fusionL.draw()
        fusionR.draw()
        BreakStimL.draw()
        BreakStimR.draw()
        maskL.draw()
        maskR.draw()
        for x in Fixation:
            x.draw()
        winL.flip()
        winR.flip()
        BreakNum = 0
        time.sleep(5)

#--------------------------------------
#              End/Cleanup
#--------------------------------------

#Display end msg
EndMsgL.draw()
EndMsgR.draw()
winL.flip()
winR.flip()
event.waitKeys()

#Output reaction times in csv

if params['Observer'] == 'z':
    pass
else:
    #Output responses in csv
    FileName = './data/TW_' + params['Observer'] +  '_' + Date + '.csv'
    #, newline=''     ./data/
    if simulationMode:
        with open(FileName, 'w', newline='') as csvfile:
            Writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            Writer.writerow(["ParticipantID", "StimOrientation", "Direction", "ResponseTime", "IsOddBall", "WaveSpeed"])
            for x in range(len(ResponseTime)):
                Writer.writerow([params['Observer'], StimOrientation[x], Direction[x], ResponseTime[x], IsOddBall[x], WaveSpeeds[x]])
        csvfile.close()
    
        with open(AveragesCSVName, 'w', newline='') as csvfile:
            Writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            Averages = [RadAvSpeed, SpirAvSpeed, ConcAvSpeed]
            Writer.writerow(RadAvSpeed)
            Writer.writerow(SpirAvSpeed)
            Writer.writerow(RadAvSpeed)
        csvfile.close()
    else:
        with open(FileName, 'wb+') as csvfile:
            Writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            Writer.writerow(["ParticipantID", "StimOrientation", "Direction", "ResponseTime", "IsOddBall", "WaveSpeed"])
            for x in range(len(ResponseTime)):
                Writer.writerow([params['Observer'], StimOrientation[x], Direction[x], ResponseTime[x], IsOddBall[x], WaveSpeeds[x]])
        csvfile.close()
    
        with open(AveragesCSVName, 'wb+') as csvfile:
            Writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            Averages = [RadAvSpeed, SpirAvSpeed, ConcAvSpeed]
            Writer.writerow(RadAvSpeed)
            Writer.writerow(SpirAvSpeed)
            Writer.writerow(RadAvSpeed)
        csvfile.close()
winL.close()
winR.close()