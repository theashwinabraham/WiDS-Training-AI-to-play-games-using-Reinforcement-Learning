from bandits import Nbandits
#Import libraries if you need them

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

    #dont edit this function
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
        pass
        
    #implement
    def action(self) -> int:
        pass

    def update(self, choice: int, reward: int) -> None:
        pass

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

#Implement other subclasses if you want to try other strategies


if __name__=='__main__':

    #Determines type of Bandit
    bandit_type = "Bernoulli"
    bandit_arms = 10
    
    Bandits = Nbandits(bandit_arms, bandit_type)
    
    #Initialise agent based on strategy
    agent = None
    
    #Train Agent
    
    #Get Regret
    regret = Bandits.get_regret()    