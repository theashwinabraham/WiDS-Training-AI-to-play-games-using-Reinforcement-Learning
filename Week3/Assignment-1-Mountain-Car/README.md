Welcome to Week 3. This week, we will be starting with a simple game and use Q-learning to "solve" the environment.

## Gymnasium

Provides environments to represent RL problems with a simple interface to interact with. 

Documentation: https://gymnasium.farama.org/

A basic usage of gymnasium is provided in the code, but if you are interested in pursuing RL further, familiarising yourself with it would be highly useful.

## Mountain Car

The environment we will be solving in the assignment. The task and documentation can be found here:

https://gymnasium.farama.org/environments/classic_control/mountain_car/

### Basic Strategy: 

Since the observation space here is continous, but classic RL algorithms require discrete observation space, we will first be discretizing the observation space by grouping nearby values together (a technique mentioned in Sutton and Barto in the chapter of function approximations) and considering them as a single state.

Then, the method goes as usual, act $\epsilon$ greedily, and keep updating the state-action pair values based on Q-Learning update rule:

$Q(s,a) \leftarrow Q(s,a) + \alpha (r_t + \gamma \text{max}_{a'} Q(s', a') - Q(s,a))$

You are free to play along with the hyperparameters, but one set of them have been provided to you. It is highly sugggested to try different values though, as the ones provided may not be the optimal ones and later, you will have to decide these hyperparameters yourselves.

Once done with the basic requirements of assignment, you may try to plot various quantities to check the learning performance of agent. Creativity is encouraged. You may also save the q-table every few training episodes.