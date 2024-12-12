#---------------------------------------
#Since : 2019/04/23
#Update: 2024/09/17
# -*- coding: utf-8 -*-
#---------------------------------------
import numpy as np
from Gomoku import Gomoku
from Othello_bitboard import Othello
from Othello66 import Othello as Othello66
from Connect4 import Connect4
from AlphaViT_mcts import A_MCTS
from collections import deque
from nn_alphavit import NNetWrapper
from parameters_alphavit import Parameters
from classical_MCTS_connect4 import MCTS as MCTS_Connect4
from classical_MCTS_gomoku import MCTS as MCTS_Gomoku
#from minimax_gomoku import Minimax as Minimax_Gomoku
from minimax_othello import Minimax as Minimax_Othello
from minimax_othello66 import Minimax as Minimax_Othello66
from copy import deepcopy
from player import Random_player
from ringbuffer import RingBuffer
import time
import multiprocessing as mp
import math
import random

class Train():
    def __init__(self):
        self.params = Parameters()
        self.comp_time = 0
        self.net    = NNetWrapper(params = self.params)
        self.games = self.params.games

        # Set the weight from the trained DNN at N iterations.
        #self.net.load_checkpoint(280)
        self.start = 2001
        if self.start != 1:
            self.net.load_checkpoint(self.start - 1)

    def Make_schedule(self, num, players, game):
        num_players = len(players)
        schedule = []
        if players[0] == players[1] and len(players) == 2:
            for n in range(num):
                schedule.append([players[0], players[1], game])
        else:
            for n in range(num//2):
                for i in range(num_players):
                    for j in range(num_players):
                        if i != j:
                            schedule.append([players[i], players[j], game])

        return schedule

    def AlphaZero(self, g, game_name, count):
        amcts = A_MCTS(game = g, game_name = game_name, net = self.net, params = self.params)
        amcts.num_moves = count
        action = amcts.Run()
        prob = amcts.Get_prob()
        return action, prob

    def Opp_Connect4(self, g):
        mm = MCTS_Connect4(g)
        action = mm.Run()
        return action

    def Opp_Gomoku(self, g):
        mm = MCTS_Gomoku(g)
        action = mm.Run()
        return action

    def Opp_Othello(self, g):
        mm = Minimax_Othello(g)
        action = mm.Run()
        return action

    def Opp_Othello66(self, g):
        mm = Minimax_Othello66(g)
        action = mm.Run()
        return action

    def Action(self, g, game_name, count = 0, player = "alphazero"):
        if player == "alphazero":
            action, prob = self.AlphaZero(g, game_name, count)
            return action, prob
        elif player == "Opp_Connect4":
            action = self.Opp_Connect4(g)
            return action
        elif player == "Opp_Gomoku":
            action = self.Opp_Gomoku(g)
            return action
        elif player == "Opp_Othello":
            action = self.Opp_Othello(g)
            return action
        elif player == "Opp_Othello66":
            action = self.Opp_Othello66(g)
            return action

    def Run(self):
        # Start training.
        mp.set_start_method('spawn')

        # Make buffers to store the training data.
        buf_board = {}
        buf_prob = {}
        buf_v = {}

        for game_name in self.games:
             buf_board[game_name]= RingBuffer(self.params.input_size)
             buf_prob[game_name] = RingBuffer(self.params.input_size)
             buf_v[game_name]    = RingBuffer(self.params.input_size)

        #--------------------
        # Make the initial dataset
        print("Read datasets")

        for game_name in self.params.games:
            buf_board[game_name]= RingBuffer(self.params.input_size)
            buf_prob[game_name] = RingBuffer(self.params.input_size)
            buf_v[game_name]    = RingBuffer(self.params.input_size)


            if self.start == 1:
                boards = np.load("datasets/"+game_name+"_boards.npy")
                probs  = np.load("datasets/"+game_name+"_probs.npy")
                vs     = np.load("datasets/"+game_name+"_vs.npy")
            else:
                boards = np.load("datasets/"+game_name+"_boards_"+str(self.start-1)+".npy")
                probs  = np.load("datasets/"+game_name+"_probs_"+str(self.start-1)+".npy")
                vs     = np.load("datasets/"+game_name+"_vs_"+str(self.start-1)+".npy")

            for i in range(self.params.input_size):
                buf_board[game_name].add(boards[i])
                buf_v[game_name].add(vs[i])
                buf_prob[game_name].add(probs[i])

        #------------------
        # Training
        print("Training")

        # The first training using the prepared datasets
        self.Learning(buf_board, buf_prob, buf_v, self.start, self.games)

        # training with self-play
        schedule = []
        for game_name in self.games:
             # Make the schedule for training.
             schedule.extend(self.Make_schedule(self.params.num_games[game_name], ["alphazero", "alphazero"], game_name))

        schedule_list = [schedule[i::self.params.num_processes_training] for i in range(self.params.num_processes_training)]

        for i in range(self.start + 1, self.params.num_iterations+1):
            start = time.time()
            training_board, training_prob, training_v = self.generate_dataset(schedule_list)

            #random.shuffle(self.games)
            for game_name in self.games:
                # Augment the data obtained in self-play.
                if game_name == "Connect4" or game_name == "Connect4_65" or game_name == "Connect4_54":
                    temp_board, temp_prob, temp_v = self.Augment_data_connect4(training_board[game_name], training_prob[game_name], training_v[game_name],
                                                                      self.params.board_x[game_name], self.params.board_y[game_name])
                else:
                    temp_board, temp_prob, temp_v = self.Augment_data(training_board[game_name], training_prob[game_name], training_v[game_name],
                                                                      self.params.board_x[game_name], self.params.board_y[game_name])

                # Add the augmented data to the input buffers.
                for j in range(len(temp_board)):
                    buf_board[game_name].add(temp_board[j])
                    buf_prob[game_name].add(temp_prob[j])
                    buf_v[game_name].add(temp_v[j])

            # Train the DNN.
            self.Learning(buf_board, buf_prob, buf_v, i, self.games)

            #Calculate computation time.
            self.comp_time = time.time() - start

            # Test the trained AlphaZero.
            if i%self.params.checkpoint_interval == 0:
                print(i, "total loss:", self.net.total_loss, "p loss:", self.net.lo_pi, "v loss:", self.net.lo_v, "time:", self.comp_time)
                self.test(i)

                for game_name in self.games:
                    np.save("datasets/"+game_name+"_boards_"+str(i)+".npy", np.array(buf_board[game_name].Get_buffer_start_end()))
                    np.save("datasets/"+game_name+"_probs_"+str(i)+".npy",  np.array(buf_prob[game_name].Get_buffer_start_end()))
                    np.save("datasets/"+game_name+"_vs_"+str(i)+".npy",     np.array(buf_v[game_name].Get_buffer_start_end()))

    def generate_dataset(self, schedule_list):
        # Set the devices.
        devices = self.params.devices

        # Initialize the lists to store boards, probabilities, and values obtained in self-play.
        training_board = {}
        training_prob  = {}
        training_v     = {}

        for game_name in self.games:
            training_board[game_name]= []
            training_prob[game_name] = []
            training_v[game_name]    = np.empty(0)

        # Start self-play.
        pool    = mp.Pool(self.params.num_processes_training)
        results = [pool.apply_async(self.self_play, args=(devices[i], schedule_list[i],)) for i in range(self.params.num_processes_training)]
        output  = [p.get() for p in results]
        pool.close()
        pool.join()

        # Add the data obtained in self-play to the lists.
        for j in range(self.params.num_processes_training):
            for k in range(len(output[j][0])):
                training_board[output[j][0][k]].append(output[j][1][k])
                training_prob[output[j][0][k]].append(output[j][2][k])
                training_v[output[j][0][k]] = np.append(training_v[output[j][0][k]], output[j][3][k])

        # Augment the data obtained in self-play.
        return training_board, training_prob, training_v

    def self_play(self, device, schedule):
        self.net.device = device

        games = []
        board_data = []
        prob_actions = []
        v_data = np.empty(0)

        for i in range(len(schedule)):
            p = schedule[i][0:2]
            game = schedule[i][2]

            if game == "Connect4" or game == "Connect4_65" or game == "Connect4_54":
                g =  Connect4(self.params.board_x[game], self.params.board_y[game], self.params.connect[game],
                                self.params.black, self.params.white, self.params.k_boards)
            elif game == "Gomoku" or game == "Gomoku77" or game == "Gomoku66" or game == "TicTacToe":
                g =  Gomoku(self.params.board_x[game], self.params.board_y[game], self.params.connect[game],
                                self.params.black, self.params.white, self.params.k_boards)
            elif game == "Othello":
                g =  Othello(self.params.board_x[game], self.params.board_y[game], self.params.connect[game],
                                self.params.black, self.params.white, self.params.k_boards)
            elif game == "Othello66":
                g =  Othello66(self.params.board_x[game], self.params.board_y[game], self.params.connect[game],
                                self.params.black, self.params.white, self.params.k_boards)
            else:
                print("Error")

            self.params.opening = self.params.game_opening_train[game]
            self.params.Temp = self.params.game_temp[game]

            temp_v_data = np.empty(0)

            winner = 0
            g.Ini_board()

            count = 0
            while True:
                count += 1

                games.append(game)
                board_data.append(g.Get_states())
                temp_v_data = np.append(temp_v_data, 1)
                action, prob = self.Action(g = g, game_name = game, count = count, player = p[(count - 1)%2])
                g.Play_action(action)
                prob_actions.append(prob)

                if g.Check_game_end():
                    winner = g.Get_winner()
                    break

            temp_v_data *= winner
            v_data = np.append(v_data, temp_v_data)

        return(games, board_data, prob_actions, v_data)

    def Learning(self, training_board, training_prob, training_v, i, games):
        self.net.device = 'cuda'
        self.net.train(training_board, training_prob, training_v, games)

        if i in self.params.savepoint_intervals:
            self.net.save_checkpoint(i)

    def Augment_data(self, training_board, training_prob, training_v, W, H):
        aug_training_board = deepcopy(training_board)
        aug_training_prob = deepcopy(training_prob)
        aug_training_v = deepcopy(training_v)

        for i in range(len(training_board)):
            board = training_board[i]
            prob = training_prob[i]

            # flip
            flip_board = np.zeros((self.params.k_boards * 2 + 1, W, H))
            for j in range(board.shape[0]):
                flip_board[j] = np.flip(board[j], axis=0)
            aug_training_board.append(flip_board)

            flip_prob = prob
            prob_none = flip_prob[-1]
            flip_prob = np.delete(flip_prob, -1)
            flip_prob = np.flip(flip_prob.reshape((W, H)), axis = 0).reshape(W*H)
            flip_prob = np.insert(flip_prob, flip_prob.size, prob_none)
            aug_training_prob.append(flip_prob)
            aug_training_v = np.append(aug_training_v, training_v[i])

            for _ in range(3):
                # rot90
                rot_board = np.zeros((self.params.k_boards * 2 + 1, W, H))
                for j in range(board.shape[0]):
                    rot_board[j] = np.rot90(board[j])
                board = rot_board
                aug_training_board.append(rot_board)

                rot_prob = prob
                prob_none = rot_prob[-1]
                rot_prob = np.delete(rot_prob, -1)
                rot_prob = np.rot90(rot_prob.reshape((W, H))).reshape(W*H)
                rot_prob = np.insert(rot_prob, rot_prob.size, prob_none)
                prob = rot_prob
                aug_training_prob.append(rot_prob)
                aug_training_v = np.append(aug_training_v, training_v[i])

                # flip
                flip_board = np.zeros((self.params.k_boards * 2 + 1, W, H))
                for j in range(board.shape[0]):
                    flip_board[j] = np.flip(board[j], axis=0)
                aug_training_board.append(flip_board)

                flip_prob = prob
                prob_none = flip_prob[-1]
                flip_prob = np.delete(flip_prob, -1)
                flip_prob = np.flip(flip_prob.reshape((W, H)), axis = 0).reshape(W*H)
                flip_prob = np.insert(flip_prob, flip_prob.size, prob_none)
                aug_training_prob.append(flip_prob)
                aug_training_v = np.append(aug_training_v, training_v[i])

        return aug_training_board, aug_training_prob, aug_training_v

    def Augment_data_connect4(self, training_board, training_prob, training_v, W, H):
        # Augmentation

        aug_training_board = deepcopy(training_board)
        aug_training_prob = deepcopy(training_prob)
        aug_training_v = deepcopy(training_v)

        for i in range(len(training_board)):
            board = training_board[i]
            prob = training_prob[i]

            flip_board = np.zeros((self.params.k_boards * 2 + 1, W, H))
            for j in range(board.shape[0]):
                flip_board[j] = np.flip(board[j], axis=0)
            aug_training_board.append(flip_board)

            flip_prob = prob
            prob_none = flip_prob[-1]
            flip_prob = np.delete(flip_prob, -1)
            flip_prob = np.flip(flip_prob.reshape((W, H)), axis = 0).reshape(W*H)
            flip_prob = np.insert(flip_prob, flip_prob.size, prob_none)
            aug_training_prob.append(flip_prob)

            aug_training_v = np.append(aug_training_v, training_v[i])

        return aug_training_board, aug_training_prob, aug_training_v

    def test(self, i):
        self.params.opening = self.params.opening_test

        num_win_alpha = {}
        num_win_opp = {}
        schedule = []

        for game in self.games:
            opponent = self.params.Opponents[game]

            schedule.extend(self.Make_schedule(self.params.num_test, ["alphazero", opponent], game))

            num_win_alpha[game] = 0
            num_win_opp[game]   = 0

        schedule_list = [schedule[i::self.params.num_processes_test] for i in range(self.params.num_processes_test)]

        devices = self.params.devices
        pool = mp.Pool(self.params.num_processes_test)
        results = [pool.apply_async(self.arena_test, args=(devices[i],schedule_list[i], )) for i in range(self.params.num_processes_test)]
        output = [p.get() for p in results]
        pool.close()
        pool.join()


        for j in range(self.params.num_processes_test):
            for k in range(len(output[j][0])):
                num_win_alpha[output[j][0][k]] += output[j][1][k]
                num_win_opp[output[j][0][k]]   += output[j][2][k]

        for game in self.games:
            print(i, game, "win:", num_win_alpha[game]/self.params.num_test, "lose:",  num_win_opp[game]/self.params.num_test, "draw", (self.params.num_test - num_win_alpha[game] - num_win_opp[game])/self.params.num_test)

    def arena_test(self, device, schedule):
        self.net.device = device

        win_alpha = np.empty(0)
        win_opp = np.empty(0)
        games = []

        for i in range(len(schedule)):
            p = schedule[i][0:2]
            game = schedule[i][2]

            if game == "Connect4" or game == "Connect4_65" or game == "Connect4_54":
                g =  Connect4(self.params.board_x[game], self.params.board_y[game], self.params.connect[game],
                                self.params.black, self.params.white, self.params.k_boards)
            elif game == "Gomoku" or game == "Gomoku77" or game == "Gomoku66" or game == "TicTacToe":
                g =  Gomoku(self.params.board_x[game], self.params.board_y[game], self.params.connect[game],
                                self.params.black, self.params.white, self.params.k_boards)
            elif game == "Othello":
                g =  Othello(self.params.board_x[game], self.params.board_y[game], self.params.connect[game],
                                self.params.black, self.params.white, self.params.k_boards)
            elif game == "Othello66":
                g =  Othello66(self.params.board_x[game], self.params.board_y[game], self.params.connect[game],
                                self.params.black, self.params.white, self.params.k_boards)
            else:
                print("Error")

            g.Ini_board()

            count = 0
            while True:
                count += 1

                if p[(count - 1)%2] == "alphazero":
                    action, _ = self.Action(g = g, count = count, player = p[(count - 1)%2], game_name = game)
                else:
                    action = self.Action(g = g, count = count, player = p[(count - 1)%2], game_name = game)

                g.Play_action(action)

                if g.Check_game_end():
                    winner = g.Get_winner()
                    if winner == self.params.black:
                        if p[0] == "alphazero":
                            games.append(game)
                            win_alpha = np.append(win_alpha, 1)
                            win_opp = np.append(win_opp, 0)
                        else:
                            games.append(game)
                            win_alpha = np.append(win_alpha, 0)
                            win_opp = np.append(win_opp, 1)
                    if winner == self.params.white:
                        if p[1] == "alphazero":
                            games.append(game)
                            win_alpha = np.append(win_alpha, 1)
                            win_opp = np.append(win_opp, 0)
                        else:
                            games.append(game)
                            win_alpha = np.append(win_alpha, 0)
                            win_opp = np.append(win_opp, 1)
                    break

        return(games, win_alpha, win_opp)

if __name__ == '__main__':
    tr = Train()
    tr.Run()
