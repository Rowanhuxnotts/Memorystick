#! /usr/bin/env python
"""
DominanceDuration.py

The most basic form of binocular rivalry experiment. Participants view rival
stimuli over a prolonged period of time and report which stimuli they see.
Vertical, horizontal or mixed.

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
from psychopy.hardware import keyboard
from psychopy.iohub import launchHubServer
from psychopy.core import getTime

#--------------------------------------
#              Initialisation
#--------------------------------------

simulationMode = True  # False

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

else:
    print("Running in experiment mode")
    resX=1680
    resY=1050
    theMonitor = 'testMonitor'
    pos = [[0,0],[0,0]] # DON'T offset 2 windows
    allowGUI = False
    viewScale = [1, 1]
    


# Start the ioHub process. 'io' can now be used during the
# experiment to access iohub devices and read iohub device events.
#io = launchHubServer()
#kb = io.devices.keyboard


kb = keyboard.Keyboard()
# Experiment params
NumTrials = 2
LEContrast=0.5
REContrast=0.5
Contrasts=[LEContrast,REContrast]
Units="deg"

# Get Date and start time
now = datetime.now()
Date = now.strftime('%d%m%y_%H%M')

# present a dialogue box for changing params
params = {'Observer':''}
paramsDlg2 = gui.DlgFromDict(params, title='Travelling Waves Basic', fixed=['date'])
Name = params['Observer']
Name=Name.upper()

ConditionList = ["Left", "Right"]
# This being the eye in which the radial is presented
 
Exp = data.TrialHandler(ConditionList,NumTrials, method='random', 
                        dataTypes=None, extraInfo=None,seed=None,
                        originPath=None)

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

#--------------------------------------
#            Create stimlui 
#--------------------------------------

# Create stimlui initial stimuli
# RadialStim has changed / been moved in newer versions of psychopy, 
# so deal with this separately !
def createRadialStim(winL, winR, resY, Contrast=(LEContrast, REContrast), Condition="Left", units=Units):
    """
    creates radial patches and returns the radial stim, concentric stim, 
    spiral stim, and masks for L and R
    """
    if simulationMode: # Change stim size in simulation vs lab
        SizeAdjust = 15
    else:
        SizeAdjust = 350
    if Condition == "Left": # for displaying on lab
       LeftEye = visual.GratingStim(winL,size=[5,5], pos=[0,0], sf=4,
                             units=units, contrast=Contrast[0], ori=90)
                             
       RightEye = visual.GratingStim(winR,size=[5,5], pos=[0,0], sf=4,
                              units=units, contrast = Contrast[1])

    if Condition == "Right": # for displaying on lab
       RightEye = visual.GratingStim(winR,size=[5,5], pos=[0,0], sf=4,
                             units=units, contrast=Contrast[0], ori=90)
    
       LeftEye = visual.GratingStim(winL,size=[5,5], pos=[0,0], sf=4,
                              units=units, contrast = Contrast[1])

    return LeftEye, RightEye

LeftEye, RightEye = createRadialStim(winL, winR, resY, Condition = "Left", Contrast=Contrasts, units=Units)

# End location

EndLocL2 = visual.PatchStim(winL, tex='None', units='pix', pos=[-140,-420], size=(7,60), color=[-1,-1,-1], ori=200)
EndLocL1 = visual.PatchStim(winL, tex='None', units='pix', pos=[0,-440], size=(7,60), color=[-1,-1,-1], ori=0)
EndLocR2 = visual.PatchStim(winR, tex='None', units='pix', pos=[-140,-420], size=(7,60), color=[-1,-1,-1], ori=200)
EndLocR1 = visual.PatchStim(winR, tex='None', units='pix', pos=[0,-440], size=(7,60), color=[-1,-1,-1], ori=0)

#Create fixation and fusion lock
#Dot
fixationL = visual.PatchStim(winL, texRes=512, tex='None', mask="circle",units='pix',rgb=-1, pos=[0,0], size=(20.0,20.0))
fixationR = visual.PatchStim(winR, texRes=512, tex='None', mask="circle",units='pix',rgb=-1, pos=[0,0], size=(20.0,20.0))

#Spokes
# to the right window    
BarTop = visual.PatchStim(winR, tex='none', units='pix', rgb=1.0, pos=(0,85),ori=0, size=(15,100))
BarLeft = visual.PatchStim(winR, tex='none', units='pix', rgb=1.0, pos=(-85,0),ori=0, size=(100,15))

# to the left window    
BarBottom = visual.PatchStim(winL, tex='none', units='pix', rgb=-1.0, pos=(-0,-85),ori=0, size=(15,100))
BarRight = visual.PatchStim(winL, tex='none', units='pix', rgb=-1.0, pos=(85,0),ori=0, size=(100,15))

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

Fixation = [fixationL, fixationR]

#--------------------------------------
#                 Messages
#--------------------------------------

# Inscructions = 

# Check stimuli is fusing
FixationMsgL = visual.TextStim(winL, 'Please ensure stimuli is fusing.', pos=(0,250),  
    flipHoriz=True, height=40, wrapWidth=1000)
FixationMsgR = visual.TextStim(winR, 'Please ensure stimuli is fusing.', pos=(0,250),  
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

TrialTimer = core.Clock()
PressedKeys = []
TimePressed = []
TrialTime = []
Cond = []
for y in Exp:
    LeftEye, RightEye = createRadialStim(winL, winR, resY, Condition=y)
    TrialTimer.reset()
    fusionL.draw()
    fusionR.draw()
    LeftEye.draw()
    RightEye.draw()
    for x in Fixation:
        x.draw()
        
    winL.flip()
    winR.flip()
    while TrialTimer.getTime() <= 3:
        #fusionL.autoDraw()
        #fusionR.autoDraw()
       # for x in Fixation:
       #     x.autoDraw()
      #  for e in kb.getEvents():
      #      print(e)
        Keys=[]
        Keys = kb.getKeys()
        if Keys:
            for k in Keys:
                PressedKeys.append(k.name)
                TimePressed.append(k.tDown)
                TrialTime.append(TrialTimer.getTime())
                Cond.append(y)
                
    print(PressedKeys)
    print(TimePressed)
    print(TrialTime)
    
    
    fusionL.draw()
    fusionR.draw()
    for x in Fixation:
        x.draw()
    winL.flip()
    winR.flip()
    time.sleep(1)


#--------------------------------------
#              End/Cleanup
#--------------------------------------
# Stop the ioHub Server
#io.quit()
#Display end msg
#EndMsgL.draw()
#EndMsgR.draw()
#winL.flip()
#winR.flip()
#event.waitKeys()

winL.close()
winR.close()