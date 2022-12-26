import sys
import copy

'''
Here we implement the minimax algorithm for the game of Tic-Tac-Toe.
Since Tic-Tac-Toe is a finite two player game, there is a non-losing strategy for one of the players.
This statement is true for every finite two player game, including games such as Chess!

This strategy is found using the Minimax algorithm.

The idea is based on forming the game tree:
The root of this tree is the starting position, and the children of each node are
the positions reachable from the node position. If the game is lost/won at a position,
it is terminated, i.e., the corresponding node has no children.

Nodes at even levels (the root is at level 0) are the positions when the first player (call her A) is to play
and nodes at the odd levels are the positions when the second player (call her B) is to play.

Now, we say a node is winning iff there exists a strategy for the player of that node such that no matter what the other player does, 
she will win. A node is losing iff there if no matter what the player of the node does, the other player can play in such a way that she loses.
If neither are true, we say the node is drawn.

Now, if a node is winning, then there must exist a move the node player makes such that from then on the other player is losing, even if she plays perfectly.
A move is a transition from a parent node to a child node (remember parent player and child player are different).

So, a node is winning if there exists a child node that is losing.
A node is drawn if there exists no losing child node but there does exist a drawn child node.
A node is losing if every child node is winning.

Since we know the statuses of all the leaf nodes (all either winning, losing or drawn),
we can get the statuses of every node (ie every position) from the bottom up, recursively.
Hence, every node is either winning, losing or drawn, including the root node.

This proves the statement above, and this algorithm for finding the node statuses is known as the Minimax algorithm.

The disadvantage is that this algorithm is extremely computationally expensive. It's training time (time taken to find out status of each node)
is proportional to the number of nodes, ie, the number of reachable game states. For a game like Chess, this is on the order of 10^40!

Therefore, the minimax algorithm is not really used, except for tiny problems, and instead, real reinforcement learning algorithms are used, which
may be less accurate, but are way less computationally expensive.

The minimax algorithm can be generalized to multiplayer games. Here we deal with states, and associate a value to each state.
We seek to maximize the value of the final state we reach.
A set of moves a1, a2 ... an by the players will cause the initial state S to transition to a state S' with the same player's chance again to play.

Using the minimax algorithm, Player 1 will seek to make the move such that the value of S' is maximum, assuming each other player always moves after
this to decrease the value of S'. We assign this maximum value as the value of S.

Mathematically this becomes:
Val(S) = max_{a1} min_{a2, ... an} Val(S'(S, a1, a2 ... an))
(S' is written here as a function of S, a1, a2 ... an)

This algorithm is known as the minimax algorithm since it is usually stated in terms of loss functions that we strive to minimize.
This causes the min and max to be interchanged in the expression (hence minimax)
'''

dim = int(sys.argv[1]) if len(sys.argv) > 1 else 3 

def mark(board, i, j, player):
    nboard = copy.deepcopy(board)
    assert nboard[i][j] == 0
    nboard[i][j] = player
    return nboard

# X = 1, O = -1, unmarked = 0
class State:
    def __init__(self, current_player = 1, board = [[0] * dim for _ in range(dim)]) -> None:
        self.board = board
        self.current_player = current_player
        self.children = {}
        self.best_move = None
        if self.winning() != 0:
            self.status = 1 if self.winning() == self.current_player else -1
        else:
            if len(self.possibilities()) == 0:
                self.status = 0
            else:
                returned = False
                draw = False
                for (i, j) in self.possibilities():
                    next_state = State(-self.current_player, mark(self.board, i, j, self.current_player))
                    self.children[(i, j)] = next_state
                    if next_state.status == -1: # If there is a losing child, then we pick that losing child
                        self.best_move = (i, j)
                        self.status = 1
                        returned = True
                    elif next_state.status == 0: # If there is no losing child, but a drawing child, we pick that drawing chidl
                        if not returned:
                            self.best_move = (i, j)
                        draw = True

                if not returned:
                    if draw:
                        self.status = 0
                    else:
                        self.status = -1
                        self.best_move = list(self.children.keys())[0] # If all children are winning, we pick any one child

    def winning(self):
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
    
    def possibilities(self):
        return [(i, j) for i in range(dim) for j in range(dim) if self.board[i][j] == 0]

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

_start = input('Do you wish to start (y/n)? ')
start = True if _start == 'y' or _start == 'Y' else False

if start:
    print((' - ' * dim + '\n\n')*dim)
    start_pos = eval(input('Enter your move as a tuple: '))
    assert len(start_pos) == 2 and 0 <= start_pos[0] < dim and 0 <= start_pos[1] < dim
    i = start_pos[0]
    j = start_pos[1]
    board = [[0]*dim for _ in range(dim)]
    board[i][j] = 1
    state = State(-1, board)
    print(state)
    if state.best_move is None:
        if state.status == 1:
            print('Computer has won')
        elif state.status == -1:
            print('You have won')
        else:
            print('Draw')
    else:
        state = state.children[state.best_move]
        print('Computer Played: ')
        print(state)
    
    while True:
        pos = eval(input('Enter your move as a tuple: '))
        assert len(pos) == 2 and 0 <= pos[0] < dim and 0 <= pos[1] < dim
        state = state.children[pos]
        print(state)
        if state.best_move is None:
            if state.status == 1:
                print('Computer has won')
            elif state.status == -1:
                print('You have won')
            else:
                print('Draw')
            break
        else:
            state = state.children[state.best_move]
            print('Computer Played: ')
            print(state)
            if state.best_move is None:
                if state.status == 1:
                    print('You have won')
                elif state.status == -1:
                    print('Computer has won')
                else:
                    print('Draw')
                break
else:
    state = State()
    print(state)
    while True:
        if state.best_move is None:
            if state.status == 1:
                print('Computer has won')
            elif state.status == -1:
                print('You have won')
            else:
                print('Draw')
        else:
            state = state.children[state.best_move]
            print('Computer Played: ')
            print(state)
            if state.best_move is None:
                if state.status == 1:
                    print('You have won')
                elif state.status == -1:
                    print('Computer has won')
                else:
                    print('Draw')
                break
        
        pos = eval(input('Enter your move as a tuple: '))
        assert len(pos) == 2 and 0 <= pos[0] < dim and 0 <= pos[1] < dim
        state = state.children[pos]
        print(state)