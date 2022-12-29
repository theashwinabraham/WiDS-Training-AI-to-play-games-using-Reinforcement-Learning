# Here we let multiple agents with the same policy run on the same bandit (same distribution)
# this will save time for the same task (you might prefer this for computing averages)

# try to use vector operations instead of loops where possible 

import numpy as np
BANDITS = ("Bernoulli", "Gaussian")

class NbanditswithM:
    def __init__(self, n:int,m:int, type:str) -> None:
        
        assert(type in BANDITS)
        self.N = n
        self.M = m
        self.type = type
        if type == "Bernoulli":
            # bandits will give reward/no reward
            self.probs = np.random.uniform(size=(n,))
            self.optimal = np.max(self.probs)
            
        elif type == "Gaussian":
            
            self.means = np.random.normal(15, 10, (n,))
            self.optimal = np.max(self.means)

        self.regret = np.zeros((m,))
    
    #Gets the cummulative regret
    def get_regret(self) -> np.ndarray:
        return self.regret

    def getN(self)->int: return self.N
    def getM(self)->int: return self.M

    def reset_regret(self)->None:
        self.regret = np.zeros((self.M,))
    
    #pull the kth lever 0 to n-1
    # ith element of k is choice of ith agent
    def choose(self,ks:np.ndarray) -> np.ndarray:
        #comment out once sure of code
        assert((0<=ks).all() and (ks<self.N).all())
        assert(ks.shape == (self.M,))

        if self.type == "Bernoulli":
            reward = (np.random.uniform(size=(self.M,))<self.probs[ks]).astype(int)
            self.regret += self.optimal - reward
            return reward
        
        #Returns reward based on gaussian distribution
        elif self.type == "Gaussian":
            reward = np.random.normal(self.means[ks], 1)
            self.regret += self.optimal - reward
            return reward

class MAgents:
    def __init__(self, bandits:NbanditswithM) -> None:
        self.Bandits = bandits
        self.BanditN = bandits.getN()
        self.M = bandits.getM()

        self.rewards = np.zeros((self.M,))
        self.numiters = 0

        #define common/required member variables here

        # define other member variables in the subclasses
    def actions(self) -> np.ndarray:
        pass
    def update(self, choice:np.ndarray, reward : np.ndarray) -> None:
        pass
    def act(self) -> np.ndarray:
        choices = self.actions()
        reward = self.Bandits.choose(choices)

        self.rewards += reward
        self.numiters += 1

        self.update(choices,reward)
        return reward        
        

class MGreedy(MAgents):
    def __init__(self, bandits: NbanditswithM, initialQs : float) -> None:
        super().__init__(bandits)
        # each row corresponds to an agent's Q values
        # Qs - > mxn matrix
        self.Qs = np.full((self.M,self.BanditN),initialQs)

    def actions(self) -> np.ndarray:
        return np.argmax(self.Qs,axis=1)

    # vectorise this in a better way
    def update(self, choice:np.ndarray, reward : np.ndarray) -> None:
        for (i,j) in zip(range(self.M),choice):
            self.Qs[i][j] += (reward[i]-self.Qs[i][j])/self.numiters
        return

## you could implement the rest

if __name__=="__main__":
    
    testbandit = NbanditswithM(120,5000,'Bernoulli')
    agent47 = MGreedy(testbandit,0.8)
    meanperf = [agent47.act().mean() for _ in range(1000)]
    testbandit.reset_regret()
    agent48 = MGreedy(testbandit,0.4)
    meanperf2 = [agent48.act().mean() for _ in range(1000)]
    testbandit.reset_regret()
    agent49 = MGreedy(testbandit,0)
    meanperf3 = [agent49.act().mean() for _ in range(1000)]
    print(testbandit.optimal)

    import matplotlib.pyplot as plt
    plt.plot(meanperf)
    plt.plot(meanperf2)
    plt.plot(meanperf3)
    plt.axhline(testbandit.optimal,color='r')
    plt.show()