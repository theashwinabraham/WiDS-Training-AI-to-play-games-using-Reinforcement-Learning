# Week 2

In this week and the next, we shall properly learn about Multiarmed Bandits and Finite Markov Decision Processes.

For your assignment you have to implement some policies for the MultiArmed Bandit problem

- `bandits.py` contains the class for the bandit. You do not need to edit this unless you want to add input formats, for eg. batchwise. The bandits here give 0 or 1 reward with fixed probabilities. 
(Note for Thompson sampling - Beta is the conjugate for a Bernouilli dsitribution)

- `agents.py` contains the class for agents and sub classes for each policy type. You only need to implement the subclasses (again, unless you want to add something or fix bugs).

- `results.py` show us your results -- graphs and all. Be creative.