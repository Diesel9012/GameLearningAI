from scipy import *
import sys, time
from screenReader import ScreenReader 
import Output as opt
from pybrain.rl.environments.environment import Environment
from PIL import Image
from numpy import int64
#keycodes
a= ["LEFT","UP","DOWN","RIGHT"]
sc = ScreenReader()
class TEnviroment(Environment):
    def __init__(self, area):
        self.indim = 4
        self.outdim = 50*50

        self.reset()
        self.area = area
        self.state = None
        self.sequence = None
        self.target = None
        self.size = 10


        
    #sees if state has been updated, and returns it
    def getSensors(self):
        time.sleep(.75)
        self.update()
        return self.state
    #Sets an action
    def performAction(self, ac):
        self.updated = False
        self.action = ac
        opt.getKeyforOutput(a[int64(ac[0]).item()])
        time.sleep(.05)
        opt.getKeyforRelease(a[int64(ac[0]).item()])

    #An update method that gets called every number of frames that updates the state
    def update(self):
        im = sc.grabArea(self.area).resize((50,50))
        self.state = sc.GetIntensityImage(im)
        
    #resets the varriables
    def reset(self):
        self.state = None
        self.updated = True
        self.sequence = []