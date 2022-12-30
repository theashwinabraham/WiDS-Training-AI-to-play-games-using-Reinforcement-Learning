import numpy as np

BANDITS = ["Bernoulli", "Gaussian"]
# N bandits together
class Nbandits:

    def __init__(self,n:int, type:str) -> None: 
        
        assert(type in BANDITS)
        self.N = n
        self.type = type
        if type == "Bernoulli":
            # bandits will give reward/no reward
            self.probs = np.random.uniform(size=(n,))
            self.optimal = np.max(self.probs)
            
        elif type == "Gaussian":
            
            self.means = np.random.normal(15, 10, (n,))
            self.optimal = np.max(self.means)

        self.regret = 0.0
    
    #Gets the cummulative regret
    def get_regret(self) -> float:
        return self.regret

    def getN(self)->int: return self.N

    def reset_regret(self)->None:
        self.regret = 0.0
    
    #pull the kth lever 0 to n-1
    def choose(self,k:int) -> int:
        assert(0<=k<self.N)
        # returns 1 with probability = self.probs[k]
        if self.type == "Bernoulli":
            
            reward = int(np.random.uniform()<self.probs[k])
            self.regret += self.optimal - reward
            return reward
        
        #Returns reward based on gaussian distribution
        elif self.type == "Gaussian":
            
            reward = np.random.normal(self.means[k], 1)
            self.regret += self.optimal - reward
            return reward

if __name__=='__main__':
    pass