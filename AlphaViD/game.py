#---------------------------------------
#Since : 2019/04/10
#Update: 2023/11/29
# -*- coding: utf-8 -*-
#---------------------------------------
import numpy as np
from Gomoku import Gomoku
from Connect4 import Connect4
from Othello_bitboard import Othello
from Othello66 import Othello as Othello66
from player import Random_player
from classical_MCTS_connect4 import MCTS as MCTS_Connect4
from minimax_gomoku import Minimax as Minimax_Gomoku
from minimax_othello import Minimax as Minimax_Othello
import time
#from parameters_alphazero import Parameters as AZ_Parameters
#from AlphaZero_mcts import A_MCTS as AZ_MCTS
#from nn_alphazero   import NNetWrapper as AZ_NNetWrapper
from parameters_alphavit import Parameters as AV_Parameters
from AlphaViT_mcts import A_MCTS as AV_MCTS
from nn_alphavit   import NNetWrapper as AV_NNetWrapper

if __name__ == '__main__':
    win_alpha = 0
    win_mcts = 0
    win_rand = 0
    win_mm = 0

    # az_params = AZ_Parameters()
    # az_net  = AZ_NNetWrapper()
    # az_net.load_model("alphazero.model")
    # az_net.device = "cuda"

    av_params = AV_Parameters()
    av_net  = AV_NNetWrapper()
#    av_net.load_model("alphavit.model")
    av_net.device = "cuda"

    game = "Othello66"#"Othello66"#"Othello"#"Gomoku"#"Connect4"

    for i in range(1,2):
        if game == "Gomoku":
            g = Gomoku(9,9,5,1,-1,1)#Othello()#Connect4()#Gomoku()
        elif game == "Gomoku77":
            g = Gomoku(7,7,5,1,-1,1)#Othello()#Connect4()#Gomoku()
        elif game == "TicTacToe":
            g = Gomoku(3,3,3,1,-1,1)#Othello()#Connect4()#Gomoku()
        elif game == "Othello":
            g = Othello(8,1,-1,1)#Othello()#Connect4()#Gomoku()
        elif game == "Othello66":
            g = Othello66(6,1,-1,1)#Othello()#Connect4()#Gomoku()
        elif game == "Connect4":
            g = Connect4(7,6,4,1,-1,1)#Othello()#Connect4()#Gomoku()

        count = 0

        while(1):
            g.Print_board()

            # count += 1
            # #print(g.Get_valid_moves())
            # action = list(map(int, input().split(",")))
            # print(action)
            # g.Play_action(action)
            # g.Print_board()
            # if g.Check_game_end():
            #     winner = g.Get_winner()
            #     print(winner)
            #     break
            #     #exit()

            # count += 1
            # print("Minimax")
            # start = time.time()
            # mm = Minimax(g)
            # action = mm.Run()
            # print(action)
            # g.Play_action(action)
            # g.Print_board()
            # print("time:", time.time() - start)
            # if g.Check_game_end():
            #     winner = g.Get_winner()
            #     print(winner)
            #     if winner == 1:
            #         win_alpha += 1
            #     if winner == -1:
            #         win_mm += 1
            #     #exit()
            #     break

            # count += 1
            # print("AlphaZero")
            # start = time.time()
            # #print(g.Get_valid_moves())
            # az_amcts = AZ_MCTS(game = g, net = az_net)
            # az_amcts.params.Temp = 10
            # az_amcts.num_moves = count
            # action = az_amcts.Run()
            # print(action)
            # g.Play_action(action)
            # g.Print_board()
            # print("time:", time.time() - start)
            # if g.Check_game_end():
            #     winner = g.Get_winner()
            #     print(winner)
            #     if winner == 1:
            #         win_alpha += 1
            #     if winner == -1:
            #         win_mm += 1
            #     #exit()
            #     break

            count += 1
            print(count)
            print("AlphaViT")
            start = time.time()
            #print(g.Get_valid_moves())
            amcts = AV_MCTS(game = g, game_name = game, net = av_net)
            amcts.params.Temp = 10
            amcts.num_moves = count
            action = amcts.Run()
            print(action)
            g.Play_action(action)
            g.Print_board()
            print("time:", time.time() - start)
            winner = g.Get_winner()
            print(winner)
            if g.Check_game_end():
                winner = g.Get_winner()
                print(winner)
                if winner == 1:
                    win_alpha += 1
                if winner == -1:
                    win_mm += 1
                #exit()
                break


            # print("MCTS")
            # start = time.time()
            # mcts = MCTS(g)
            # mcts.num_sim = 300
            # action = mcts.Run()
            # g.Play_action(action)
            # g.Print_board()
            # print("time:", time.time() - start)
            # if g.Check_game_end():
            #     winner = g.Get_winner()
            #     print(winner)
            #     if winner == 1:
            #         win_alpha += 1
            #     if winner == -1:
            #         win_mm += 1
            #     #exit()
            #     break

            # count += 1
            # print(count)
            # print("MCTS")
            # start = time.time()
            # mcts = MCTS(g, game_name = game)
            # mcts.num_sim = 100
            # action = mcts.Run()
            # g.Play_action(action)
            # g.Print_board()
            # print("time:", time.time() - start)
            # if g.Check_game_end():
            #     winner = g.Get_winner()
            #     print(winner)
            #     if winner == 1:
            #         win_alpha += 1
            #     if winner == -1:
            #         win_mm += 1
            #     #exit()
            #     break


            count += 1
            print("Random")
            rand = Random_player(g)
            move = rand.Move()
            g.Play_action(move)
            g.Print_board()
            if g.Check_game_end():
                winner = g.Get_winner()
                print(winner)
                if winner == 1:
                    win_rand += 1
                if winner == -1:
                    win_alpha += 1
                #exit()
                break

        # g = Gomoku()

        # count = 0

        # while(1):

        #     #count += 1
        #     # print("MCTS")
        #     # start = time.time()
        #     # mcts = MCTS(g)
        #     # action = mcts.Run()
        #     # g.Play_action(action)
        #     # g.Print_board()
        #     # print("time:", time.time() - start)
        #     # if g.Check_game_end():
        #     #     winner = g.Get_winner()
        #     #     if winner == 1:
        #     #         win_alpha += 1
        #     #     if winner == -1:
        #     #         win_mm += 1
        #     #     #exit()
        #     #     break


        #     count += 1
        #     print("Random")
        #     rand = Random_player(g)
        #     move = rand.Move()
        #     g.Play_action(move)
        #     g.Print_board()
        #     if g.Check_game_end():
        #         winner = g.Get_winner()
        #         print(winner)
        #         if winner == -1:
        #             win_rand += 1
        #         if winner == 1:
        #             win_alpha += 1
        #         #exit()
        #         break

        #     count += 1
        #     print("Minimax")
        #     start = time.time()
        #     mm = Minimax(g)
        #     action = mm.Run()
        #     g.Play_action(action)
        #     g.Print_board()
        #     print("time:", time.time() - start)
        #     if g.Check_game_end():
        #         winner = g.Get_winner()
        #         print(winner)
        #         if winner == 1:
        #             win_alpha += 1
        #         if winner == -1:
        #             win_mm += 1
        #         #exit()
        #         break

        #     #count += 1
        #     # print("Alpha")
        #     # start = time.time()
        #     # amcts = A_MCTS(game = g, net = net)
        #     # amcts.num_moves = count
        #     # action = amcts.Run()
        #     # #print(action)
        #     # g.Play_action(action)
        #     # g.Print_board()
        #     # print("time:", time.time() - start)
        #     # if g.Check_game_end():
        #     #     winner = g.Get_winner()
        #     #     print(winner)
        #     #     if winner == 1:
        #     #         win_mm += 1
        #     #     if winner == -1:
        #     #         win_alpha += 1
        #     #     #exit()
        #     #     break

        # # print("Alpha:", win_alpha / i / 2, "MCTS:", win_mcts / i / 2,  "draw:", (i * 2 - win_alpha - win_mcts) / i / 2)
        # # print("Alpha:", win_alpha / i / 2, "Rand:", win_rand / i / 2,  "draw:", (i * 2 - win_alpha - win_rand) / i / 2)
        # # print("Alpha:", win_alpha / i / 2, "Minimax:", win_mm / i / 2, "draw:", (i * 2 - win_alpha - win_mm) / i / 2)
        # # print("MCTS:",  win_mcts / i / 2,  "Rand:", win_rand / i / 2,  "draw:", (i * 2 - win_mcts - win_rand) / i / 2)
        # # print("MCTS:", win_mcts / i / 2,   "Minimax:", win_mm / i / 2, "draw:", (i * 2 - win_mcts - win_mm) / i / 2)
        # # print("Minimax:", win_mm / i / 2,  "Rand:", win_rand / i / 2,  "draw:", (i * 2 - win_mm - win_rand) / i / 2)
