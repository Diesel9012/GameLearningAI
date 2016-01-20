from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import scipy.io
import pickle
import numpy as np

def RGBToInt(p):# turns a list of RGB values into a single number
        return int('%02x%02x%02x' % (p[0], p[1], p[2]), 16)

n = FeedForwardNetwork()

inLayer = LinearLayer(32*32)
hiddenLayer = SigmoidLayer(20)
hiddenLayer2 = SigmoidLayer(15)
outLayer = LinearLayer(10)

n.addInputModule(inLayer)
n.addModule(hiddenLayer)
n.addModule(hiddenLayer2)
n.addOutputModule(outLayer)

in_to_hidden = FullConnection(inLayer, hiddenLayer)
hidden_to_hidden = FullConnection(hiddenLayer, hiddenLayer2)
hidden_to_out = FullConnection(hiddenLayer2, outLayer)

n.addConnection(in_to_hidden)
n.addConnection(hidden_to_hidden)
n.addConnection(hidden_to_out)
n.sortModules()

ds = SupervisedDataSet(32*32, 10)
mat = scipy.io.loadmat('train_32x32.mat')
#73257
print("Loading data set")
for i in range(2000):
        #print(mat['y'][i][0])
        img = np.int32([int('0',16) for z in range(32*32)])
        for y in range (32):
                for x in range(32):
                        img[x*32+y] = np.int32(RGBToInt((mat['X'][x][y][0][i],mat['X'][x][y][1][i],mat['X'][x][y][2][i])))
        out = [0 for z in range(10)]
        out[mat['y'][i][0]-1] = 1
        ds.addSample(img,out)
print("learning")
trainer = BackpropTrainer(n, ds)
i = 20
while(i>=.04482):
        i=trainer.train()
        print(i)
#trainer.trainUntilConvergence()

file = open("Number.txt","wb+")
pickle.dump(n,file)
print ("Done")
file.close()
