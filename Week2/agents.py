import numpy as np
from bandits import Nbandits

class Agent:
    def __init__(self, bandits:Nbandits) -> None:
        self.bandits = bandits
        self.banditN = bandits.getN()

        self.rewards = 0
        self.numiters = 0
        #define common/required member variables here

        # define other member variables in the subclasses
    
    # which lever to pull
    def action(self) -> int: #implement in the subclasses
        pass

    def update(self,choice : int, reward : int) -> None:
        pass

    #dont touch below
    def act(self) -> int:
        choice = self.action()
        reward = self.bandits.choose(choice)

        self.rewards += reward
        self.numiters += 1

        self.update(choice,reward)
        return reward

class GreedyAgent(Agent):
    def __init__(self, bandits: Nbandits, initialQ : float) -> None:
        super().__init__(bandits)
        #add member variables
        self.Q = np.full((self.banditN,),initialQ)
        
    #implement
    def action(self) -> int:
        return np.argmax(self.Q)

    def update(self, choice: int, reward: int) -> None:
        self.Q[choice] += (reward - self.Q[choice])/self.numiters
        return 

class epsGreedyAgent(Agent):
    def __init__(self, bandits: Nbandits, epsilon : float) -> None:
        super().__init__(bandits)
        self.epsilon = epsilon
        #add member variables
    
    #implement
    def action(self) -> int:
        pass

    def update(self, choice: int, reward: int) -> None:
        pass

class UCBAAgent(Agent):
    def __init__(self, bandits: Nbandits, c: float) -> None:
        super().__init__(bandits)
        self.c = c
        #add member variables

    #implement
    def action(self) -> int:
        pass

    def update(self, choice: int, reward: int) -> None:
        pass

class GradientBanditAgent(Agent):
    def __init__(self, bandits: Nbandits, alpha : float) -> None:
        super().__init__(bandits)
        self.alpha = alpha
        #add member variables

    #implement
    def action(self) -> int:
        pass

    def update(self, choice: int, reward: int) -> None:
        pass

class ThompsonSamplerAgent(Agent):
    def __init__(self, bandits: Nbandits) -> None:
        super().__init__(bandits)
        #add member variables

    #implement
    def action(self) -> int:
        pass

    def update(self, choice: int, reward: int) -> None:
        pass

if __name__=='__main__':
    import matplotlib.pyplot as plt

    Bandits = Nbandits(12)
    agent = GreedyAgent(Bandits,1)
    howitgo = [agent.act() for _ in range(150)]
    
    plt.plot(howitgo)
    plt.show()
    