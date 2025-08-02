#---------------------------------------
#Since : 2024/10/06
#Update: 2024/10/06
# -*- coding: utf-8 -*-
#---------------------------------------
import numpy as np

#ゲームリスト
games=[
    'Connect4',
    'Gomoku',
    'Othello'
]

# ファイル名のリスト
files = [
    'AlphaViT_Large_Test.dat',
    'AlphaViD_Large_Test.dat',
    'AlphaVDA_Large_Test.dat',
    'AlphaViT_Multi_Test.dat',
    'AlphaViD_Multi_Test.dat',
    'AlphaVDA_Multi_Test.dat',
    ]

# 各ファイルに対して平均を計算
for game in games:
    print(game)

    for file in files:
        # ファイルからデータを読み込む
        data = np.loadtxt(game+"/"+file)

        # 2100から3000までの範囲のデータを抽出
        filtered_data = data[(data[:, 0] >= 2100) & (data[:, 0] <= 3000)]

        # 平均を計算
        average_value = np.mean(filtered_data[:, 1])
        std = np.std(filtered_data[:, 1])

        # 結果を表示
        print(f"{file} の2100から3000までの平均値: {average_value} ({std})")
