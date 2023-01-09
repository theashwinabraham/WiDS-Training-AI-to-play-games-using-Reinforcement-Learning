import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

'''
The first task to work with a gym env is to initialise it using gym.make(name_of_env) and reset it using .reset() function. This resets the env to a starting position, with some noise in state. It returns a tuple of the initial state of environment and a dictionary containing info (Not important for the moment).

Just as a environment in RL, you can take action based on current state. This is done using env.step(action), and it returns the following 5 values:

1. Next State: The state the environment transitioned to after taking the step.

2. Reward: Reward received for taking the action

3. Terminated: A boolean which is true if the environment terminated after taking the action. The condition for this termination is provided in the documentation of the environment.

4. Truncated: A boolean which is true if the environment was truncated after taking the action, usually because we cannot run a environment for infinite time, and hence every environment has a truncation period. More details in the documentation

Note: You must call env.reset() after either termination or truncation.

5. Info: A dictionary containing information of env.

The observation space of Mountation Car is an array of two variables: Position of car(x - coordinate) and velocity of cart. 

Three actions are possible, as mentioned in documentation
'''
class QAgent:
    def __init__(self, env: str) -> None:
        self.env_name = env
        self.env = gym.make(env) 
        self.state = self.env.reset()[0] #Variable to store current state of the environment
        
        self.observation_space_size = len(self.state) #2 for Mountain Car
        
        self.actions = self.env.action_space.n # 3 for Mountain Car, represents total number of possible actions
        
        self.observation_space_low = self.env.observation_space.low #Returns array of length 2, representing the minimum values of position and velocity respectively. Consult documentation for more info.
        
        self.observation_space_high = self.env.observation_space.high
        
        #Hyperparameters. Play around with these values!!
        
        self.discrete_sizes = [25, 25] # Represents how many parts you want to discretize your observation space in. First element represents parts for position of car, and second for velocity of car.
        self.alpha = 0.1 # As defined in update rule
        self.gamma = 0.95 # As defined in update rule
        
        self.num_train_episodes = 25000 #Number of episodes to train the model for
        self.epsilon = 1 #Initial value for epsilon-greedy behavior
        self.num_episodes_decay = 15000 # Number of episodes to act epsilon-greedily for, after which epsilon becomes 0
        self.epsilon_decay = self.epsilon / self.num_episodes_decay # Linear decay of epsilon, that is the amount to be decreased from epsilon after every episode termination
        
        '''
        Q-Table. We have provided one way to initialise it, and tried to keep it general, so you even try a different environment. You are adviced to think of other ways you could have initialised it.
        
        The dimensions of Q-Table must be parts of state-1 x parts of state-2 x actions (why?). It is initialised with random values here.
        
        * operator opens the array. So *[1,2] represents 1,2. Hence *self.discrete_sizes, self.actions represents 25, 25, 3 here
        '''
        self.q_table = np.random.uniform(low=-2, high=0, size=(*self.discrete_sizes, self.actions))
        
    def get_state_index(self, state):
        '''
        Define a function which gives the index of the state in the Q_Table. Here a simple example to illustrate this task:
        
        Suppose low for position is 0, and high 2, and discretised it in 20 parts. Then the sections are [0-0.1], [0.1-0.2]...[1.9-2], and index for say position=0.45 will be 4 (in [0.4-0.5])
        
        The state here is a array of length self.observation_space_size(2). Other necessary variables are initialised in init method. Try to keep this function general for any environment, but you may hardcode the numbers if you feel the task is difficult to generalise.
        
        Return a tuple containing the indices along each dimension
        '''
        pass

    def update(self, state, action, reward, next_state, is_terminal):
        '''
        Update the value of q[state, action] in the q-table based on the update rule. 
        First discretize both the state and next_state to get indices in q-table.
        The boolean is_terminal here represents whether the state action pair resulted in termination (NOT TRUNCATION) of environment. In this case, update the value by considering max_a' q(s', a,) = 0 (consult theory for why) and not based on q-table.
        '''
        if is_terminal:
            pass
        else:
            pass
    
    def get_action(self):    
        '''
        Get the action either greedily, or randomly based on epsilon (You may use self.env.action_space.sample() to get a random action). Return an int representing action, based on self.state. Remember to discretize self.state first
        '''
        pass
    
    
    def env_step(self):
        '''
        Takes a step in the environment and updated q-table
        '''
        action = self.get_action()
        next_state, reward, terminated, truncated, info = self.env.step(action)
        
        self.update(self.state, action, reward, next_state, terminated and not truncated) # terminated and not truncated is true when the episode got terminated but not truncated.
        
        self.state = next_state
        
        return terminated or truncated # Represents whether we need to reset the environment
    
    def agent_eval(self):
        '''Visualise the performance of agent'''
        eval_env = gym.make(self.env_name, render_mode = "human")
        done = False
        eval_state = eval_env.reset()[0]
        while not done:
            action = None # Take action based on greedy strategy now
            next_state, reward, terminated, truncated, info = eval_env.step(action)
            
            eval_env.render() #Renders the environment on a window.
            
            done = terminated or truncated
            eval_state = next_state
          
    def train(self, eval_intervals):
        '''Main function to train the agent'''
        for episode in range(1, self.num_train_episodes + 1):
            done = False
            while not done:
                done = self.env_step()
            self.state = self.env.reset()[0] # Reset environment after end of episode
            
            self.epsilon = max(0, self.epsilon - self.epsilon_decay) #Update epsilon after every episode
            
            if episode % eval_intervals == 0:
                #Check performance of agent
                self.agent_eval()
        

if __name__ == "__main__":
    agent = QAgent("MountainCar-v0")
    agent.train(eval_intervals=1000) # Change the number to change frequency of evaluation
