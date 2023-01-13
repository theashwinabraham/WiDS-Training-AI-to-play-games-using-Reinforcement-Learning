# Importing Libraries

from bandits import Bandit
import numpy as np

# Implementing Classes

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
    def __init__(self, bandits: Bandit, initialQ) -> None:
        super().__init__(bandits)
        self.Qvals = initialQ
        self.count_actions = np.zeros(self.banditN)
        
    def action(self) -> int:
        a = np.argmax(self.Qvals)
        return a

    def update(self, choice: int, reward: int) -> None:

        self.count_actions[choice] += 1
        self.Qvals[choice] += (reward - self.Qvals[choice])/(self.count_actions[choice])
        return 

class epsGreedyAgent(Agent):
    def __init__(self, bandits: Bandit, epsilon : float, initialQ) -> None:

        super().__init__(bandits)
        self.epsilon = epsilon
        self.Qvals = initialQ
        self.count_actions = np.zeros(self.banditN)

    
    def action(self) -> int:
        
        # Greedy action
        a = np.argmax(self.Qvals)
        
        # The probability vector
        p_values = [self.epsilon/(self.banditN-1)]*self.banditN
        p_values[a] = 1 - self.epsilon

        # The choice of action using this scheme
        choice = np.argmax(np.random.multinomial(1, p_values))
        return choice

    def update(self, choice: int, reward: int) -> None:
        
        self.count_actions[choice] += 1
        self.Qvals[choice] += (reward - self.Qvals[choice])/(self.count_actions[choice])
        return 

class UCBAAgent(Agent):
    def __init__(self, bandits: Bandit, c: float, initialQ) -> None:
        super().__init__(bandits)
        self.c = c
        self.Qvals = initialQ
        self.count_actions = np.zeros(self.banditN)

    def action(self) -> int:
        
        if np.min(self.count_actions) == 0 :
            return np.argmin(self.count_actions)

        # Using UCBA
        a = np.argmax(self.Qvals + self.c * np.sqrt(self.numiters/self.count_actions))
        return a

    def update(self, choice: int, reward: int) -> None:
        
        self.count_actions[choice] += 1
        self.Qvals[choice] += (reward - self.Qvals[choice])/(self.count_actions[choice])
        return 

class GradientBanditAgent(Agent):
    def __init__(self, bandits: Bandit, alpha : float, initialH) -> None:
        super().__init__(bandits)
        self.alpha = alpha
        self.H = initialH
        self.R = 0
        self.count_actions = np.zeros(self.banditN)

    def action(self) -> int:
        
        p_values = (np.exp(self.H))/np.sum(np.exp(self.H))
        
        choice = np.argmax(np.random.multinomial(1, p_values))
        return choice 

    def update(self, choice: int, reward: int) -> None:
        
        identity = np.zeros(self.banditN)
        identity[choice] = 1

        policy = np.exp(self.H)/np.sum(np.exp(self.H))

        self.H += self.alpha*(reward - self.R)*(identity - policy)
        self.R += (reward - self.R)/self.numiters


class ThompsonSamplerAgent(Agent):
    def __init__(self, bandits: Bandit) -> None:

        # Assumption : std deviation = 1

        super().__init__(bandits)
        if self.bandit.type == "Bernoulli" :
            self.alphas = np.zeros(self.banditN) + 1.5
            self.betas = np.zeros(self.banditN) + 1.5
        
        else : 
            self.sigmas = np.full(self.banditN, 1)
            self.mus = np.zeros(self.banditN)


    def action(self) -> int:
        if self.bandit.type == "Bernoulli" :
            rewards = np.random.beta(self.alphas, self.betas)
            return np.argmax(rewards)

        else : 
            rewards = np.random.normal(loc = self.mus, scale = self.sigmas)
            return np.argmax(rewards)

    def update(self, choice: int, reward: int) -> None:

        if self.bandit.type == "Bernoulli" :
            self.alphas[choice] += reward
            self.betas[choice] += 1- reward        
            return 

        else : 
            self.sigmas[choice] = self.sigmas[choice]/np.sqrt(np.square(self.sigmas[choice]) + 1)
            self.mus[choice] = (reward*np.square(self.sigmas[choice]) + self.mus[choice])/(np.square(self.sigmas[choice]) + 1)
            return
