# -*- coding: utf-8 -*-
"""
PeriodicPerturbation.py

A test example of periodic pertubation paradigm

RH 27/02/25

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
print(visual.__file__)
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
Conts = [0.5,0.5]

# Get Date and start time
now = datetime.now()
Date = now.strftime('%d%m%y_%H%M')

# # present a dialogue box for changing params
# params = {'Observer':''}
# paramsDlg2 = gui.DlgFromDict(params, title='Travelling Waves Basic', fixed=['date'])
# Name = params['Observer']
# Name=Name.upper()


ConditionList = ['Left','Right'] 
 
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

def createRadialStim(winL, winR, resY, units="cm", contrast=(Conts), Condition="Left", SimMode = simulationMode):
    """
    creates radial patches and returns the radial stim, concentric stim, 
    spiral stim, and masks for L and R
    """
    if SimMode == True:
        if Condition == "Left": # for displaying on lab
           LeftEye = visual.GratingStim(winL,size=[15, 2.5], ori=90,
                                 sf=0.75, contrast=contrast[0], units=units)
           
           TriggerL = visual.GratingStim(winL,size=[1.5, 2.5], ori=90,
                                  sf=0.75, pos=[0,-7], contrast = 1, units=units)
        
           RightEye = visual.GratingStim(winR,size=[2.5, 15],
                                  sf=1, contrast = contrast[1], units=units)
    
           TriggerR = visual.GratingStim(winR,size=[2.5, 1.5], 
                                  sf=1, pos=[0,7], contrast = 1, units=units)
           
        elif Condition == "Right": # for displaying on lab
          # RightEye = visual.GratingStim(winR,size=[resY/1.2, resY/10], ori=90,
           #                      sf=2500, units=units, contrast=contrast[0])
           RightEye = visual.GratingStim(winR,size=[15, 2.5], ori=90,
                                 sf=0.75,  contrast = contrast[0], units=units)
           
           TriggerR = visual.GratingStim(winR,size=[1.5, 2.5], ori=90,
                                 sf=0.75,  pos=[0,-7], contrast = 1, units=units)
        
           LeftEye = visual.GratingStim(winL,size=[2.5, 15],
                                  sf=1, contrast = contrast[1], units=units)
         
           TriggerL = visual.GratingStim(winL,size=[2.5, 1.5], 
                                  sf=1, pos=[0,7], contrast = 1, units=units)
    else:
        if Condition == "Left": # for displaying on lab
           LeftEye = visual.PatchStim(winL,size=[15, 2.5], ori=90, tex='sin',
                                 sf=0.75, contrast=contrast[0], units=units)
           
           TriggerL = visual.PatchStim(winL,size=[1.5, 2.5], ori=90, tex='sin',
                                  sf=0.75, pos=[0,-7], contrast = 1, units=units)
        
           RightEye = visual.PatchStim(winR,size=[2.5, 15], tex='sin',
                                  sf=1, contrast = contrast[1], units=units)
    
           TriggerR = visual.PatchStim(winR,size=[2.5, 1.5], tex='sin',
                                  sf=1, pos=[0,7], contrast = 1, units=units)
           
        elif Condition == "Right": # for displaying on lab
          # RightEye = visual.GratingStim(winR,size=[resY/1.2, resY/10], ori=90,
           #                      sf=2500, units=units, contrast=contrast[0])
           RightEye = visual.PatchStim(winR,size=[15, 2.5], ori=90,tex='sin',
                                 sf=0.75,  contrast = contrast[0], units=units)
           
           TriggerR = visual.PatchStim(winR,size=[1.5, 2.5], ori=90,tex='sin',
                                 sf=0.75,  pos=[0,-7], contrast = 1, units=units)
        
           LeftEye = visual.PatchStim(winL,size=[2.5, 15],tex='sin',
                                  sf=1, contrast = contrast[1], units=units)
         
           TriggerL = visual.PatchStim(winL,size=[2.5, 1.5], tex='sin',
                                  sf=1, pos=[0,7], contrast = 1, units=units)
    
    return LeftEye, RightEye, TriggerL, TriggerR


LeftEye, RightEye, TriggerL, TriggerR = createRadialStim(winL, winR, resY, Condition = "Left")

# Dots
RDK= visual.DotStim(win=winL,units="cm",dotSize=3, dotLife=20, fieldPos=[0,0], fieldSize=[30,30],nDots=30, coherence=0.5, fieldShape="circle")


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
#BarTop = visual.PatchStim(winR, tex='none', units='pix', rgb=1.0, pos=(0,85),ori=0, size=(12,90))
BarLeft = visual.PatchStim(winR, tex='none', units='pix', rgb=1.0, pos=(-85,0),ori=0, size=(90,12))

# to the left window    
#BarBottom = visual.PatchStim(winL, tex='none', units='pix', rgb=-1.0, pos=(-0,-85),ori=0, size=(12,90))
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

Fixation = [fixationL, fixationR, dotR, dotL, BarLeft, BarRight, EndLocL1, EndLocL2, EndLocR1, EndLocR2]

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
y = "Left"

while Keys != "space":
    if Keys == "left":
        y = "Right"
    else:
        y = "Left"
    # Create stimuli
    LeftEye, RightEye, TriggerL, TriggerR = createRadialStim(winL, winR, resY, Condition=y)

    fusionL.draw()
    fusionR.draw()
    LeftEye.draw()
    RightEye.draw()
    for x in Fixation:
        x.draw()
    winL.flip()
    winR.flip()
    time.sleep(0.5)
    
    fusionL.draw()
    fusionR.draw()
    LeftEye.draw()
    RightEye.draw()
    for x in Fixation:
        x.draw()
    TriggerL.draw()
    winL.flip()
    winR.flip()
    time.sleep(0.5)
    
    fusionL.draw()
    fusionR.draw()
    LeftEye.draw()
    RightEye.draw()
    for x in Fixation:
        x.draw()
    winL.flip()
    winR.flip()
    time.sleep(1)
    
    fusionL.draw()
    fusionR.draw()
    LeftEye.draw()
    RightEye.draw()
    for x in Fixation:
        x.draw()
    TriggerR.draw()
    winL.flip()
    winR.flip()
    time.sleep(0.5)
    
    fusionL.draw()
    fusionR.draw()
    LeftEye.draw()
    RightEye.draw()
    for x in Fixation:
        x.draw()
    winL.flip()
    winR.flip()
    time.sleep(0.5)
    
    Keys = event.getKeys()
    if Keys == []:
        Keys = [""] 
    Keys=Keys[0]
    Keys = Keys.strip("[']")
    print(Keys)


#--------------------------------------
#              End/Cleanup
#--------------------------------------


winL.close()
winR.close()