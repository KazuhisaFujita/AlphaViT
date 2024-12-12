#---------------------------------------
#Since : 2018/09/16
#Update: 2023/12/06
# -*- coding: utf-8 -*-
#---------------------------------------
import numpy as np
from ringbuffer import RingBuffer
from copy import deepcopy
from ctypes import *
import sys

# Load the shared library
lib = CDLL('./check_valid.so')
lib_put = CDLL('./put_stone.so')

# Define return and argument types
lib.check_valid.restype = c_int
lib.check_valid.argtypes = [np.ctypeslib.ndpointer(dtype=np.int32, flags='C_CONTIGUOUS'), c_int, c_int, c_int, c_int, c_int]

# Define return and argument types
#lib_put.put_stone.argtypes = [POINTER(c_int), c_int, c_int, c_int, c_int, c_int]

class Othello():
    def __init__(self, xnum = 6, ynum = 6, connect = 0, black = 1, white = -1, k_boards = 1):
        self.xnum = xnum
        self.ynum = xnum
        self.num  = xnum

        self.black = black
        self.white = white
        self.k_boards = k_boards

        self.directions = np.array([[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]])

        self.Ini_board()

    def Ini_board(self):
        self.board          = self.Create_board()
        self.current_player = self.black
        self.seq_boards     = RingBuffer(self.k_boards)
        for i in range(self.k_boards):
            self.seq_boards.add(np.zeros((self.num, self.num)))
        self.seq_boards.add(deepcopy(self.board))

    def Create_board(self):
        b = np.zeros((self.num, self.num))
        b[self.num // 2 - 1][self.num // 2 - 1] = self.white
        b[self.num // 2    ][self.num // 2 -1]  = self.black
        b[self.num // 2 - 1][self.num // 2]     = self.black
        b[self.num // 2    ][self.num // 2]     = self.white
        return b

    def Print_board(self):
        print("  ", end='')
        for j in range(self.num):
            print(str(j)+"|", end='')
        print("")

        for i in range(self.num):
            print(str(i)+"|", end='')
            for j in range(self.num):
                if self.board[j][i] == self.white:
                    print("o|", end='')
                elif self.board[j][i] == self.black:
                    print("x|", end='')
                else:
                    print(" |", end='')
            print("")


    def Put(self, b, x, y, player):
        b[x][y] = player
        return b

    def Get_board(self):
        return deepcopy(self.board)

    def Get_board_size(self):
        return (self.num, self.num)

    def Get_action_size(self):
        return self.params.othello66_action_size

    def Get_winner(self):
        b = deepcopy(self.board)

        winner = None

        if self.Check_game_end():
            if np.sum(b) * self.white > 0:
                winner = self.white
            elif np.sum(b) * self.white < 0:
                winner = self.black
            else:
                winner = 0

        return winner

    def Get_valid_moves(self, p = None):
        b = deepcopy(self.board)

        if p == None:
            player = self.current_player
        else:
            player = p

        valid_moves = []
        moves = np.argwhere(b == 0)
        if np.size(moves) != 0:
            valid_flag = False
            for x, y in moves:
                valid = False

                b = b.astype(np.int32)

                if lib.check_valid(b, b.shape[0], b.shape[1], x, y, player) == 1:
                    valid = True

                if valid:
                    valid_moves.append([x, y])
                    valid_flag = True

            if valid_flag == False:
                valid_moves = [[self.num - 1, self.num]]

        else:
            valid_moves = [[self.num - 1, self.num]]

        return(valid_moves)

    def Check_game_end(self):
        b = deepcopy(self.board)

        if np.size(np.argwhere(b == 0)) == 0:
            return(True)
        elif np.size(np.argwhere(b == self.white)) == 0:
            return(True)
        elif np.size(np.argwhere(b == self.black)) == 0:
            return(True)
        elif self.Get_valid_moves(p = self.white)[0][1] == self.num and self.Get_valid_moves(p = self.black)[0][1] == self.num:
            return(True)
        else:
            return(False)

    def Put_stone(self, action):
        if action[1] != self.num:
            player = self.current_player
            x = action[0]
            y = action[1]

            b = self.board.astype(np.int32)
            lib_put.put_stone.argtypes = [np.ctypeslib.ndpointer(dtype=np.int32, flags='C_CONTIGUOUS'), c_int, c_int, c_int, c_int, c_int]
            lib_put.put_stone.restype = POINTER(c_int)
            output_ptr = lib_put.put_stone(b, b.shape[0], b.shape[1], x, y, player)
            output = np.ctypeslib.as_array(output_ptr, shape=(b.shape[0] * b.shape[1],))
            self.board = output.reshape(b.shape[0], b.shape[1])

    def Get_states(self):
        temp_states = self.seq_boards.Get_buffer()
        states = []
        for i in range(self.k_boards):
            states.append(np.where(temp_states[i] == self.white, 1, 0))
            states.append(np.where(temp_states[i] == self.black, 1, 0))

        if self.current_player == 1:
            states.append(np.ones((self.num, self.num)))
        else:
            states.append(np.zeros((self.num, self.num)))

        return np.array(states)

    def Play_action(self, action):
        self.Put_stone(action)
        self.current_player *= -1
        self.seq_boards.add(deepcopy(self.board))

    def Get_current_player(self):
        return self.current_player

if __name__ == '__main__':
    ot = Othello()

    # ot.board = np.array([
    #     [-1, -1, -1, -1, -1, -1],
    #     [-1, -1, -1, -1,  0,  0],
    #     [-1, -1, -1, -1, -1,  0],
    #     [-1, -1, -1, -1, -1,  1],
    #     [-1, -1, -1, -1, -1,  0],
    #     [-1,  0, -1, -1, -1, -1]])
    # ot.Print_board()
    # print(ot.Get_valid_moves())
    # print(ot.Get_winner())
    # print(ot.Check_game_end())


    ot = Othello()

    ot.Print_board()

    while(1):
#        print(ot.Get_states())
        print(ot.Get_valid_moves())
        ot.Play_action(ot.Get_valid_moves()[0])
        ot.Print_board()

        if ot.Check_game_end():
            winner = ot.Get_winner()
            print(winner)
            exit()
