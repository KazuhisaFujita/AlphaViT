#---------------------------------------
#Since : 2018/09/16
#Update: 2023/11/29
# -*- coding: utf-8 -*-
#---------------------------------------
import numpy as np
from ringbuffer import RingBuffer
from copy import deepcopy
from ctypes import *
import sys

# Load the shared library
lib = CDLL('./check_connect.so')

# Define return and argument types
lib.check_connect.restype = c_int
lib.check_connect.argtypes = [POINTER(c_int), c_int, c_int, c_int]

class Gomoku() :
    def __init__(self, xnum = 9, ynum = 9, connect = 5, black = 1, white = -1, k_boards = 1):
        self.xnum = xnum
        self.ynum = ynum
        self.black = black
        self.white = white
        self.k_boards = k_boards
        self.connect = connect

        self.winner = 0
        self.put_location = [0,0]

        self.Ini_board()

    def Ini_board(self):
        self.board = self.Create_board()
        self.current_player = self.black
        self.seq_boards = RingBuffer(self.k_boards)
        for i in range(self.k_boards):
            self.seq_boards.add(np.zeros((self.xnum, self.ynum)))
        self.seq_boards.add(deepcopy(self.board))

    def Create_board(self):
        return np.zeros((self.xnum, self.ynum))

    def Print_board(self):
        print("  ", end='')
        for i in range(self.xnum):
            print(str(i)+"|", end='')
        print("")

        for i in range(self.ynum):
            print(str(i)+"|", end='')
            for j in range(self.xnum):
                if self.board[j][i] == self.black:
                    print("o|", end='')
                elif self.board[j][i] == self.white:
                    print("x|", end='')
                else:
                    print(" |", end='')
            print("")


    def Can_put(self, b):
        return b == 0

    def Put(self, b, x, y, player):
        b[x][y] = player
        return b

    def Get_player(self):
        return deepcopy(self.player)

    def Get_board(self):
        return deepcopy(self.board)

    def Get_board_size(self):
        return (self.xnum, self.ynum)

    def Get_action_size(self):
        return self.xnum * self.ynum

    def Check_connection(self, b):
        # Convert 2D numpy array to 1D C array
        #c_array = board.ravel().astype(np.int32)
        b = b.astype(np.int32)
        ptr = b.ctypes.data_as(POINTER(c_int))

        # Call the C function
        result = lib.check_connect(ptr, b.shape[0], b.shape[1], self.connect)

        return result

    def Check_winner(self):
        b_black = np.where(self.board == self.black, 1, 0)
        if self.Check_connection(b_black) == 1:
            return self.black
        b_white = np.where(self.board == self.white, 1, 0)
        if self.Check_connection(b_white) == 1:
            return self.white
        return 0

    def Get_winner(self):
        return self.winner

    def Get_valid_moves(self):
        moves = np.argwhere(self.board == 0)
        return(moves)

    def Check_game_end(self):
        self.winner = self.Check_winner()
        if self.winner != 0:
            return(True)
        else:
            if np.size(self.Get_valid_moves()) == 0:
                return(True)
            else:
                return(False)

    def Get_states(self):
        temp_states = self.seq_boards.Get_buffer()
        states = []
        for i in range(self.k_boards):
            states.append(np.where(temp_states[i] == 1, 1, 0))
            states.append(np.where(temp_states[i] == -1, 1, 0))

        if self.current_player == 1:
            states.append(np.ones((self.xnum, self.ynum)))
        else:
            states.append(np.zeros((self.xnum, self.ynum)))

        return np.array(states)

    def Put_stone(self, action):
        if self.board[action[0]][action[1]] == 0:
            self.board[action[0]][action[1]] = self.current_player
        else:
            print("Error")
            sys.exit()

    def Play_action(self, action):
        self.Put_stone(action)
        self.current_player *= -1
        self.seq_boards.add(deepcopy(self.board))

    def Get_current_player(self):
        return self.current_player

if __name__ == '__main__':
    tc = Gomoku(3,3,3)

    tc.Print_board()

    while(1):
#        print(tc.Get_states())
        tc.Print_board()
        print(tc.Get_valid_moves())
        tc.Play_action(tc.Get_valid_moves()[0])
#        tc.Print_board()

        if tc.Check_game_end():
            winner = tc.Get_winner()
            print(winner)
            exit()
