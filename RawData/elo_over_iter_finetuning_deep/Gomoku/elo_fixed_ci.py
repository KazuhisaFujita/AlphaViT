#---------------------------------------
#Since : 2025/06/11
#Update: 2025/06/20
# -*- coding: utf-8 -*-
#---------------------------------------


#!/usr/bin/env python
"""
elo_fixed_ci.py
  - 14 体の固定 Elo を動かさず、
    学習回数ごとに存在するテスト AI (1,2,4,...,1000) の Elo を推定
  - ブートストラップで 95 % CI を付与
"""

import csv, random, argparse, re, collections
from typing import Dict, List, Tuple
import numpy as np
import os
from elo import Elo_rating

# ----------------------------------------------------------------------
# 1) 14 体分の固定 Elo をここに記入（例は Table 3 の値）
FIXED_ELO: Dict[str, float] = {
"AlphaZero"     :2038.2466171010637,
"AlphaViT_Large":1965.8475683497727,
"AlphaViD_Large":1698.2176165801982,
"AlphaVDA_Large":1566.7521224060813,
"AlphaViT_Small":1552.5516241216822,
"AlphaViD_Small":1518.6840177821737,
"AlphaVDA_Small":977.2018711755893,
"AlphaViT_Multi":2024.3143538856154,
"AlphaViD_Multi":1529.5055865947666,
"AlphaVDA_Multi":1570.418718618554,
"MCTS100"       :1228.7568430979902,
"MCTS400"       :1160.7989189204172,
"Minimax"       :1471.8780874370223,
"random"        :696.8260539290741,
}

NUM_ITER  = {"Connect4": 3000,
             "Connect4_54": 1000,
             "Gomoku": 3000,
             "Gomoku66": 1000,
             "Othello": 3000,
             "Othello66": 1000}

GAME_NAME = "Gomoku"
# Will be set dynamically inside main() based on the input filename
TEST_NAME_RAW: str = ""
ITERATIONS = [1,2,4,6,10]
ITERATIONS.extend(range(20,100,20))
ITERATIONS.extend(range(100,NUM_ITER[GAME_NAME]+1,100))


# ----------------------------------------------------------------------

def extract_test_name(csv_path: str) -> str:
    """Return base name without trailing "_matches.csv"."""
    base = os.path.basename(csv_path)
    return re.sub(r"_matches\.csv$", "", base)

def rename_test_player(name: str, it: str) -> str:
    """テスト AI の行だけ名前を iter 付きに変更"""
    if name == TEST_NAME_RAW:
        return f"{TEST_NAME_RAW}_iter{int(it):04d}"
    return name

def load_rows(path: str) -> List[dict]:
    with open(path, newline="") as f:
        rdr = csv.DictReader(f)
        rows = []
        for r in rdr:
            r = dict(r)                   # make mutable
            r["player_black"] = rename_test_player(r["player_black"], r["iter"])
            r["player_white"] = rename_test_player(r["player_white"], r["iter"])
            rows.append(r)
    return rows

# ----------------------------------------------------------------------
def compute_elo_fixed(rows: List[dict],
                      base_elo: float = 1500) -> Dict[str, float]:
    """
    Elo を逐次更新。ただし
      - FIXED_ELO に載っているプレーヤは rating を変えない
      - それ以外 (テスト AI) は更新する
    """
    elo = collections.defaultdict(lambda: float(base_elo))
    elo.update(FIXED_ELO)     # 初期化
    rater = Elo_rating()      # 既存クラス (デフォルト K=1)
    for row in rows:
        a, b = row["player_black"], row["player_white"]
        sa = int(row["black_win"]) + 0.5 * int(row["draw"])
        sb = int(row["white_win"]) + 0.5 * int(row["draw"])

        # 固定 vs 固定 → スキップ
        if a in FIXED_ELO and b in FIXED_ELO:
            continue

        # 更新は「動く側だけ」
        if a in FIXED_ELO:
            elo[b] = rater.New_elo(elo[b], elo[a], sb, 1)   # b が可変
        elif b in FIXED_ELO:
            elo[a] = rater.New_elo(elo[a], elo[b], sa, 1)   # a が可変
        else:
            # テスト AI 同士は発生しない想定だが一応
            elo[a], elo[b] = rater.New_elo(elo[a], elo[b], sa, 1), \
                             rater.New_elo(elo[b], elo[a], sb, 1)
    return elo

# ----------------------------------------------------------------------
def bootstrap_ci_fixed(rows: List[dict],
                       B: int = 1000,
                       alpha: float = 0.05
                       ) -> Tuple[Dict[str,float],Dict[str,Tuple[float,float]]]:
    point = compute_elo_fixed(rows)
    samples = {name: [] for name in point}

    for _ in range(B):
        boot_rows = random.choices(rows, k=len(rows))
        boot_elo = compute_elo_fixed(boot_rows)
        for name, rating in boot_elo.items():
            samples[name].append(rating)

    low_q, hi_q = 100*alpha/2, 100*(1-alpha/2)
    ci = {n: tuple(np.percentile(v, [low_q, hi_q])) for n,v in samples.items()}
    return point, ci

# ----------------------------------------------------------------------

def write_results_csv(
    csv_path: str,
    point: Dict[str, float],
    ci: Dict[str, Tuple[float, float]],
    iterations: List[int],
):
    """Write selected test‑AI rows to a CSV file."""
    header = ["iter", "elo", "ci_low", "ci_high"]
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for it in iterations:
            name = f"{TEST_NAME_RAW}_iter{it:04d}"
            if name not in point:
                continue
            elo = point[name]
            lo, hi = ci[name]
            delta = elo - FIXED_ELO["AlphaZero"]
            w.writerow([it, f"{elo:.1f}", f"{lo:.1f}", f"{hi:.1f}"])

# ----------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="matches.csv", help="input match CSV (from self‑play)")
    ap.add_argument("--B", type=int, default=1000, help="number of bootstrap samples")
    ap.add_argument("--out", default="elo_progress.csv", help="output CSV for plotting")
    args = ap.parse_args()

    # Set the global TEST_NAME_RAW dynamically
    global TEST_NAME_RAW
    TEST_NAME_RAW = extract_test_name(args.file)

    rows = load_rows(args.file)
    point, ci = bootstrap_ci_fixed(rows, args.B)

    # Print to console (as before)
    header = f"{'iter':>6} {'Elo':>8} {'95% CI':>23}  ΔvsAlphaZero"
    print(header)
    print("-" * len(header))
    for it in ITERATIONS:
        name = f"{TEST_NAME_RAW}_iter{it:04d}"
        if name not in point:
            continue
        elo = point[name]
        lo, hi = ci[name]
        delta = elo - FIXED_ELO["AlphaZero"]
        print(f"{it:6d} {elo:8.1f}  [{lo:.1f}, {hi:.1f}]  {delta:+7.1f}")

    # Save to CSV
    write_results_csv(args.out, point, ci, ITERATIONS)
    print(f"\nSaved results to {args.out} – ready for plotting!")

# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()
