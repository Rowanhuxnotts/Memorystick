from psychopy import *
import numpy as np
resX=1680
resY=1050
win = visual.Window(size=(resX,resY), monitor='testMonitor', units='pix', bitsMode=None, fullscr=True, allowGUI=False, color=0.0,screen=0)
myMask = np.array([
        [ 1, 0,-1, 0],
        [ 0,-1, 0, 1],
        [-1, 0, 1, 0],
        [ 0, 1, 0,-1]
        ])
myTex = np.random.random( (8,8,4) )
print(myTex)
myStim = visual.GratingStim(win, tex=None, mask=None, size=256)
myStim.draw()

win.flip()
event.waitKeys()
