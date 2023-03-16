from chessEngine import GameState
from math import sqrt,log
import random

weights = {'P' : 100, 'N' : 320, 'B' : 330, 'R' : 500, 'Q' : 900, 'K': 20000}
pstPawn = { 'P':   [[0,  0,  0,  0,  0,  0,  0,  0],
                    [50, 50, 50, 50, 50, 50, 50, 50],
                    [10, 10, 20, 30, 30, 20, 10, 10],
                    [5,  5, 10, 25, 25, 10,  5,  5],
                    [0,  0,  0, 20, 20,  0,  0,  0],
                    [5, -5,-10,  0,  0,-10, -5,  5],
                    [5, 10, 10,-20,-20, 10, 10,  5],
                    [0,  0,  0,  0,  0,  0,  0,  0]],

            'N':   [[-50,-40,-30,-30,-30,-30,-40,-50],
                    [-40,-20,  0,  0,  0,  0,-20,-40],
                    [-30,  0, 10, 15, 15, 10,  0,-30],
                    [-30,  5, 15, 20, 20, 15,  5,-30],
                    [-30,  0, 15, 20, 20, 15,  0,-30],
                    [-30,  5, 10, 15, 15, 10,  5,-30],
                    [-40,-20,  0,  5,  5,  0,-20,-40],
                    [-50,-40,-30,-30,-30,-30,-40,-50]],

            'B':   [[-20,-10,-10,-10,-10,-10,-10,-20],
                    [-10,  0,  0,  0,  0,  0,  0,-10],
                    [-10,  0,  5, 10, 10,  5,  0,-10],
                    [-10,  5,  5, 10, 10,  5,  5,-10],
                    [-10,  0, 10, 10, 10, 10,  0,-10],
                    [-10, 10, 10, 10, 10, 10, 10,-10],
                    [-10,  5,  0,  0,  0,  0,  5,-10],
                    [-20,-10,-10,-10,-10,-10,-10,-20]],

            'R':   [[0,  0,  0,  0,  0,  0,  0,  0],
                    [5, 10, 10, 10, 10, 10, 10,  5],
                    [-5,  0,  0,  0,  0,  0,  0, -5],
                    [-5,  0,  0,  0,  0,  0,  0, -5],
                    [-5,  0,  0,  0,  0,  0,  0, -5],
                    [-5,  0,  0,  0,  0,  0,  0, -5],
                    [-5,  0,  0,  0,  0,  0,  0, -5],
                    [0,  0,  0,  5,  5,  0,  0,  0]],

            'Q':   [[-20,-10,-10, -5, -5,-10,-10,-20],
                    [-10,  0,  0,  0,  0,  0,  0,-10],
                    [-10,  0,  5,  5,  5,  5,  0,-10],
                    [-5,  0,  5,  5,  5,  5,  0, -5],
                    [0,  0,  5,  5,  5,  5,  0, -5],
                    [-10,  5,  5,  5,  5,  5,  0,-10],
                    [-10,  0,  5,  0,  0,  0,  0,-10],
                    [-20,-10,-10, -5, -5,-10,-10,-20]],

            'K':  [[-30,-40,-40,-50,-50,-40,-40,-30],
                    [-30,-40,-40,-50,-50,-40,-40,-30],
                    [-30,-40,-40,-50,-50,-40,-40,-30],
                    [-30,-40,-40,-50,-50,-40,-40,-30],
                    [-20,-30,-30,-40,-40,-30,-30,-20],
                    [-10,-20,-20,-20,-20,-20,-20,-10],
                    [20, 20,  0,  0,  0,  0, 20, 20],
                    [20, 30, 10,  0,  0, 10, 30, 20]]
        }
chess = GameState()

class Node():
    def __init__(self, state):
        self.state = state
        self.action = ''
        self.children = []
        self.parent = None
        self.n = 0
        self.v = 0

def uct(curr_node, parent_node):
    if(curr_node.n == 0):
        return(float("inf"))
    return curr_node.v + 2*(sqrt(log(parent_node.n)/(curr_node.n)))

def getBestChildNode(curr_node):
    # Selection

    maxUct = 0 
    maxMove=curr_node.children[0]
    for i, child in enumerate(curr_node.children):
        uctVal = uct(curr_node.children[i], curr_node)
        if(uctVal > maxUct):
            maxUct = uctVal
            # maxChild = curr_node.children[i]
            maxMove = child                
            
    maxMove.n += 1
    return maxMove

def getChildNodes(curr_node):
    # Expansion
    moves = chess.findValidMoves()
    for move in moves:
        tempNode = Node() 
        tempNode.action = move 
        tempNode.parent = curr_node
        chess.makeMove(move)
        tempNode.state.board = chess.board
        evaluate(curr_node)
        chess.undoMove
        curr_node.children.append(tempNode)

def playRandom(curr_node):
    # Simulation

    count = 0
    while((not chess.stalemate) and (not chess.checkmate)):
        count += 1
        moves = chess.findValidMoves()
        move = random.choice(moves)
        chess.makeMove(move)

    # The AI plays as Black
    if chess.stalemate:
        pass
    elif not chess.whiteToPlay:
        curr_node.v += 100
    else:
        curr_node.v -= 100
        
    for _ in range(count):
        chess.undoMove

# def updateValue(curr_node, res):
def evaluate(curr_node):
    score = 0
    for i, rows in enumerate(curr_node.state.board):
        for j, pos in enumerate(rows):
            if pos[1] in pstPawn:
                if pos[0] == 'w':
                    score -= pstPawn[pos[1]][i][j]    # The bonus is deducted if it is favourable to white
                    score -= weights[pos[1]]
                else:
                    score -= pstPawn[pos[1]][i][j]    # Flipping the pstPawn so -
                    score += weights[pos[1]]
                
    curr_node.v = score

def AIMove(state):
    root = Node(state)
    if not state.whiteToPlay:
        root.state = state
        getChildNodes(root)
    bestmove= getBestChildNode(root)
    chess.makeMove(bestmove)
