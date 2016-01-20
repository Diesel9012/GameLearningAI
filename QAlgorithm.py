from PIL.ImageGrab import grab
import imagehash
import time
import pickle
import numpy as np
import random
import Output
from screenReader import ScreenReader
from TEnviroment import TEnviroment 
from TTask import TTask
from pybrain.rl.learners.valuebased import ActionValueNetwork
from pybrain.rl.learners import Q
from pybrain.rl.agents import LearningAgent
from pybrain.rl.experiments.episodic import EpisodicExperiment
import multiprocessing
import sys
import pickle
import os.path

class QAlgorithm:
  def Pause(self):#if menu says pause pause exicution 
    while self.state == 1:
      time.sleep(.05)
    return True

  def Quit(self):#if menu says quit stop running
    self.process.terminate()
    return False

  def Start(self):#starts the Bot
    if self.process == None:
      self.runBot()
      #self.process = multiprocessing.Process(target=self.runBot, args= [])
      #self.process.start() 
    return True

  def CheckState(self):#checks to see what state the menu says to be in 
    if self.state == 0 :
      self.Start()
    elif self.state == 1:
      self.Pause()
    elif self.state == 2:
      self.Quit()

  def GameOver(self):#checks to see if state requires bot pause, quit or if the game is over
    return self.CheckState() or self.sr.checkEndGame(self.endBox,self.gameOver)

  def __init__(self,rewardBox,box,gameOver,endGame,scoreArea):
    self.reward = rewardBox
    self.bbox = box
    self.environment = TEnviroment(box)#Custom environment class
    if os.path.isfile("bot.txt"):
      self.controller  = pickle.load(open("bot.txt","rb")) 
    else:
      self.controller = ActionValueNetwork(50**2,4)#Arguments (framerate*maxPlaytime, Number of acitons)
    self.learner = Q()
    gf = {0:self.GameOver}
    self.agent = LearningAgent(self.controller, self.learner)
    self.task = TTask(self.environment,scoreArea,gf)#needs custom task
    self.experiment = EpisodicExperiment(self.task, self.agent)
    self.process = None
    self.endBox = endGame

  def runBot(self):#runes the bot for a single Episode
      self.experiment.doEpisodes()
      self.agent.learn()
      self.agent.reset()
      file = open("bot.txt","wb+")
      pickle.dump(self.controller,file)