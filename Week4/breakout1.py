import gym
import os
import ale_py
import numpy as np
from gym.wrappers import AtariPreprocessing
from gym.wrappers import FrameStack
from gym.core import ObservationWrapper
from gym.core import Wrapper
from gym.spaces import Box
import matplotlib.pyplot as plt
import pygame
import torch
import torch.nn as nn
import random
# from scipy.misc import imresize
import cv2
import tqdm

class PreprocessAtari(ObservationWrapper):
    def __init__(self, env):
        """A gym wrapper that crops, scales image into the desired shapes and optionally grayscales it."""
        ObservationWrapper.__init__(self,env)
        
        self.img_size = (84, 84)
        self.observation_space = Box(0.0, 1.0, (self.img_size[0], self.img_size[1], 1))

    def observation(self, img):
        """what happens to each observation"""
        
        # crop image (top and bottom, top from 34, bottom remove last 16)
        img = img[34:-16, :, :]
        
        # resize image
        img = cv2.resize(img, self.img_size)
        
        img = img.mean(-1,keepdims=True)
        
        img = img.astype('float32') / 255.
              
        return img

class FrameBuffer(Wrapper):
    def __init__(self, env, n_frames=4):
        """A gym wrapper that reshapes, crops and scales image into the desired shapes"""
        super(FrameBuffer, self).__init__(env)
        
        height, width, n_channels = env.observation_space.shape
        print(n_channels)
        """Multiply channels dimension by number of frames"""
        obs_shape = [n_channels * n_frames, height, width] 
        
        self.observation_space = Box(0.0, 1.0, obs_shape)
        self.framebuffer = np.zeros(obs_shape, 'float32')
        #print(self.framebuffer)

    def reset(self):
        
        self.framebuffer = np.zeros_like(self.framebuffer)
        
        self.update_buffer(self.env.reset()[0])
        return self.framebuffer
    
    def step(self, action):
        
        new_img, reward, terminated,truncated,  info = self.env.step(action)
        
        self.update_buffer(new_img)
        return self.framebuffer, reward, terminated, truncated, info
    
    def update_buffer(self, img):
        offset = self.env.observation_space.shape[-1]
        axis = 0
        cropped_framebuffer = self.framebuffer[:-1,:,:]
        img = np.array(img)
        img = np.transpose(img, (2, 0 ,1))
        self.framebuffer = np.concatenate([img, cropped_framebuffer], axis = axis)
    
def make_env():
    env = gym.make("ALE/Breakout-v5")
    env = PreprocessAtari(env)
    env = FrameBuffer(env, n_frames=4)
    return env

def make_env_render():
    env = gym.make("ALE/Breakout-v5", render_mode = "human")
    env = PreprocessAtari(env)
    env = FrameBuffer(env, n_frames=4)
    return env

class DQN(nn.Module):
    """
    Convolutional Neural Net with 3 conv layers and two linear layers
    """
    def __init__(self, input_shape, n_actions):
        super(DQN, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(input_shape[0], 16, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=4, stride=2),
            nn.ReLU(),
            
        )

        conv_out_size = self._get_conv_out(input_shape)
        self.fc = nn.Sequential(
            nn.Linear(conv_out_size, n_actions),
            
        )
    
    def _get_conv_out(self, shape):
        o = self.conv(torch.zeros(1, *shape))
        return int(np.prod(o.size()))

    def forward(self, x):
        if isinstance(x, np.ndarray) : 
            x = torch.FloatTensor(x)

        elif not isinstance(x, torch.Tensor):
            x = torch.FloatTensor(x).to("cpu")
            x = x.unsqueeze(0)
        conv_out = self.conv(x).view(x.size()[0], -1)
        return self.fc(conv_out)





class DQNAgent:

    def __init__(self, state_space, action_space, max_memory_size, batch_size, gamma, lr,
                 dropout, exploration_max, exploration_min, exploration_decay):

        # Define DQN Layers
        self.state_space = state_space
        self.action_space = action_space
        self.device = 'cuda' 
        
        # DQN network  
        self.dqn =DQN(state_space, action_space).to(self.device)
        self.target_dqn = DQN(state_space, action_space).to(self.device)

        self.optimizer = torch.optim.Adam(self.dqn.parameters(), lr=lr)

        # Create memory
        self.max_memory_size = max_memory_size
    
        self.STATE_MEM = torch.zeros(max_memory_size, *self.state_space)
        self.ACTION_MEM = torch.zeros(max_memory_size, 1)
        self.REWARD_MEM = torch.zeros(max_memory_size, 1)
        self.STATE2_MEM = torch.zeros(max_memory_size, *self.state_space)
        self.DONE_MEM = torch.zeros(max_memory_size, 1)
        self.ending_position = 0
        self.num_in_queue = 0
        
        self.memory_sample_size = batch_size
        
        # Learning parameters
        self.gamma = gamma
        self.l1 = nn.SmoothL1Loss().to(self.device) # Also known as Huber loss
        self.exploration_max = exploration_max
        self.exploration_rate = exploration_max
        self.exploration_min = exploration_min
        self.exploration_decay = exploration_decay

    def remember(self, state, action, reward, state2, done):
        """Store the experiences in a buffer to use later"""
        self.STATE_MEM[self.ending_position] = state.float()
        self.ACTION_MEM[self.ending_position] = action.float()
        self.REWARD_MEM[self.ending_position] = reward.float()
        self.STATE2_MEM[self.ending_position] = state2.float()
        self.DONE_MEM[self.ending_position] = done.float()
        self.ending_position = (self.ending_position + 1) % self.max_memory_size  # FIFO tensor
        self.num_in_queue = min(self.num_in_queue + 1, self.max_memory_size)
    
    def batch_experiences(self):
        """Randomly sample 'batch size' experiences"""
        idx = random.choices(range(self.num_in_queue), k=self.memory_sample_size)
        STATE = self.STATE_MEM[idx]
        ACTION = self.ACTION_MEM[idx]
        REWARD = self.REWARD_MEM[idx]
        STATE2 = self.STATE2_MEM[idx]
        DONE = self.DONE_MEM[idx]      
        return STATE, ACTION, REWARD, STATE2, DONE
    
    def act(self, state):
        """Epsilon-greedy action"""
        if random.random() < self.exploration_rate:  
            return torch.tensor([[random.randrange(self.action_space)]]) , 0
        else:
            return torch.argmax(self.dqn(state.to(self.device))).unsqueeze(0).unsqueeze(0).cpu() , 1

    def act_greedy(self, state):
        return torch.argmax(self.dqn(state.to(self.device))).unsqueeze(0).unsqueeze(0).cpu()

    
    def experience_replay(self):
        if self.memory_sample_size > self.num_in_queue:
            return
    
        # Sample a batch of experiences
        STATE, ACTION, REWARD, STATE2, DONE = self.batch_experiences()
        STATE = STATE.to(self.device)
        ACTION = ACTION.to(self.device)
        REWARD = REWARD.to(self.device)
        STATE2 = STATE2.to(self.device)
        DONE = DONE.to(self.device)
        
        self.optimizer.zero_grad()
        # Q-Learning target is Q*(S, A) <- r + γ max_a Q(S', a) 
        target = REWARD + torch.mul((self.gamma * self.dqn(STATE2).max(1).values.unsqueeze(1)), 1 - DONE)
        current = self.dqn(STATE).gather(1, ACTION.long())
        
        loss = self.l1(current, target)
        loss.backward() # Compute gradients
        self.optimizer.step() # Backpropagate error

        self.exploration_rate *= self.exploration_decay
        
        # Makes sure that exploration rate is always at least 'exploration min'
        self.exploration_rate = max(self.exploration_rate, self.exploration_min)

def save_network(network, epoch_label):
    save_filename = 'net_%s.pth' % epoch_label
    save_path = os.path.join('./savedModels', save_filename)
    torch.save(network.state_dict(), save_path)
def run(num_episodes=10000, exploration_max=1):
   
    env = make_env()
    env.reset
    observation_space = env.observation_space.shape
    action_space = env.action_space.n
    agent = DQNAgent(state_space=observation_space,
                     action_space=action_space,
                     max_memory_size=30000,
                     batch_size=32,
                     gamma=0.99,
                     lr=0.00025,
                     dropout=0.2,
                     exploration_max=0.4,
                     exploration_min=0.1,
                     exploration_decay=1)
    
    # Restart the enviroment for each episode
    num_episodes = num_episodes
    env.reset()
    
    total_rewards = []
    
    for ep_num in range(num_episodes):
        state = env.reset()
        state = torch.Tensor([state])
        total_reward = 0
        steps = 0
        while True:
            action, greedy = agent.act(state)
            #print(greedy, end = "")

            steps += 1
            
            state_next, reward, terminated, truncated, info = env.step(int(action[0]))
            total_reward += reward
            state_next = torch.Tensor([state_next])
            reward = torch.tensor([reward]).unsqueeze(0)
            
            terminal = torch.tensor([int(terminated)]).unsqueeze(0)
            
            agent.remember(state, action, reward, state_next, terminal)
            agent.experience_replay()
            
            state = state_next
            if terminal:
                break
        if ep_num%200 == 0 and ep_num != 0 :
            save_network(agent.dqn, ep_num) 
        
        total_rewards.append(total_reward)
       

        print("Episode {} score = {}, average score = {}".format(ep_num + 1, total_rewards[-1], np.mean(total_rewards),))
         

    
    env.close()
run()