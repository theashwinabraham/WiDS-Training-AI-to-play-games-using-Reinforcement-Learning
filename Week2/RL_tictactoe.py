import sys
import numpy as np
import copy
import random

'''
This is a basic script where an agent learns to play tic tac toe by in the manner described in the notes (Chapter 1, Section 1.5, page 7).

Your task will be to implement other strategies for balancing exploration and exploitation such as UCBA, Gradient Bandits and Thompson Sampling.
Most of the framework with which you will work with has already been coded up for you. You just have to implement the algorithms.

The epsilon greedy algorithm has already been coded up as well. So the code - as it is - can run. Try running it and training the agents, and
then try playing against the trained agents yourself!

As a sidenote, the actual RL algorithms used for training agents to play games are more sophisticated than this, so don't expect too much performance.
'''

dim = int(sys.argv[1]) if len(sys.argv) > 1 else 3

class Board:
    def __init__(self, board = None) -> None: # No mutable default arguments
        self.board = board if board else [[0 for _ in range(dim)] for _ in range(dim)] # [[0]*dim]*dim is evil

    def won_by(self) -> int: # 0 if no one has won, 1 if X has won, -1 if O has won
        for i in range(dim):
            for j in range(dim):
                if self.board[i][0] == 0 or self.board[i][j] != self.board[i][0]:
                    break
            else:
                return self.board[i][0]
            for j in range(dim):
                if self.board[0][i] == 0 or self.board[j][i] != self.board[0][i]:
                    break
            else:
                return self.board[0][i]
        for i in range(dim):
            if self.board[0][0] == 0 or self.board[i][i] != self.board[0][0]:
                break
        else:
            return self.board[0][0]
        for i in range(dim):
            if self.board[0][dim - 1] == 0 or self.board[i][dim - i - 1] != self.board[0][dim - 1]:
                break
        else:
            return self.board[0][dim - 1]
        return 0
    
    def possibilities(self) -> list:
        return [(i, j) for i in range(dim) for j in range(dim) if self.board[i][j] == 0]
    
    def marked(self, mov, player):
        assert player == 1 or player == -1
        assert mov in self.possibilities(), "An illegal move was made"
        nboard = copy.deepcopy(self.board)
        nboard[mov[0]][mov[1]] = player
        return Board(nboard)

    def __str__(self) -> str:
        s = ''
        for i in range(dim):
            for j in range(dim):
                if self.board[i][j] == 0:
                    s += ' - '
                elif self.board[i][j] == 1:
                    s += ' X '
                else:
                    s += ' O '
            s += '\n\n'
        return s

class State:
    def __init__(self, board: Board = Board(), player = 1) -> None:
        self.board = board
        self.player = player
        self.values = {1:self.board.won_by(), -1: -self.board.won_by()}
        self.children = {}
        self.parent = None

class Agent:
    def __init__(self, id = 1) -> None:
        self.id = id
    
    def train_policy(self, state: State) -> State:
        raise NotImplementedError() # Must be implemented in subclass

    def make_move(self, mov: tuple, state: State) -> State:
        assert self.id == state.player
        if mov not in state.children:
            state.children[mov] = State(state.board.marked(mov, self.id), -self.id)
            state.children[mov].parent = state
        return state.children[mov]
    
    def test_policy(self, state: State) -> State: # Greedy Policy
        val_mov = [(new_state.values[self.id], mov) for mov, new_state in state.children.items()]
        val_mov0 = np.array([x[0] for x in val_mov])
        max_val, best_move = val_mov[np.random.choice(np.flatnonzero(np.isclose(val_mov0, val_mov0.max())))] if len(val_mov) > 0 else (0, random.choice(state.board.possibilities()))
        if max_val < 0 and len(state.children) < len(state.board.possibilities()):
            mov = random.choice(list(set(state.board.possibilities()) - set(state.children.keys())))
            st = self.make_move(mov, state)
            self.valuate(mov, state)
            return st
        else:
            st = self.make_move(best_move, state)
            self.valuate(best_move, state)
            return st


class Interactive_Agent(Agent):
    def __init__(self, id = 1) -> None:
        super().__init__(id)
    
    def test_policy(self, state : State) -> State:
        print(state.board)
        mov = eval(input(f'Enter your move as a tuple, Player {"X" if self.id == 1 else "O"}: '))
        return self.make_move(mov, state)
    
    def train_policy(self, state : State) -> State:
        self.test_policy(state)


class RL_Agent(Agent):
    def __init__(self, id = 1, learn_rate = 0.1) -> None:
        super().__init__(id)
        self.alpha = learn_rate

    def valuate(self, move: tuple, state: State) -> None:
        state.values[self.id] += self.alpha*(state.children[move].values[self.id] - state.values[self.id])
        if state.parent:
            state.parent.values[self.id] += self.alpha*(state.values[self.id] - state.parent.values[self.id])


class Eps_Greedy_Agent(RL_Agent):
    def __init__(self, id = 1, learn_rate = 0.9, epsilon = 0.5) -> None:
        super().__init__(id, learn_rate)
        self.eps = epsilon

    def train_policy(self, state: State) -> State:
        if np.random.binomial(1, self.eps):
            mov = random.choice(state.board.possibilities())
            return self.make_move(mov, state) # Non-greedy move, no evaluation required
        else:
            val_mov = [(new_state.values[self.id], mov) for mov, new_state in state.children.items()]
            val_mov0 = np.array([x[0] for x in val_mov])
            max_val, best_move = val_mov[np.random.choice(np.flatnonzero(np.isclose(val_mov0, val_mov0.max())))] if len(val_mov) > 0 else (0, random.choice(state.board.possibilities()))
            if max_val < 0 and len(state.children) < len(state.board.possibilities()):
                mov = random.choice(list(set(state.board.possibilities()) - set(state.children.keys())))
                st = self.make_move(mov, state)
                self.valuate(mov, state)
                return st
            else:
                st = self.make_move(best_move, state)
                self.valuate(best_move, state)
                return st


'''For these classes, only the training policies and constructor have to be made. Feel free to make any additional functions you may have need of.'''
class UCBA_Agent(RL_Agent):
    '''Implement this'''
    pass

class Gradient_Agent(RL_Agent):
    '''Implement this'''
    pass

class Thompson_Agent(RL_Agent):
    '''Implement this'''
    pass


def train(agent1: Agent, agent2: Agent, start_state = State(), num_games: int = int(sys.argv[2]) if len(sys.argv) > 2 else 100, suppress_prints: bool = False):
    scores = {1:0, -1:0, 0:0}
    won_by = {1: "Won by X", -1: "Won by O", 0: "Draw"}
    for num_played in range(num_games):
        state = start_state
        while True:
            state = agent1.train_policy(state)

            if len(state.board.possibilities()) == 0 or state.board.won_by() != 0:
                break

            state = agent2.train_policy(state)

            if len(state.board.possibilities()) == 0 or state.board.won_by() != 0:
                break

        scores[state.board.won_by()] += 1
        if not suppress_prints:
            print(f'Game #{1 + num_played}: {won_by[state.board.won_by()]}')
            print(state.board)
            print(f'Wins by X: {scores[1]}, Wins by O: {scores[-1]}, Draws: {scores[0]}\n\n')

def play_against_agent(start_state: State = State()):
    num_played = 0
    while input('Press q to quit playing: ') not in ['q', 'Q']:
        iagent = Interactive_Agent(1 if input('Enter y if you want to play first: ') in ['y', 'Y'] else -1)
        rl_algent = Eps_Greedy_Agent(-iagent.id)
        agents = {iagent.id : iagent, rl_algent.id : rl_algent}
        won_by = {iagent.id: "Won by you", rl_algent.id: "Won by computer", 0: "Draw"}

        state = start_state
        while True:
            state = agents[1].test_policy(state)

            if len(state.board.possibilities()) == 0 or state.board.won_by() != 0:
                break

            state = agents[-1].test_policy(state)

            if len(state.board.possibilities()) == 0 or state.board.won_by() != 0:
                break
        

        print(f'Game #{1 + num_played}: {won_by[state.board.won_by()]}')
        print(state.board)
        num_played += 1



start = State()
train(Eps_Greedy_Agent(), Eps_Greedy_Agent(-1), start)
play_against_agent(start)