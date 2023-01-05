from bandits import Bandit
import numpy as np

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
        self.Q = initialQ
        self.N = np.zeros((self.banditN), dtype = np.int)
        
    def action(self) -> int:
        a = np.argmax(self.Q) 
        return a

    def update(self, choice: int, reward: int) -> None:
        self.N[choice] += 1
        self.Q[choice] += ( reward - self.Q[choice] ) / self.N[choice]

class epsGreedyAgent(Agent):
    def __init__(self, bandits: Bandit, epsilon : float) -> None:
        super().__init__(bandits)
        self.epsilon = epsilon
        self.Q = np.zeros((self.banditN))
        self.N = np.zeros((self.banditN), dtype = np.int)

    def action(self) -> int:
        if np.random.random() > self.epsilon:
            a = np.argmax(self.Q)
        else:
            a = np.random.randint(self.banditN)
        return a

    def update(self, choice: int, reward: int) -> None:
        self.N[choice] += 1
        self.Q[choice] += ( reward - self.Q[choice] ) / self.N[choice]

class UCBAAgent(Agent):
    def __init__(self, bandits: Bandit, c: float) -> None:
        super().__init__(bandits)
        self.c = c
        self.Q = np.zeros((self.banditN))
        self.N = np.zeros((self.banditN), dtype = np.int)

    def action(self) -> int:
        if self.numiters < self.banditN:
            a = self.numiters
        else:
            U = self.c * (np.sqrt(np.log(self.numiters) / self.N))
            a = np.argmax(self.Q + U)
        return a

    def update(self, choice: int, reward: int) -> None:
        self.N[choice] += 1
        self.Q[choice] += ( reward - self.Q[choice] ) / self.N[choice]

class GradientBanditAgent(Agent):
    def __init__(self, bandits: Bandit, alpha : float) -> None:
        super().__init__(bandits)
        self.alpha = alpha
        self.pi = np.ones(self.banditN, dtype = np.float64)
        self.pi = self.pi / np.sum(self.pi)
        self.H = np.zeros((self.banditN))
        self.mean_reward = 0

    def action(self) -> int:
        return np.random.choice(np.arange(self.banditN), size=1, p = self.pi)

    def update(self, choice: int, reward: int) -> None:
        self.mean_reward += (reward - self.mean_reward) / self.numiters
        self.H = np.array([ self.H[action] + self.alpha * (reward - self.mean_reward) * ( (choice == action) - self.pi[action]) for action in range(len(self.H)) ]).reshape(-1)
        exp_H = np.exp(self.H)
        self.pi = exp_H / np.sum(exp_H)
        self.pi = self.pi / np.sum(self.pi)

class ThompsonSamplerAgent(Agent):
    def __init__(self, bandits: Bandit, alpha: float = 1, beta: float = 1) -> None:
        super().__init__(bandits)
        self.alpha = alpha # Controls the initial standard deviation of the Gaussian distribution of each Q-value
        self.beta = beta
        self.Q = np.zeros((self.banditN))
        self.N = np.zeros((self.banditN), dtype = np.int)
        self.success = [ [1,1] for action in range(self.banditN) ]

    def action(self) -> int:
        if self.bandit.type == "Gaussian":
            samples = np.random.normal(loc=self.Q, scale=self.alpha/(np.sqrt(self.N) + self.beta))
        elif self.bandit.type == "Bernoulli":
            samples = [ np.random.beta(a = action[0] , b =  action[1]) for action in self.success ]

        return np.argmax(samples)

    def update(self, choice: int, reward: int) -> None:
        self.N[choice] += 1
        self.Q[choice] += ( reward - self.Q[choice] ) / self.N[choice]
        self.success[choice] = np.add(self.success[choice], [reward == 1, reward == 0])

