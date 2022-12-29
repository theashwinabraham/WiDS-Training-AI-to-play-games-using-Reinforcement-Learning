import numpy as np

# N bandits together
class Nbandits:

    def __init__(self,n:int) -> None:    
        self.N = n
        # bandits will give reward/no reward
        self.probs = np.random.uniform(size=(n,))
        self.optimal = np.max(self.probs)

    def getN(self)->int: return self.N

    #pull the kth lever 0 to n-1
    def choose(self,k:int) -> int:
        assert(0<=k<=self.N)
        # returns 1 with probability = self.probs[k]
        return int(np.random.uniform()<self.probs[k])

if __name__=='__main__':
    pass