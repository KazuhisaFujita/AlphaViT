#---------------------------------------
#Since : 2019/04/25
#Update: 2024/12/01
# -*- coding: utf-8 -*-
#---------------------------------------
import math
import torch
import numpy as np

class Parameters:
    def __init__(self):
        #------------------------
        # AlphaVDM

        # parameters for parallel processing
        self.num_processes_training = 10 # the number of parallelized processes of training of AlphaZero
        self.num_processes_test     = 10 # the number of parallelized processes of test games
        self.devices                = ['cuda:0', 'cuda:1', 'cuda:2', 'cuda:0', 'cuda:1', 'cuda:2', 'cuda:0', 'cuda:1', 'cuda:2', 'cuda:0', 'cuda:1', 'cuda:2'] # used devices

        self.num_iterations = 3000 # the number of iterations
        self.num_games      = {"Gomoku": 10, "Gomoku77": 10, "Gomoku66": 10, "Othello": 10,
                                   "Othello66": 10, "Connect4": 30, "Connect4_65": 30, "Connect4_54": 30, "TicTacToe": 50} # the number of games

        # AlphaZero plays games with the other AI agent every checkpoint_interval to test the strength of AlphaZero.
        self.checkpoint_interval = 20
        self.num_test            = 10 # the number of games in test play


        #MCTS
        # the number of MCTS simulations
        self.num_mcts_sims      = {"Gomoku": 400, "Gomoku77": 400, "Gomoku66": 200,
                                   "Othello": 400, "Othello66": 200,
                                   "Connect4": 200, "Connect4_65": 200, "Connect4_54": 200, "TicTacToe": 100}
        # the opening of a game for training
        self.game_opening_train = {"Gomoku": 8, "Gomoku77": 7, "Gomoku66": 6,
                                   "Othello": 8, "Othello66": 6,
                                   "Connect4": 4, "Connect4_65": 4, "Connect4_54": 4, "TicTacToe": 1}
        # temparature for training
        self.game_temp          = {"Gomoku": 40, "Gomoku77": 40, "Gomoku66": 20,
                                   "Othello": 80, "Othello66": 40,
                                   "Connect4": 100, "Connect4_65": 100, "Connect4_54": 100, "TicTacToe": 50}

        self.opening_test  = 0          # the opening of a game for test
        self.opening       = 0          # the opening of a game
        self.cpuct         = 1.25       # the exploration rate
        self.Temp          = 10         # the temperature parameter of softmax function for calculating the move probability
        self.rnd_rate      = 0.2        # the probability to select a move at random

        #Neural Network
        self.input_size        = 100000 # the number of inputs

        self.epochs            = 1    # the number of epochs every iteration
        self.batch_size        = 1024 # the size of the mini batch
        self.num_batch         = math.ceil(self.input_size/self.batch_size)
        self.lam               = 1e-4 # learning rate
        #self.weight_decay      = 1e-4 # weight decay
        #self.momentum          = 0.9  # momentum

        self.k_boards          = 1      # the number of board states in one input
        self.input_channels    = (self.k_boards * 2) + 1 # the number of channels of an input

        self.pos_size          = 16

        self.patch_size        = 5    # patch size, it can be regarded as filter size.
        self.stride_size       = 1    # stride size
        self.emb_size          = 512  # embedding size
        self.num_layers        = 1    # the number of transformer encoder layer
        self.num_heads         = 8
        self.dim_feedforward   = self.emb_size*2

        self.num_value_hidden  = self.emb_size # the number of hidden units of the value head
        self.num_policy_hidden = self.emb_size # the number of hidden units of the policy head

        self.decoder_emb_size          = self.emb_size  # embedding size
        self.decoder_token_size        = 256
        self.decoder_num_layers        = 1 # the number of transformer encoder layer
        self.decoder_num_heads         = self.num_heads
        self.decoder_dim_feedforward   = self.decoder_emb_size*2

        self.dropout = 0.1

        #---------------------------------
        #Game settings
        self.games     = ["Connect4", "Gomoku", "Othello"]#["Connect4", "Gomoku", "Othello", "Gomoku77", "Othello66"]
        games          = ["Connect4", "Connect4_65", "Connect4_54", "Gomoku", "Gomoku77", "Gomoku66", "Othello", "Othello66", "TicTacToe"]
        self.board_x   = {"Connect4": 7, "Connect4_65": 6, "Connect4_54": 5, "Gomoku": 9, "Gomoku77": 7, "Gomoku66": 6, "Othello": 8, "Othello66": 6, "TicTacToe": 3}
        self.board_y   = {"Connect4": 6, "Connect4_65": 5, "Connect4_54": 4, "Gomoku": 9, "Gomoku77": 7, "Gomoku66": 6, "Othello": 8, "Othello66": 6, "TicTacToe": 3}
        self.connect   = {"Connect4": 4, "Connect4_65": 4, "Connect4_54": 4, "Gomoku": 5, "Gomoku77": 5, "Gomoku66": 5, "Othello": 0, "Othello66": 0, "TicTacToe": 3}
        self.Opponents = {"Connect4":"Opp_Connect4", "Connect4_65":"Opp_Connect4", "Connect4_54":"Opp_Connect4", "Gomoku":"Opp_Gomoku", "Gomoku77":"Opp_Gomoku", "Gomoku66":"Opp_Gomoku", "Othello":"Opp_Othello", "Othello66":"Opp_Othello66", "TicTacToe":"Opp_Gomoku"}
        self.action_size = {}
        self.game_token = {}
        for g in games:

            token = torch.zeros((1,1,self.emb_size))
            if g == "Connect4" or g == "Connect4_65" or g == "Connect4_54":
                token[0][0][0] = 1
                self.action_size[g] = self.board_x[g]
            elif g == "Gomoku" or g == "Gomoku77" or g == "Gomoku66":
                token[0][0][2] = 1
                self.action_size[g] = self.board_x[g] * self.board_y[g]
            elif g == "Othello" or g == "Othello66":
                token[0][0][1] = 1
                self.action_size[g] = self.board_x[g] * self.board_y[g] + 1
            elif g == "TicTacToe":
                token[0][0][3] = 1
                self.action_size[g] = self.board_x[g] * self.board_y[g]

            self.game_token[g] = token

        self.black  =  1         # stone color of the first player. For Connect4, black is regareded as red.
        self.white  = -1         # stone color of the second player. For Connect4, white is regareded as yellow.

        first_part = np.arange(0, 101, 1)
        second_part = np.arange(100, self.num_iterations+1, 5)
        self.savepoint_intervals = np.concatenate((first_part, second_part[1:])) # second_part[1:] to avoid repeating 100
