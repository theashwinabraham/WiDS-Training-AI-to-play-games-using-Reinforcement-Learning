from bandits import Bandit
import numpy as np
import math
import random
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

class GreedyAgent(Agent): # DONE
    def __init__(self, bandits: Bandit, initialQ : float) -> None:
        super().__init__(bandits)
        self.Q_arr = [initialQ for _ in range(self.banditN)]
        self.eachCount = [0 for _ in range(self.banditN)]

        # add any member variables you may require
        
    # implement
    def action(self) -> int:
        
        return np.argmax(self.Q_arr)

    # implement
    def update(self, choice: int, reward: int) -> None:
        self.eachCount[choice] += 1
        self.Q_arr[choice] += (reward - self.Q_arr[choice])/self.eachCount[choice]

class epsGreedyAgent(Agent): # DONE
    def __init__(self, bandits: Bandit, epsilon : float) -> None:
        super().__init__(bandits)
        self.epsilon = epsilon
        self.Q_arr = [0 for _ in range(self.banditN)]
        self.eachCount = [0 for _ in range(self.banditN)]
        # add any member variables you may require
    
    # implement
    def action(self) -> int:
        if random.random() > self.epsilon:
            return np.argmax(self.Q_arr)
        else:
            return random.randint(0, self.banditN-1)

    # implement
    def update(self, choice: int, reward: int) -> None:
        self.eachCount[choice] += 1
        self.Q_arr[choice] += (reward - self.Q_arr[choice])/self.eachCount[choice]

class UCBAAgent(Agent): # DONE
    def __init__(self, bandits: Bandit, c: float) -> None:
        super().__init__(bandits)
        self.c = c
        self.Q_arr = [0 for _ in range(self.banditN)]
        self.eachCount = [0 for _ in range(self.banditN)]

    # implement
    def action(self) -> int:
        WeightArray = [(self.Q_arr[i] + self.c * np.sqrt(np.log(self.numiters + 1)/(self.eachCount[i]+1))) for i in range(self.banditN)]
        # print(WeightArray)
        return np.argmax(WeightArray)

    # implement
    def update(self, choice: int, reward: int) -> None:
        self.eachCount[choice] += 1
        self.Q_arr[choice] += (reward - self.Q_arr[choice])/self.eachCount[choice]

class GradientBanditAgent(Agent): # DONE
    def __init__(self, bandits: Bandit, alpha : float) -> None:
        super().__init__(bandits)
        self.alpha = alpha
        self.H_arr = [0.0 for _ in range(self.banditN)]
        self.pi_arr = [0.0 for _ in range(self.banditN)]
        # add any member variables you may require

    # implement
    def action(self) -> int:
        self.pi_arr = np.exp(self.H_arr) / np.sum(np.exp(self.H_arr), axis=0)
        return random.choices(range(self.banditN), weights = self.pi_arr, k=1)[0]

    # implement
    def update(self, choice: int, reward: int) -> None:
        #TODO: gradient descent
        self.H_arr[choice] += self.alpha * (reward - (self.rewards/self.numiters)) * (1 - self.pi_arr[choice])
        for i in range(self.banditN):
            if i == choice:
                continue
            self.H_arr[i] -= self.alpha * (reward - (self.rewards/self.numiters)) * self.pi_arr[i]

        

class ThompsonSamplerAgent(Agent): # DONE
    def __init__(self, bandits: Bandit, sigma0: float, sigma: float, mu0: float) -> None:
        super().__init__(bandits)
        self.sigma0 = sigma0
        self.mu0 = mu0
        self.armsum = [0 for _ in range(self.banditN)]
        self.sigma = sigma
        self.eachCount = [0 for _ in range(self.banditN)]
        # add any member variables you may require

    # implement 
    def action(self) -> int:
        samples = np.random.normal(loc=[math.pow((math.pow(self.sigma0, -2) + self.eachCount[i]*math.pow(self.sigma, -2)), -1)*((self.mu0/(self.sigma0*self.sigma0))+(self.armsum[i]/(self.sigma*self.sigma))) for i in range(self.banditN)], scale=[math.pow(math.pow(self.sigma0, -2) + self.eachCount[i]/self.sigma**2, -0.5) for i in range(self.banditN)])
        return np.argmax(samples)


    # implement
    def update(self, choice: int, reward: int) -> None:
        self.eachCount[choice] += 1
        self.armsum[choice] += reward

# Implement other subclasses if you want to try other strategies