# This is a bonus problem. 
# see what works
# You may see how the previously implemented policies work here; you may try out variations
import numpy as np
from bandits import Nbandits
# bandits shuffle once in x iters
class CBv1(Nbandits) :
    def __init__(self,n:int,type:str,x:int) -> None:
        super().__init__(n,type)
        self.x = x
        self.numiters = 0

    def reset_regret(self)->None:
        self.regret = 0.0
        self.numiters = 0
    
    #pull the kth lever 0 to n-1
    def choose(self,k:int) -> int:
        assert(0<=k<self.N)
        self.numiters +=1
        # returns 1 with probability = self.probs[k]
        if self.type == "Bernoulli":
            reward = int(np.random.uniform()<self.probs[k])
            if (self.numiters%self.x==0):
                self.probs = np.random.permutation(self.probs)
        #Returns reward based on gaussian distribution
        elif self.type == "Gaussian":
            reward = np.random.normal(self.means[k], 1)
            if (self.numiters%self.x==0):
                self.means = np.random.permutation(self.means)
        
        self.regret += self.optimal - reward
        return reward
        
#states alternate
class CBv2(Nbandits):
    def __init__(self, n: int, type: str, nstates:int) -> None:
        super().__init__(n, type)
        self.state = 0
        self.numstates = nstates
        if type == "Bernoulli":
            # bandits will give reward/no reward
            self.probs = np.random.uniform(size=(nstates,n))
            self.optimal = np.max(self.probs,axis=1)
        elif type == "Gaussian":
            self.means = np.random.normal(15, 10, (nstates,n))
            self.optimal = np.max(self.means,axis=1)
        
    def reset_regret(self) -> None:
        self.state = 0
        return super().reset_regret()

    def choose(self, k: int) -> int:
        assert(0<=k<self.N)
        # returns 1 with probability = self.probs[k]
        if self.type == "Bernoulli":            
            reward = int(np.random.uniform()<self.probs[self.state][k])
        #Returns reward based on gaussian distribution
        elif self.type == "Gaussian":
            reward = np.random.normal(self.means[self.state][k], 1)
        self.regret += self.optimal[k] - reward
        return reward

#not really contextual bandits
#MDP where each action changes the state
class MDPv1(Nbandits):
    def __init__(self, n: int, type: str,nstates:int) -> None:
        super().__init__(n, type)
        self.state = 0
        self.numstates = nstates
        if type == "Bernoulli":
            self.probs = np.random.uniform(size=(nstates,n))
            self.optimal = np.max(self.probs)
        elif type == "Gaussian":
            self.means = np.random.normal(15, 10, (nstates,n))
            self.optimal = np.max(self.means)
        self.act2state = np.random.randint(0,nstates,size = (n,))

    def reset_regret(self) -> None:
        self.state = 0
        return super().reset_regret()

    def choose(self, k: int) -> int:
        assert(0<=k<self.N)
        # returns 1 with probability = self.probs[k]
        if self.type == "Bernoulli":            
            reward = int(np.random.uniform()<self.probs[self.state][k])
        #Returns reward based on gaussian distribution
        elif self.type == "Gaussian":
            reward = np.random.normal(self.means[self.state][k], 1)
        self.state = self.act2state[k]
        self.regret += self.optimal - reward
        return reward