from bandits import Bandit
# Import libraries if you need them

class Agent:
    def __init__(self, bandit: Bandit) -> None:
        self.bandit = bandit
        self.banditN = bandit.getN()

        self.rewards = 0
        self.numiters = 0
    

    def action(self) -> int:
        '''This function returns which action is to be taken. It must be implemented in the subclasses.'''
        raise NotImplementedError()

    def update(self, choice : int, reward : int) -> None:
        '''This function updates all member variables you may require. It must be implemented in the subclasses.'''
        raise NotImplementedError()

    # dont edit this function
    def act(self) -> int:
        choice = self.action()
        reward = self.bandit.choose(choice)

        self.rewards += reward
        self.numiters += 1

        self.update(choice,reward)
        return reward

class GreedyAgent(Agent):
    def __init__(self, bandits: Bandit, initialQ : float) -> None:
        super().__init__(bandits)
        # add any member variables you may require
        
    # implement
    def action(self) -> int:
        pass

    # implement
    def update(self, choice: int, reward: int) -> None:
        pass

class epsGreedyAgent(Agent):
    def __init__(self, bandits: Bandit, epsilon : float) -> None:
        super().__init__(bandits)
        self.epsilon = epsilon
        # add any member variables you may require
    
    # implement
    def action(self) -> int:
        pass

    # implement
    def update(self, choice: int, reward: int) -> None:
        pass

class UCBAAgent(Agent):
    def __init__(self, bandits: Bandit, c: float) -> None:
        super().__init__(bandits)
        self.c = c
        # add any member variables you may require

    # implement
    def action(self) -> int:
        pass

    # implement
    def update(self, choice: int, reward: int) -> None:
        pass

class GradientBanditAgent(Agent):
    def __init__(self, bandits: Bandit, alpha : float) -> None:
        super().__init__(bandits)
        self.alpha = alpha
        # add any member variables you may require

    # implement
    def action(self) -> int:
        pass

    # implement
    def update(self, choice: int, reward: int) -> None:
        pass

class ThompsonSamplerAgent(Agent):
    def __init__(self, bandits: Bandit) -> None:
        super().__init__(bandits)
        # add any member variables you may require

    # implement
    def action(self) -> int:
        pass

    # implement
    def update(self, choice: int, reward: int) -> None:
        pass

# Implement other subclasses if you want to try other strategies