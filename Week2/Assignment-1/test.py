from bandits import Bandit
from agents import *
import random
x=[0,0,0,0]
N = 100
M = 500
for u in range(N):
    game = Bandit(5,'Bernoulli')
    

    e = 0
    for j in range(M):
        e = e + game.choose(random.randint(0,4))
    x[0]+=e

    u = UCBAAgent(game,25.0)
    e = 0
    for j in range(M):
        e = e + u.act()
    x[1]+=e

    v = GradientBanditAgent(game,25)
    e = 0
    for j in range(M):
        e = e + v.act()
    x[2]+=e

    w = ThompsonSamplerAgent(game)
    e = 0
    for j in range(M):
        e = e + w.act()
    x[3]+=e

   

print(x[0]/(N*M))
print(x[1]/(N*M))
print(x[2]/(N*M))
print(x[3]/(N*M))