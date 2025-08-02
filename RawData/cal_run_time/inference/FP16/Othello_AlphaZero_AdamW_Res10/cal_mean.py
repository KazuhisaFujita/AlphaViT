#---------------------------------------
#Since : 2025/07/09
#Update: 2025/07/09
# -*- coding: utf-8 -*-
#---------------------------------------


#!/usr/bin/env python3
"""
numbers.txt の各行に 1 つずつ並んだ数値の
平均・標準偏差・最大・最小を表示するスクリプト
"""

import numpy as np
import sys
from pathlib import Path

def main(file_path: str) -> None:
    # 1 行 1 数値のテキストファイルを読み込む
    try:
        data = np.loadtxt(file_path, dtype=float)      # 空行や文字列が無ければこれで十分
    except OSError as e:
        sys.exit(f"ファイルを開けませんでした: {e}")
    except ValueError as e:
        sys.exit(f"数値以外の行が含まれています: {e}")

    if data.size == 0:
        sys.exit("ファイルに数値が見つかりませんでした。")

    # 統計量の計算
    mean = np.mean(data)
    std  = np.std(data)          # population 標準偏差 (ddof=0 が既定)
    max_ = np.max(data)
    min_ = np.min(data)

    # 結果の表示
    print(f"件数        : {data.size}")
    print(f"平均        : {mean:.6g}")
    print(f"標準偏差    : {std:.6g}")
    print(f"最大値      : {max_}")
    print(f"最小値      : {min_}")

if __name__ == "__main__":
    # コマンドライン引数が無ければカレントディレクトリの numbers.txt を読む
    target = sys.argv[1] if len(sys.argv) > 1 else "numbers.txt"
    main(target)
