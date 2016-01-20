from pybrain.rl.environments.episodic import EpisodicTask
import Output as opt
from screenReader import ScreenReader 
#keycodes
a= ["LEFT","UP","DOWN","RIGHT"]
sc = ScreenReader()
class TTask(EpisodicTask):
        def __init__(self, environment,ScoreBox,GameOver):
                """ All tasks are coupled to an environment. """
                self.env = environment
                self.N = 1500000000000000
                self.t = 0
                # limits for scaling of sensors and actors (None=disabled)
                self.sensor_limits = None
                self.actor_limits = None
                self.clipping = True
                self.scoreBox = ScoreBox
                self.discount = .1# Discount Rate for actions
                self.batchSize = 32#how many actions to learn over
                self.gameOver = GameOver

        
        def isFinished(self):
                if self.t >= self.N:
                        self.t = 0
                        return True and self.gameOver[0]()
                else:
                        self.t += 1
                        return False and self.gameOver[0]()
        def getObservation(self):
                self.state = self.env.getSensors()
                return self.state

         #Sets an action
        def performAction(self, ac):
                self.env.performAction(ac)

        def getReward(self):
                # sleep(0.01)
                # print(self.state, self.action)
                score = sc.GetScore(sc.grabArea(self.scoreBox))
                reward = 0
                for x in range(len(score)):
                        reward += score[x]*10**x
                return reward