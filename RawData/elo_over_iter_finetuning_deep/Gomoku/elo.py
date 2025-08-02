#---------------------------------------
#Since : 2019/06/12
#Update: 2024/04/29
# -*- coding: utf-8 -*-
#---------------------------------------
import numpy as np
import math as mt

class Elo_rating():
    def __init__(self):
        self.c_elo = 1 / 400
        self.K = 8

    def P_est(self, elo, elo_opponent):
        return(1/(1 + mt.pow(10, self.c_elo * (elo_opponent - elo))))

    def New_elo(self, elo, elo_opponent, n_win, n_games):
        return(elo + self.K * (n_win - self.P_est(elo, elo_opponent) * n_games))

if __name__ == '__main__':
    elo_rating = Elo_rating()
    elo1 = 1500
    elo2 = 1500
    n_win = 0
    n_games =1
    print(elo_rating.New_elo(elo1, elo2, n_win, n_games))
