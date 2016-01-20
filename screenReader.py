from PIL.ImageGrab import grab
import imagehash
import time
import pickle
from PIL import Image,ImageOps
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

class ScreenReader:
    def Segment (self, img):#seperates the digits out of raw score

        im = img.resize((52,64))#resizes image so it the happens properly
        im = ImageOps.grayscale(im)
        colThresh = 255*.817*im.size[1]#calculates threshold of white space in collums (white intesnity)*81.7%*numcollums
        rowThresh = 255*.66*im.size[0]#calculates threshold of white space in rows (white intesnity)*66%*numrows

        width = im.size[0]#gets number of collums
        height = im.size[1]#gets number or rows

        colSum = [ 0 for x in range(width)]#creates an array to hold sum of collum intesnisty
        rowSum = [0 for y in range(height)]#creates an array to hold sum of row intesnisty
        for x in range(width):#sums along collums and rows 
            for y in range(height):
                colSum[x] += im.getpixel((x,y))
                rowSum[y] += im.getpixel((x,y))
        cols = []#holds a list of cordinants for start and end of didgit collums
        rows = []#holds a list of cordinants for start and end of didgit rows
        testprev, testcurrent = False,False#finds the start and end of digits collums
        for x in range(len(colSum)):
            if(colSum[x]<colThresh):
                testprev = testcurrent
                testcurrent = True
            else:
                testprev = testcurrent
                testcurrent = False
            if(testprev == False and testcurrent == True):#from higher than threshold to below start of digit
                cols.append(x)
            if(testprev == True and testcurrent == False):#from lower than threshold to higher end of digit
                cols.append(x)

        testprev, testcurrent = False,False
        for x in range(len(rowSum)):#finds the start and end of digits rows
            if(rowSum[x]<rowThresh):
                testprev = testcurrent
                testcurrent = True
            else:
                testprev = testcurrent
                testcurrent = False
            if(testprev == False and testcurrent == True):#from higher than threshold to below start of digit
                rows.append(x)
            if(testprev == True and testcurrent == False):#from lower than threshold to higher end of digit
                rows.append(x)
        crop =[]#holds cropped images
        deltax = width*0.023529411764705882 #slight padding to get whole digit collums
        deltay = height*0.037037037037037035 #slight padding to get whole digit rows
        rowMin = min(rows)
        rowMax = max(rows)
        while(len(cols)%2 != 0):
            cols = cols[:len(cols)-2]
        for x in range(0,len(cols),2):
            crop.append(img.crop((cols[x]-int(deltax),rowMin-int(deltay),cols[x+1]+int(deltax),rowMax+int(deltay))))
        return crop

    def GetScore(self,img):#reads score from screen
            try:
                digits = self.Segment(img)
            except:
                print ("Redo the Score Bounds")

            score = []
            for x in digits:
                temp = x.resize((32,32))
                im = ([int('0',16) for z in range(32*32)])
                for y in range (32):
                    for x in range(32):
                        im[x*32+y] = (self.RGBToInt(img.getpixel((x,y))))
                temp = self.net.activate(im)
                l = temp.argmax()
                if l == 9:
                    l = 0 
                else:
                    l = l+1
                score.append(l)
            return score

    def checkEndGame(self,x,img):#Checks to see if a saved area has changed
    	return imagehash.average_hash(img) == imagehash.average_hash(self.grabArea(x))

    def readNumber(self,img):#Reads an area to find out what number is in that area
        img = img.resize((32,32))
        im = ([int('0',16) for z in range(32*32)])
        for y in range(32):
            for x in range(32):
                im[x*32+y] = (RGBToInt(img.getpixel((x,y))))
        temp = number.activate(img)
        index = temp.index(max)
        if temp == 10:
            return 0
        else :
            return temp

    def GetIntensityImage(self,image):#returns an array describing the rgb intesnsites of an image
        intensityMap = [None for y in range(image.width*image.height)]
        for x in range(image.width):
            for y in range(image.height):
                intensityMap[image.width-1*image.height-1+x] = self.RGBToInt(image.getpixel((x,y)))
        return intensityMap

    def RGBToInt(self,p):# turns a list of RGB values into a single number
        return int('%02x%02x%02x' % (p[0], p[1], p[2]), 16)
    
    def grabArea(self,bbox):# turns a defined area into (x0-x1,y0-y1) into an image
        return grab(bbox)
    
    def SaveAreaCoordinates(self,e):#used to get the Coordinates of an area of intrest 
        temp = self.root.winfo_geometry()
        p1 = temp.find("x")
        p2 = temp.find("+",p1+1)
        p3 = temp.find("+",p2+1)
        x0 = int(temp[p2+1:p3])
        y0 = int(temp[p3+1:])
        x1 = int(temp[0:p1]) +x0 
        y1 = int(temp[p1+1:p2]) +y0 + 5
        self.selectedArea = [x0,y0,x1,y1]
        print()
        self.root.destroy()
        self.quit = True
        return self.selectedArea

    def veiwArea(self, area):
        root = Tk()
        root.geometry(area)
        root.mainloop()

    def selectArea(self, prevar = None):#makes a window to be used to select an area of interst 
        self.root = Tk()
        self.quit = False
        self.root.geometry(prevar)
        self.root.bind('<Return>',self.SaveAreaCoordinates)
        self.root.wm_attributes("-topmost", 1)
        while not self.quit:
            self.root.update_idletasks()
            self.root.update()        
        return self.selectedArea
    
    def TestSelectArea(self):#test select area function
        print(self.selectArea())

    def TestRGBToInt(self):#tests rgb to int conversion 
        print("Enter r")
        r = int(input())
        print("Enter g")
        g = int(input())
        print("Enter b")
        b = int(input())
        print(self.RGBToInt((r,g,b)))
        
    def TestGrabScreen(self): #test screen grabing
        area = [0,0,0,0]
        for i in range(4):
            print("Enter point cordinante")
            area[i] = int(input())
        image = self.grabArea(tuple(area))
        print(image)
        return image

    def Quit(self):
        sys.exit(0)
        
    def TestCompare(self):#test hashing compasions
        i1 = grab()
        i2 = i1.copy()
        print("Change screen")
        time.sleep(15)
        i3 = grab()
        hash1 = imagehash.average_hash(i1)
        hash2 = imagehash.average_hash(i2)
        hash3 = imagehash.average_hash(i3)
        print("image 1 vs image 2")
        print(hash1 == hash2)
        print("image 1 vs image 3")
        print(hash1 == hash3)
        
    def switch(self,x):#navagates testing menu
        return {
            '1': self.TestSelectArea,
            '2': self.TestGrabScreen,
            '3': self.TestCompare,
            '4': self.TestRGBToInt,
            '0': self.Quit,
        }[x]()
    
    def test(self):#unit test for Screan reader
        select = -12
        while(select != '0'):
            print("=====Testing Mode=======")
            print("1)select area")#stores an area so operations can be done on it
            print("2)sceen shot")#takes a screen shot of area so it can be loaded to memory
            print("3)get Screen Hash")#makes a hash of image for comparison 
            print("4)get rgb single value")#returns the rgb as a single value 
            print("0)exit")
            select = input()
            self.switch(select)
        
    def __init__(self,mode=0):#creats a screen reader object and loads neural network that was taught to read numbers
        self.net = pickle.load(open("Number.txt","rb"))
        self.root = None
        self.selectedArea = None
        if(mode != 0):
            self.test()
            



