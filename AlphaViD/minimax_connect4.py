#---------------------------------------
#Since : 2019/04/10
#Update: 2023/12/25
# -*- coding: utf-8 -*-
#---------------------------------------
import numpy as np
from copy import deepcopy
import random
import math
from Connect4 import Connect4
import time
from parameters_alphazero import Parameters
from ctypes import *

# Load the shared library
lib = CDLL('./check_connect_minimax.so')

# Define return and argument types
lib.check_connect_minimax.restype = c_int
lib.check_connect_minimax.argtypes = [POINTER(c_int), c_int, c_int, c_int]

class Node():
    def __init__(self, state, player, move = None, terminal = False, winner = 0, parent = None):
        self.p        = player
        self.move     = move
        self.state    = state
        self.children = []
        self.parent   = parent
        self.terminal = terminal
        self.winner   = winner
        self.value    = None

    def Get_state(self):
        return deepcopy(self.state)

    def Get_player(self):
        return deepcopy(self.p)

    def Add_child(self, state, player, move, terminal, winner):
        child = Node(state, player, move, terminal, winner, self)
        self.children.append(child)

class Minimax:
    def __init__(self, game):
        self.g = game
        self.p = self.g.current_player
        self.xnum = self.g.xnum
        self.ynum = self.g.ynum
        self.connect = self.g.connect
        self.red = self.g.red
        self.yellow = self.g.yellow
        self.k_boards = self.g.k_boards
        self.params = Parameters()

        self.root = Node(state = self.g.Get_board(), player = self.g.current_player)

        self.depth = 3 # the depth of a game tree

        self.base_reward = 100

    def Expand_node(self, node):
        temp_g = Connect4(xnum = self.xnum, ynum = self.ynum, connect = self.connect, red = self.red, yellow = self.yellow, k_boards = self.k_boards)
        temp_g.board = node.Get_state()
        temp_g.current_player = node.Get_player()
        valid_moves = temp_g.Get_valid_moves()
        for m in valid_moves:
            temp_g.Ini_board()
            temp_g.board = node.Get_state()
            temp_g.current_player = node.Get_player()
            temp_g.Play_action(m)
            player = temp_g.current_player
            terminal = temp_g.Check_game_end()
            winner = temp_g.Get_winner()
            state = temp_g.Get_board()
            node.Add_child(state, player, m, terminal, winner)

    def Make_tree(self, node, depth):
        depth -= 1
        if node.terminal != True and depth >= 0:
            self.Expand_node(node)
            for i in node.children:
                self.Make_tree(i, depth)

    def Run(self):
        node = self.root

        self.Make_tree(node, self.depth)

        return self.Search(self.root).move

    def Evaluate(self, s, p):
        # Extract the board position of the root node.
        b = np.where(s == p, 1, 0)
        ptr = b.ctypes.data_as(POINTER(c_int))
        # Caclurate the score of the board position of minimax player.
        v = lib.check_connect_minimax(ptr, b.shape[0], b.shape[1], self.params.connect - 1 ,self.base_reward)
        # Extract the board position of the opponent.
        b = np.where(s == -p, 1, 0)
        ptr = b.ctypes.data_as(POINTER(c_int))
        # Caclurate the score of the board position fo the opponent.
        # Subtract the opponent's score from the minimax player's score.'
        v -= lib.check_connect_minimax(ptr, b.shape[0], b.shape[1], self.params.connect - 1 ,self.base_reward)
        return v

    def Search(self, root):
        temp_g = Connect4(xnum = self.xnum, ynum = self.ynum, connect = self.connect, red = self.red, yellow = self.yellow, k_boards = self.k_boards)

        stack = [root] # the list to store the nodes

        while len(stack) != 0:
            n = stack.pop()

            if len(n.children) != 0:
                stack += n.children
            else:
                v = 0
                if n.terminal:
                    v = root.p * n.winner * 1000000 # the value when the node is a terminal node.
                else:
                    if len(n.children) == 0:
                        v = self.Evaluate(n.state, root.p)
                    else:
                        v = n.value

                # When the terminal node is in second nodes, v is None and Errot occur. This code avoid this problem.
                n.value = v

                while n.parent != None:
                    # Set the node to the parent node.
                    n = n.parent

                    if n.value == None:
                        n.value = v
                    elif n.p == root.p and n.value < v:
                        n.value = v
                    elif n.p != root.p and n.value > v:
                        n.value = v

        values = np.array([i.value for i in root.children])
        if not np.all(values == values[0]):
            return root.children[np.argmax(np.array([i.value for i in root.children]))]
        else:
            return root.children[np.random.randint(len(root.children))]
