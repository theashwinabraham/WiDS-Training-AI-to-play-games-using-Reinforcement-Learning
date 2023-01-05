from agents import *
import numpy as np
import matplotlib.pyplot as plt

NUM_ITER = 500

Greedy = GreedyAgent(Bandit(5, "Gaussian"), np.zeros(5))
egreedy = epsGreedyAgent(Bandit(5, "Gaussian"), 0.1, np.zeros(5))
ucba = UCBAAgent(Bandit(5, "Gaussian"),0.1 ,np.zeros(5))
grad = GradientBanditAgent(Bandit(5, "Gaussian"), 0.1, np.zeros(5))
thomas = ThompsonSamplerAgent(Bandit(5, "Gaussian"))

bandits = [Greedy, egreedy, ucba, grad, thomas]
labels = ["Greedy", "eps-greedy", "UCBA", "Grad", "Thomas"]

steps = np.arange(NUM_ITER)
regrets = np.zeros((5, NUM_ITER))

for i in range(NUM_ITER) : 
    for bandit in range(5) : 
        reward = bandits[bandit].act()
        regrets[bandit][i] = bandits[bandit].bandit.get_regret()

for i in range(5) : 
    plt.plot(steps, regrets[i][:], label = labels[i])

print(regrets)

plt.legend()
plt.show()

