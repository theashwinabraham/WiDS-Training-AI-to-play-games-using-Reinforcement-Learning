from bandits import Bandit
import numpy as np
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

class GreedyAgent(Agent):
    def __init__(self, bandits: Bandit, initialQ : float) -> None:
        super().__init__(bandits)
        self.x = [0]*self.bandit.getN()
        self.e = [0]*self.bandit.getN()
        # add any member variables you may require
        
    # implement
    def action(self) -> int:
        a=self.x[0]
        b=0
        for i in range(len(self.x)):
            if self.x[i]>a:
                a=self.x[i]
                b= i
        return b

    # implement
    def update(self, choice: int, reward: int) -> None:
        self.e[choice]=self.e[choice]+1
        self.x[choice]=(self.x[choice]*(self.e[choice]-1)+reward)/self.e[choice] 
        


class epsGreedyAgent(Agent):
    def __init__(self, bandits: Bandit, epsilon : float) -> None:
        super().__init__(bandits)
        self.epsilon = epsilon
        self.x = [0]*self.bandit.getN()
        self.e = [0]*self.bandit.getN()
    
    # implement
    def action(self) -> int:
        y = random.random()
        if y<=1-self.epsilon:
            a=self.x[0]
            b=0
            for i in range(len(self.x)):
               if self.x[i]>a:
                a=self.x[i]
                b= i
            return b
        else :
            return random.randint(0,self.bandit.getN()-1)
           
class UCBAAgent(Agent):
    def __init__(self, bandits: Bandit, c: float) -> None:
        super().__init__(bandits)
        self.c = c
        self.t = 1
        self.x = [0]*int(self.bandit.getN())
        self.b = [1]*int(self.bandit.getN())
        #d = [0]*self.bandit.getN
        # add any member variables you may require

    # implement
    def action(self) -> int:
        ind= 0

        a = self.x[0]+self.c*(np.sqrt(np.log(self.t)/self.b[0]))
        for i in range((int(self.bandit.getN()))):
            if a < self.x[i]+self.c*(np.sqrt(np.log(self.t)/self.b[i])):
                ind = i
                a = self.x[i]+self.c*(np.sqrt(np.log(self.t)/self.b[i]))
        
        return ind 

    # implement
    def update(self, choice: int, reward: int) -> None:
        self.t = self.t+1
        self.b[choice]+=self.b[choice]+1
        self.x[choice] = ((self.x[choice]*(self.b[choice]-1)+reward)/self.b[choice])

class GradientBanditAgent(Agent):
    def __init__(self, bandits: Bandit, alpha : float) -> None:
        super().__init__(bandits)
        self.alpha = alpha
        self.H = [0]*int(self.bandit.getN())
        self.phi = [1/self.bandit.getN()]*int(self.bandit.getN())
        self.total_reward=0
        self.a = 0
        self.numbers = []
        for u in range(self.bandit.getN()):
            self.numbers.append(u)
        # add any member variables you may require

    # implement
    def action(self) -> int:
        x = random.choices(self.numbers,weights=tuple(self.phi))
        return x[0]
        
    # implement
    def update(self, choice: int, reward: int) -> None:
        self.a+=1
        self.total_reward= (self.total_reward*(self.a-1)+ reward)/self.a
        self.H[choice]= self.H[choice]+self.alpha*(reward-self.total_reward)*(1-self.phi[choice])
        for k in range(len(self.H)):
            if k!=choice:
                self.H[k]= self.H[k]-self.alpha*(reward-self.total_reward)*(self.phi[k])
                
        self.phi = np.exp(self.H)/sum(np.exp(self.H))
               
            
            


class ThompsonSamplerAgent(Agent):
    def __init__(self, bandits: Bandit) -> None:
        super().__init__(bandits)
        self.alpha = [1]*int(self.bandit.getN())
        self.beta = [1]*int(self.bandit.getN())


    # implement
    def action(self) -> int:
        if self.bandit.type == 'Bernoulli':
            b = 0
            c = [0]*int(self.bandit.getN())
            for i in range(self.bandit.getN()):
                c[i]=np.random.beta(self.alpha[i],self.beta[i],size = None)
            a=c[0]
            for j in range(self.bandit.getN()):
                if c[j]>a:
                    b=j
            return b
                
    # implement
    def update(self, choice: int, reward: int) -> None:
        if self.bandit.type == 'Bernoulli':
            if reward==1:
                self.alpha[choice]+=1
            else:
                self.beta[choice]+=1

# Implement other subclasses if you want to try other strategies