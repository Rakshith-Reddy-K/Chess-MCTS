import copy
from node import Node 
import evaluation as eval
import chess
import numpy as np
import random
turn = None

def playMove(node:Node,move):
    curr_board = copy.deepcopy(node.board)
    move_str = curr_board.san(move)
    curr_board.push_san(move_str)
    return curr_board

def get_random_move(num_legal_moves,selected_childs):
    if num_legal_moves == 1:
        return 0
    random_move = random.randint(0,num_legal_moves-1)
    while selected_childs is not None and random_move in selected_childs:
        random_move = random.randint(0,num_legal_moves-1)
    
    return random_move

def select_node(node:Node):
    currentNode = node
    # if currentNode.parent is not None and currentNode.parent.isRoot():
    #     currentNode.expanded = True
    while currentNode.expanded:
        try:
            if len(currentNode.children) < len(currentNode.legal_moves):
                bestMove = get_random_move(len(currentNode.legal_moves), currentNode.children.keys())
            else:
                bestMove = currentNode.best_child()
            if bestMove not in currentNode.children:
                curr_board = playMove(currentNode,currentNode.legal_moves[bestMove])
                # curr_board = copy.deepcopy(currentNode.board)
                # move_str = curr_board.san(currentNode.legal_moves[bestMove])
                # curr_board.push_san(move_str)
                currentNode.children[bestMove] = Node(curr_board,bestMove,currentNode)
        except:
            break
        currentNode = currentNode.children[bestMove]
    return currentNode

def expand(node:Node):
    global turn
    
    if node.board.is_game_over():
        return (node,eval.getScore(node.board,turn))
    # all_legal_moves = node.legal_moves
    # max_score = float('-inf')
    # best_move = None
    # board = None
    # pov = -1 if node.board.turn is chess.BLACK else 1
    # for i in range(0,len(all_legal_moves)):
    #     new_board = playMove(node,all_legal_moves[i])
    #     score = eval.getScore(new_board,node.board.turn)
    #     if score > max_score:
    #         max_score = score
    #         best_move = i
    #         board = new_board
    
    # node.children[best_move] = Node(board,best_move,node)
    # return (node.children[best_move],max_score)
    random_move = get_random_move(len(node.legal_moves),node.children.keys())
    new_board = playMove(node,node.legal_moves[random_move])
    node.children[random_move] = Node(new_board,random_move,node)
    max_score = eval.getScore(new_board,turn)

    return (node.children[random_move],max_score)

def rollout(node:Node):
    
    if(node.board.is_game_over()):
        board = node.board
        if(board.result()=='1-0'):
            #print("h1")
            return (node,3)
        elif(board.result()=='0-1'):
            #print("h2")
            return (node,-3)
        else:
            return (node,1.5)

    # for i in range(0,len(node.legal_moves)):
    #     if i not in node.children.keys():
    #         curr_board = copy.deepcopy(node.board)
    #         move_str = curr_board.san(node.legal_moves[i])
    #         curr_board.push_san(move_str)
    #         node.children[i] = Node(curr_board,i,node)
    rnd_state = get_random_move(len(node.legal_moves),node.children.keys())
    curr_board = copy.deepcopy(node.board)
    move_str = curr_board.san(node.legal_moves[rnd_state])
    curr_board.push_san(move_str)
    node.children[rnd_state] = Node(curr_board,rnd_state,node)
    return rollout(node.children[rnd_state])
# def expandAndRollout(node:Node,depth):
#     if node.board.is_game_over():
#         if(node.board.result()=='1-0'):
#             #print("h1")
#             return (node,10)
#         elif(node.board.result()=='0-1'):
#             #print("h2")
#             return (node,-10)
#         else:
#             return (node,5)
#     if depth > 5:
#         score = eval.getScore(node.board,turn)
#         if score >= 3:
#             return (node,10)
#         elif score <= -3:
#             return (node,-10)
#         else:
#             return (node,score/4)
#     random_move = random.randint(0,len(node.legal_moves)-1)
#     new_board = playMove(node,node.legal_moves[random_move])
#     node.children[random_move] = Node(new_board,random_move,node)
#     return expandAndRollout(node.children[random_move],depth+1)

def backup(node:Node,score):
    global turn
    current_node = node
    while current_node is not None and current_node.parent is not None :
        current_node.number_visits +=1
        if current_node.parent.board.turn == turn:
            if score < 0:
                current_node.total_value += 2 * score
            else:
                current_node.total_value += score
        else:
            if score < 0:
                current_node.total_value -= 2 * score
            else:
                current_node.total_value -= score

        current_node.expanded = True
        current_node = current_node.parent 
        

def visit_all_children(root:Node):
    global turn
    all_legal_moves = root.legal_moves
    for i in range(0,len(all_legal_moves)):
        new_board = playMove(root,all_legal_moves[i])
        score = eval.getScore(new_board,turn)
        root.children[i] = Node(new_board,i,root)
        backup(root.children[i],score)

def totalNodes(node:Node):
    if len(node.children) == 0:
        return 0
    v = np.zeros(len(node.children))
    i=0
    for key,value in node.children.items():
        v[i] = 1+ totalNodes(value)
        print(node.legal_moves[key] , " --Rewards " , node.children_values[key] , " -- Visists " , node.children_number_visits[key] )
        i=i+1
    return np.sum(v)

def predictNextMove(board:chess.Board,simulations = 500):
    global turn 
    root = Node(board,None)
    turn = board.turn
    root.expanded = True
    visit_all_children(root)
    # for key,value in root.children.items():
    #         print(root.legal_moves[key] , " --Rewards " , root.children_values[key] , " -- Visists " , root.children_number_visits[key])

    for _ in range(simulations):
        selected_node = select_node(root)
        leaf , reward = expand(selected_node)
        # expanded_node,_ = expand(selected_node)
        # leaf,reward = rollout(expanded_node)
        if turn != selected_node.board.turn:
            reward *= -1
        backup(leaf,reward)
    # for key,value in root.children.items():
    #         print(root.legal_moves[key] , " --Rewards " , root.children_values[key] , " -- Visists " , root.children_number_visits[key])

    return root.legal_moves[np.argmax(root.children_avg_rewards())]
