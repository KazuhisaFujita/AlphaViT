#---------------------------------------
#Since : 2019/04/10
#Update: 2023/12/08
# -*- coding: utf-8 -*-
#---------------------------------------
import numpy as np
from copy import deepcopy
import random
import math
from Othello_bitboard import Othello
import time

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
        self.num = self.g.num
        self.k_boards = self.g.k_boards
        self.black = self.g.black
        self.white = self.g.white

        self.p = self.g.current_player

        self.root = Node(state = self.g.Get_board(), player = self.g.current_player)

        self.depth = 3
        self.th = 6

        if self.num == 8:
            self.values = np.array([
                [120, -20,  20,   5,   5,  20, -20, 120],
                [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
                [ 20,  -5,  15,   3,   3,  15,  -5,  20],
                [  5,  -5,   3,   3,   3,   3,  -5,   5],
                [  5,  -5,   3,   3,   3,   3,  -5,   5],
                [ 20,  -5,  15,   3,   3,  15,  -5,  20],
                [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
                [120, -20,  20,   5,   5,  20, -20, 120],
                ])
        elif self.num == 6:
            self.values = np.array([
                [30,  -5,   2,   2,  -5, 30],
                [-5, -15,   3,   3, -15, -5],
                [ 2,   3,   0,   0,   3,  2],
                [ 2,   3,   0,   0,   3,  2],
                [-5, -15,   3,   3, -15, -5],
                [30,  -5,   2,   2,  -5, 30],
                ])

    def Expand_node(self, node):
        temp_g = Othello(self.num, self.num, 0, self.black, self.white, self.k_boards)
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
        if np.argwhere(node.state == 0).shape[0] <= self.th:
            self.depth = self.th

        self.Make_tree(node, self.depth)

        return self.Search(self.root).move

    def Search(self, root):
        temp_g = Othello(self.num, self.num, 0, self.black, self.white, self.k_boards)
        stack = [root]

        while len(stack) != 0:
            n = stack.pop()
            if len(n.children) != 0:
                stack += n.children
            else:
                v = 0
                if n.terminal:
                    v = n.winner * root.p * 1000
                else:
                    if len(n.children) == 0:
                        v = np.sum(self.values.reshape(self.num*self.num)[n.state.reshape(self.num*self.num) == root.p]) \
                          - np.sum(self.values.reshape(self.num*self.num)[n.state.reshape(self.num*self.num) == (- root.p)])
                    else:
                        v = n.value

                n.value = v # When the terminal node is in second nodes, v is None and Errot occur. This code avoid this problem.
                while n.parent != None:
                    n = n.parent
                    if n.value == None:
                        n.value = v
                    elif n.p == root.p and n.value < v:
                        n.value = v
                    elif n.p != root.p and n.value > v:
                        n.value = v

        values = np.array([i.value for i in root.children])
        max_value = np.max(values)
        max_children = np.where(values == max_value)[0]
        selected_child = np.random.choice(max_children)

        return root.children[selected_child]
