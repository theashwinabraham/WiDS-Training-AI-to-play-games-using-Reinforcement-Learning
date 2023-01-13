from agents import *
import numpy as np
import matplotlib.pyplot as plt

NUM_ITER = 1000
N_ARMS = 15

Greedy = GreedyAgent(Bandit(N_ARMS, "Gaussian"), np.zeros(N_ARMS))
egreedy = epsGreedyAgent(Bandit(N_ARMS, "Gaussian"), 0.1, np.zeros(N_ARMS))
ucba = UCBAAgent(Bandit(N_ARMS, "Gaussian"),0.1 ,np.zeros(N_ARMS))
grad = GradientBanditAgent(Bandit(N_ARMS, "Gaussian"), 0.1, np.zeros(N_ARMS))
thomas_bern = ThompsonSamplerAgent(Bandit(N_ARMS, "Bernoulli"))
#thomas_gaussian = ThompsonSamplerAgent(Bandit(N_ARMS, "Gaussian"))

bandits = [Greedy, egreedy, ucba, grad, thomas_bern]
labels = ["Greedy", "eps-greedy", "UCBA", "Grad", "Thomas_Bernoulli"]

steps = np.arange(NUM_ITER)
regrets = np.zeros((N_ARMS, NUM_ITER))

for i in range(1,NUM_ITER) : 
    for bandit in range(5) : 
        reward = bandits[bandit].act()
        regrets[bandit][i] = bandits[bandit].bandit.get_regret()/i

for i in range(5) : 
    plt.plot(steps, regrets[i][:], label = labels[i])

plt.legend()
plt.show()

