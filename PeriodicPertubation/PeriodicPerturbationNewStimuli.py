# -*- coding: utf-8 -*-
"""
PeriodicPerturbation.py

A test example of periodic pertubation paradigm

RH 27/02/25

"""

# Import modules
import psychopy
from psychopy import *
from numpy import *
#rom scipy import *
import time
from datetime import datetime
import csv

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
    
print(visual.__file__)

#--------------------------------------
#              Initialisation
#--------------------------------------

simulationMode = True

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
    fullscrMode = True
    
# Experiment params
NumTrials = 1
Conts = [0.6, 0.6] # Contrasts of base stimuli for left and right respectively
PresentationRepeats = 1 # Number of both triggers in a trial
ConditionList = ['HoriL', 'HoriR', 'VertL', 'VertR', 'SlantL', 'SlantR'] 

# Get Date and start time
now = datetime.now()
Date = now.strftime('%d%m%y_%H%M')

# Present a dialogue box that asks for the observers initials
params = {'Observer' : ''}
paramsDlg2 = gui.DlgFromDict(params, title='Travelling Waves Basic', 
                             fixed=['date'])
Name = params['Observer']
Name=Name.upper()

# %% Functions

# Could do with outputting the global time too
def TrialSection(SectionLength, SectionTimer, TrialClock, GlobalClock, ID, PressedKeys, 
                 TrialTime, GlobalTList, Cond):
    """
    Can be placed after a stimuli presentation to act as a constant check
    for button presses for a select period of time (SectionLength).
    """
    print(GlobalClock)
    SectionTimer.reset()
    while SectionTimer.getTime() <= SectionLength:
        Keys = event.getKeys(timeStamped=TrialClock)
        
        if Keys:
            Results = Keys[0]
            k = Results[0].strip("[']")
            ID.append(params['Observer'])
            PressedKeys.append(k)
            TrialTime.append(TrialClock.getTime())
            Global = GlobalClock.getTime()
            GlobalTList.append(Global)
            Cond.append(y)

    return ID, PressedKeys, TrialTime, GlobalTList, Cond

def RescaleOnZero(InArray):
    """
    Takes a numpy array of 265 luminance values and converts them to -1 to 1.
    
    InArray = Numpy array of ints from 0-265
    """
    InArray = InArray / 128
    InArray = InArray - 1
    return InArray

def createGratingStim(
        winL, winR, resY, Units="deg", 
        Contrast=(Conts), Condition="HoriL", 
        SimMode = simulationMode, Textures = None):
    """
    Creates grating stimuli
    """
    # Get texture orientation name
    if Condition.startswith("H"):
        TextName = "Hori"
    elif Condition.startswith("V"):
        TextName = "Vert"
    elif Condition.startswith("S"):
        TextName = "SlantMinus45"
        
    # Create textures in each eye
    if Condition.endswith("L"):
        # Test patch
        LeftEye = visual.GratingStim(winL, tex=Textures[TextName], mask=None, 
                                    units=Units, size=(1.6,10), 
                                    contrast=Contrast[0], sf=0.75)
        TriggerL = visual.GratingStim(winL, tex=Textures[TextName], mask=None, 
                                    units=Units, size=(1.6,1), sf=0.75,
                                    contrast=1, pos=[0,4.5])
        # Control patch
        RightEye = visual.GratingStim(winR, tex=Textures["Slant45"], mask=None, 
                                    units=Units, size=(1.6,10), 
                                    contrast=Contrast[1], sf=0.75)
        TriggerR = visual.GratingStim(winR, tex=Textures["Slant45"], mask=None, 
                                    units=Units, size=(1.6,1), sf=0.75,
                                    contrast=1, pos=[0,-4.5])
    else:
        # Test Patch
        RightEye = visual.GratingStim(winR, tex=Textures["Hori"], mask=None, 
                                    units=Units, size=(1.6,10), 
                                    contrast=Contrast[1], sf=0.75)
        TriggerR = visual.GratingStim(winR, tex=Textures[TextName], mask=None, 
                                    units=Units, size=(1.6,1), sf=0.75,
                                    contrast=1, pos=[0,-4.5])
        # Control patch
        LeftEye = visual.GratingStim(winL, tex=Textures["Slant45"], mask=None, 
                                    units=Units, size=(1.6,10), 
                                    contrast=Contrast[0], sf=0.75)
        TriggerL = visual.GratingStim(winL, tex=Textures["Slant45"], mask=None, 
                                    units=Units, size=(1.6,1), sf=0.75,
                                    contrast=1, pos=[0,4.5])
        
    return LeftEye, RightEye, TriggerL, TriggerR

# %% Create Stimuli

# Setup trial handeler and window maybe move
Exp = data.TrialHandler(ConditionList,NumTrials, method='random', 
                        dataTypes=None, extraInfo=None, seed=None,
                        originPath=None)

# Setup window (this works on old as well as new versions)
winL = visual.Window(size=(resX,resY), 
                     monitor=theMonitor, units='pix', 
                     bitsMode=None, fullscr=fullscrMode, 
                     allowGUI=allowGUI, color=0.0,screen=0, pos = pos[0], 
                     viewScale=viewScale)
winR = visual.Window(size=(resX,resY), 
                     monitor=theMonitor, units='pix', 
                     bitsMode=None, fullscr=fullscrMode, 
                     allowGUI=allowGUI, color=0.0,screen=1, pos = pos[1], 
                     viewScale=viewScale)

#winL.setGamma([2.05741,2.05741,2.05741])
#winR.setGamma([1.83718,1.83718,1.83718])

# Create textures
N = 256
x = linspace(-pi,pi, N)
Sine1D = 128.0 + (127.0 * sin(x * 2.0))
Sine1D = uint8(Sine1D)
Vertical = tile(Sine1D, (N,1))

Horizontal = copy(Vertical)
Slant45 = copy(Vertical)
SlantMinus45 = copy(Vertical)


# Transforms
for i in range(N):
    Slant45[i]= roll(Sine1D,-i) 
for i in range(N):
    SlantMinus45[i]= roll(Sine1D,i) 
Horizontal = Horizontal.transpose() 

# Normalise
Vertical = RescaleOnZero(Vertical)
Horizontal = RescaleOnZero(Horizontal)
Slant45 = RescaleOnZero(Slant45)
SlantMinus45 = RescaleOnZero(SlantMinus45)

#Maybe rename left and rights to slant45 and slantminus45
TexturesIn = {"Vert" : Vertical, "Hori" : Horizontal,
            "Slant45": Slant45, "SlantMinus45" : SlantMinus45}


# Initialise grating stims
LeftEye, RightEye, TriggerL, TriggerR = createGratingStim(winL, winR, resY, 
                                                         Condition = "HoriL",
                                                         Textures=TexturesIn)

# End location
EndLocL2 = visual.PatchStim(winL, tex='None', units='pix', pos=[-140,-320], 
                            size=(6,60), color=[-1,-1,-1], ori=200)
EndLocL1 = visual.PatchStim(winL, tex='None', units='pix', pos=[140,-320], 
                            size=(6,60), color=[-1,-1,-1], ori=340)
EndLocR2 = visual.PatchStim(winR, tex='None', units='pix', pos=[-140,-320], 
                            size=(6,60), color=[-1,-1,-1], ori=200)
EndLocR1 = visual.PatchStim(winR, tex='None', units='pix', pos=[140,-320], 
                            size=(6,60), color=[-1,-1,-1], ori=340)

#Create fixation and fusion lock
#Dot right
fixationL = visual.PatchStim(winL, texRes=512, tex='None', mask="circle",
                             units='pix', rgb=-1, pos=[-65,0], 
                             size=(40.0,40.0))
fixationR = visual.PatchStim(winR, texRes=512, tex='None', mask="circle",
                             units='pix', rgb=-1, pos=[-65,0], 
                             size=(40.0,40.0))

dotL = visual.PatchStim(winL, texRes=512, tex='None', mask="circle",
                        units='pix',rgb=1, pos=[-65,0], size=(20.0,20.0))
dotR = visual.PatchStim(winR, texRes=512, tex='None', mask="circle",
                        units='pix',rgb=1, pos=[-65,0], size=(20.0,20.0))

#Create fixation and fusion lock
#Dot left
fixationL2 = visual.PatchStim(winL, texRes=512, tex='None', mask="circle",
                              units='pix', rgb=-1, pos=[65,0], 
                              size=(40.0,40.0))
fixationR2 = visual.PatchStim(winR, texRes=512, tex='None', mask="circle",
                              units='pix', rgb=-1, pos=[65,0], 
                              size=(40.0,40.0))

dotL2 = visual.PatchStim(winL, texRes=512, tex='None', mask="circle",
                         units='pix',rgb=1, pos=[65,0], size=(20.0,20.0))
dotR2 = visual.PatchStim(winR, texRes=512, tex='None', mask="circle",
                         units='pix',rgb=1, pos=[65,0], size=(20.0,20.0))

#Spokes
# to the right window    
BarTopL = visual.PatchStim(winL, tex='none', units='cm', rgb=-1.0, 
                           pos=(-2.3,1),ori=0, size=(2,0.2))
BarTopR = visual.PatchStim(winR, tex='none', units='cm', rgb=-1.0, 
                           pos=(-2.3,1),ori=0, size=(2,0.2))
BarTopL2 = visual.PatchStim(winL, tex='none', units='cm', rgb=-1.0, 
                            pos=(2.3,1),ori=0, size=(2,0.2))
BarTopR2 = visual.PatchStim(winR, tex='none', units='cm', rgb=-1.0, 
                            pos=(2.3,1),ori=0, size=(2,0.2))
BarLeft = visual.PatchStim(winR, tex='none', units='pix', rgb=1.0,  # why is the units different?
                           pos=(-90,0),ori=0, size=(90,12))

# to the left window    
BarBottomL = visual.PatchStim(winL, tex='none', units='cm', rgb=-1.0, 
                              pos=(-2.3, -1), ori=0, size=(2,0.2))
BarBottomR = visual.PatchStim(winR, tex='none', units='cm', rgb=-1.0, 
                              pos=(-2.3, -1), ori=0, size=(2,0.2))
BarBottomL2 = visual.PatchStim(winL, tex='none', units='cm', rgb=-1.0, 
                               pos=(2.3, -1), ori=0, size=(2,0.2))
BarBottomR2 = visual.PatchStim(winR, tex='none', units='cm', rgb=-1.0, 
                               pos=(2.3, -1),ori=0, size=(2,0.2))
BarRight = visual.PatchStim(winL, tex='none',  units='pix', rgb=-1.0, 
                            pos=(90,0), ori=0, size=(90,12))

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

# Blocks
# Named = BlockLeftMonitorLeft/Right/Top/Bottom (side of screen)
units = 'cm'
BlockLML = visual.PatchStim(winL, tex='none', size = [10,15], pos=[-6.125,0], 
                            color=[0,0,0], units=units)
BlockLMR = visual.PatchStim(winL, tex='none', size = [10,15], pos=[6.125,0], 
                            color=[0,0,0], units=units)
BlockLMT = visual.PatchStim(winL, tex='none', size = [10,5], pos=[0,10], 
                            color=[0,0,0], units=units)
BlockLMB = visual.PatchStim(winL, tex='none', size = [10,5], pos=[0,-10], 
                            color=[0,0,0], units=units)

BlockRML = visual.PatchStim(winR, tex='none', size = [10,15], pos=[-6.125,0], 
                            color=[0,0,0], units=units)
BlockRMR = visual.PatchStim(winR, tex='none', size = [10,15], pos=[6.125,0], 
                            color=[0,0,0], units=units)
BlockRMT = visual.PatchStim(winR, tex='none', size = [10,5], pos=[0,10], 
                            color=[0,0,0], units=units)
BlockRMB = visual.PatchStim(winR, tex='none', size = [10,5], pos=[0,-10], 
                            color=[0,0,0], units=units)


Blocks = [BlockLML,BlockLMR,BlockLMT,BlockLMB,
          BlockRML,BlockRMR,BlockRMT,BlockRMB]

Fixation = [BarLeft, BarRight, BarTopL, BarTopR, BarBottomL, BarBottomR, 
            BarTopL2, BarTopR2, BarBottomL2, BarBottomR2, fixationL, fixationR, 
            dotL, dotR, fixationL2, fixationR2, dotL2, dotR2]

#--------------------------------------
#                 Messages
#--------------------------------------

# Inscructions = 

# Check stimuli is fusing
FixationMsgL = visual.TextStim(winL, 'Please ensure stimuli is fusing. \nPress the Right arrow when the wave reaches the desitination point\nPress the Left arrow if the wave is not triggered\nPress any button to begin', pos=(0,250),  
    flipHoriz=True, height=40, wrapWidth=1000)
FixationMsgR = visual.TextStim(winR, 'Please ensure stimuli is fusing. \nPress the Right arrow when the wave reaches the desitination point\nPress the Left arrow if the wave is not triggered\nPress any button to begin', pos=(0,250),  
    flipHoriz=True, height=40, wrapWidth=1000)

EndMsgL = visual.TextStim(winL, 'Experiment Over \nThanks for Participating!',  flipHoriz=True, height=40, wrapWidth=1000)
EndMsgR = visual.TextStim(winR, 'Experiment Over \nThanks for Participating!',  flipHoriz=True, height=40, wrapWidth=1000)

#--------------------------------------
#           Presentation Loop
#--------------------------------------

# Initialise lists that will store output data
Keys = []
ID=[]
PressedKeys = []
TrialTime = []
GlobalTList = []
Cond = []

# TrialClock for trials starting on 0
# SessionClock for global time
TrialClock = core.Clock()
SectionTimer = core.Clock()
GlobalClock = core.Clock()

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

for y in Exp: # Main presentation loop
    LeftEye, RightEye, TriggerL, TriggerR = createGratingStim(winL, winR, resY, 
                                                              Condition=y, 
                                                              Textures=TexturesIn)
    TrialClock.reset()
    # One trigger length pause at the start of each loop
    fusionL.draw()
    fusionR.draw()
    LeftEye.draw()
    RightEye.draw()
    for x in Blocks:
        x.draw()
    for x in Fixation:
        x.draw()
    winL.flip()
    winR.flip()
    ID, PressedKeys, TrialTime, GlobalTList, Cond = TrialSection(1.5, SectionTimer, TrialClock, GlobalClock, ID, PressedKeys, TrialTime, GlobalTList, Cond)

    for x in range(PresentationRepeats):
        fusionL.draw()
        fusionR.draw()
        LeftEye.draw()
        RightEye.draw()
        for x in Blocks:
            x.draw()
        for x in Fixation:
            x.draw()
        winL.flip()
        winR.flip()
        print(GlobalClock)
        ID, PressedKeys, TrialTime, GlobalTList, Cond = TrialSection(0.5, SectionTimer, TrialClock, GlobalClock, ID, PressedKeys, TrialTime, GlobalTList, Cond)
        
        fusionL.draw()
        fusionR.draw()
        LeftEye.draw()
        RightEye.draw()
        TriggerL.draw()
        for x in Blocks:
            x.draw()
        for x in Fixation:
            x.draw()
        winL.flip()
        winR.flip()
        ID, PressedKeys, TrialTime, GlobalTList, Cond = TrialSection(0.5, SectionTimer, TrialClock, GlobalClock, ID, PressedKeys, TrialTime, GlobalTList, Cond)
        fusionL.draw()
        fusionR.draw()
        LeftEye.draw()
        RightEye.draw()
        for x in Blocks:
            x.draw()
        for x in Fixation:
            x.draw()
        winL.flip()
        winR.flip()
        ID, PressedKeys, TrialTime, GlobalTList, Cond = TrialSection(1, SectionTimer, TrialClock, GlobalClock, ID, PressedKeys, TrialTime, GlobalTList, Cond)
        
        fusionL.draw()
        fusionR.draw()
        LeftEye.draw()
        RightEye.draw()
        TriggerR.draw()
        for x in Blocks:
            x.draw()
        for x in Fixation:
            x.draw()
        winL.flip()
        winR.flip()
        ID, PressedKeys, TrialTime, GlobalTList, Cond = TrialSection(0.5, SectionTimer, TrialClock, GlobalClock, ID, PressedKeys, TrialTime, GlobalTList, Cond)
        
        fusionL.draw()
        fusionR.draw()
        LeftEye.draw()
        RightEye.draw()
        for x in Blocks:
            x.draw()
        for x in Fixation:
            x.draw()
        winL.flip()
        winR.flip()
        ID, PressedKeys, TrialTime, GlobalTList, Cond = TrialSection(0.5, SectionTimer, TrialClock, GlobalClock, ID, PressedKeys, TrialTime, GlobalTList, Cond)
    
    fusionL.draw()
    fusionR.draw()
    for x in Fixation:
        x.draw()
    winL.flip()
    winR.flip()
    time.sleep(0.1)
    
#--------------------------------------
#              End/Cleanup
#--------------------------------------
if params['Observer'] != 'z':
    FileName = './data/PP_' + params['Observer'] +  '_' + Date + '.csv'
    with open(FileName, 'w+') as csvfile:
        Writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        Writer.writerow(["ParticipantID", "Condition", "PressedKey", "TrialTime", "GlobalTime"])
        for x in range(len(PressedKeys)):
            Writer.writerow([params['Observer'], Cond[x], PressedKeys[x], TrialTime[x], GlobalTList[x]])
    csvfile.close()

winL.close()
winR.close()