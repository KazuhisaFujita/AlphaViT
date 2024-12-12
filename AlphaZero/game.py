#---------------------------------------
#Since : 2019/04/10
#Update: 2023/12/10
# -*- coding: utf-8 -*-
#---------------------------------------
import numpy as np
from Gomoku import Gomoku
from player import Random_player
from classical_MCTS import MCTS
import time
from parameters_alphazero import Parameters
from AlphaZero_mcts import A_MCTS as AZ_MCTS
from nn_alphazero   import NNetWrapper

if __name__ == '__main__':
    win_alpha = 0
    win_mcts = 0
    win_rand = 0
    win_mm = 0

    # az_params = AZ_Parameters()
    # az_net  = AZ_NNetWrapper()
    # az_net.load_model("alphazero.model")
    # az_net.device = "cuda"

    params = Parameters()
    az_net  = NNetWrapper()
#    av_net.load_model("alphavit.model")
    az_net.device = "cuda"

    for i in range(1,2):
        g = Gomoku(6,6,5,1,-1,1)#Gomoku()#Connect4()#Gomoku()
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

            count += 1
            print("AlphaZero")
            start = time.time()
            #print(g.Get_valid_moves())
            az_amcts = AZ_MCTS(game = g, net = az_net)
            az_amcts.params.Temp = 10
            az_amcts.num_moves = count
            action = az_amcts.Run()
            print(action)
            g.Play_action(action)
            g.Print_board()
            print("time:", time.time() - start)
            if g.Check_game_end():
                winner = g.Get_winner()
                print(winner)
                if winner == 1:
                    win_alpha += 1
                if winner == -1:
                    win_mm += 1
                #exit()
                break

            # count += 1
            # print(count)
            # print("AlphaViT")
            # start = time.time()
            # #print(g.Get_valid_moves())
            # amcts = AV_MCTS(game = g, game_name = game, net = av_net)
            # amcts.params.Temp = 10
            # amcts.num_moves = count
            # action = amcts.Run()
            # print(action)
            # g.Play_action(action)
            # g.Print_board()
            # print("time:", time.time() - start)
            # winner = g.Get_winner()
            # print(winner)
            # if g.Check_game_end():
            #     winner = g.Get_winner()
            #     print(winner)
            #     if winner == 1:
            #         win_alpha += 1
            #     if winner == -1:
            #         win_mm += 1
            #     #exit()
            #     break


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
