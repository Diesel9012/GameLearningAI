import pygubu
import tkinter as tk
from screenReader import ScreenReader
from QAlgorithm import QAlgorithm

builder  = pygubu.Builder()#loads Ui Builder
#
builder.add_from_file("FinalGUI.ui")#loads main menu from file
window = tk.Tk()#creates window object
window.mainwindow = builder.get_object("MainWindow")#copies the main frame for ui in file
#this section creates instances of attibuites in Main windows
StartButton = builder.get_object("Start")
Pause = builder.get_object("Pause")
End = builder.get_object("End")
Reward = builder.get_object("Reward")#passed to q-learning class to update current reward desplayed in menu
#DELETE LATER ALONG WITH PART IN GUI
ViewCurrent = builder.get_object("Current")
NewBBox = builder.get_object("Bounds")
EndGame = builder.get_object("EndGame")
Score = builder.get_object("Score")


sr = ScreenReader()#instanciates screen reader
#important game areas
scoreArea = None
GameArea = None
endGame = None
gameImage = None

bot = None #instanciates game playing bot 
#starts the bot playing the game
def StartBot(e):
	bot = QAlgorithm(Reward,GameArea,gameImage,endGame,scoreArea)#instanciates game playing bot 
	bot.state = 0
	bot.CheckState()
#saves a new area for main game play
def NewBox(e):
	global GameArea
	#load sup window or area selection
	#save array of bound boxs of interest
	if not (GameArea == None):
		x = GameArea[0]
		y = GameArea[1]
		h = abs(GameArea[0] -GameArea[2])
		w = abs(GameArea[1] -GameArea[3])
		GameArea = sr.selectArea('%dx%d+%d+%d' % (w, h, x, y))
	else:
		GameArea = sr.selectArea() 
def ScoreArea(e):
	global scoreArea
	#load sup window or area selection
	#save array of bound boxs of interest
	if not (scoreArea == None):
		x = scoreArea[0]
		y = scoreArea[1]
		h = abs(scoreArea[0] -scoreArea[2])
		w = abs(scoreArea[1] -scoreArea[3])
		scoreArea = sr.selectArea('%dx%d+%d+%d' % (w, h, x, y))
	else:
		scoreArea = sr.selectArea()
#pauses bot execution 
def PauseBot(e):
	bot.state = 1
#ends bot	
def EndBot(e):
	bot.state = 2

#DELETE LATER ALONG WITH PART IN GUI
def ViewBox(e):
	if(GameArea == None):
		NewBox()
	x = GameArea[0]
	y = GameArea[1]
	h = abs(GameArea[0] -GameArea[2])
	w = abs(GameArea[1] -GameArea[3])
	sr.veiwArea('%dx%d+%d+%d' % (w, h, x, y))


#This captures the game over screen
def CaptureEnd(e):
	global gameImage
	#Thiscapures the end screen
	global endGame
	if not (endGame == None):
		x = endGame[0]
		y = endGame[1]
		h = abs(endGame[0] -endGame[2])
		w = abs(endGame[1] -endGame[3])
		endGame = sr.selectArea('%dx%d+%d+%d' % (w, h, x, y))
	else:
		endGame = sr.selectArea()
	gameImage = sr.grabArea(endGame)

	

#needs work not implmented right
#window.resizeable(0,0)#disables window resizing

#adds handlers to main attributes in main window
StartButton.bind("<ButtonPress-1>",StartBot)
#DELETE LATER ALONG WITH PART IN GUI
ViewCurrent.bind("<ButtonPress-1>",ViewBox)
NewBBox.bind("<ButtonPress-1>",NewBox)
Pause.bind("<ButtonPress-1>",PauseBot)
End.bind("<ButtonPress-1>",EndBot)
EndGame.bind("<ButtonPress-1>",CaptureEnd)
Score.bind("<ButtonPress-1>",ScoreArea)
#starts bot's main menu
window.mainloop()