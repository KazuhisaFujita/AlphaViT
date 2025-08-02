#---------------------------------------
#Since : 2025/06/11
#Update: 2025/07/18
# -*- coding: utf-8 -*-
#---------------------------------------

#!/usr/bin/env python
"""
bootstrap_ci_alpha.py
  - 逐次更新 Elo を点推定
  - B 回ブートストラップで 95 % CI
  - さらに AlphaZero (name="AlphaZero") との差分 ΔElo と 95 % CI も出力
"""
import csv, collections, random, argparse
import numpy as np
from elo import Elo_rating

random.seed(1)

ALPHA_NAME = "AlphaZero"     # ★CSV 内での AlphaZero の名前
DISPLAY_ORDER = [
    "AlphaZero",
    "AlphaViT_Large",
    "AlphaViD_Large",
    "AlphaVDA_Large",
    "AlphaViT_Small",
    "AlphaViD_Small",
    "AlphaVDA_Small",
    "AlphaViT_Multi",
    "AlphaViD_Multi",
    "AlphaVDA_Multi",
    "MCTS400",
    "MCTS100",
    "Minimax",
    "random",
]

def expected_update(rater, ra, rb, score_a, score_b):
    new_a = rater.New_elo(ra, rb, score_a, 1)
    new_b = rater.New_elo(rb, ra, score_b, 1)
    return new_a, new_b


def compute_elo(rows, base_elo=1500):
    elo = collections.defaultdict(lambda: float(base_elo))
    rater = Elo_rating()
    for row in sorted(rows, key=lambda r: int(r["iter"])):
        a, b = row["player_black"], row["player_white"]
        s_a = int(row["black_win"]) + 0.5 * int(row["draw"])
        s_b = int(row["white_win"]) + 0.5 * int(row["draw"])
        elo[a], elo[b] = expected_update(rater, elo[a], elo[b], s_a, s_b)
    return elo


def bootstrap_ci(path, base_elo=1500, B=1000, alpha=0.05):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))

    point = compute_elo(rows, base_elo)              # 点推定
    if ALPHA_NAME not in point:
        raise ValueError(f"{ALPHA_NAME} が players に見つかりません")

    # --- Elo サンプルと差分サンプルを貯める ---------------------------
    samples = {name: [] for name in point}
    diff_samples = {name: [] for name in point if name != ALPHA_NAME}

    for _ in range(B):
        boot_rows = random.choices(rows, k=len(rows))
        boot_elo = compute_elo(boot_rows, base_elo)
        alpha_boot = boot_elo[ALPHA_NAME]
        for name, rating in boot_elo.items():
            samples[name].append(rating)
            if name != ALPHA_NAME:
                diff_samples[name].append(rating - alpha_boot)

    # --- CI 計算 ------------------------------------------------------
    low_q, hi_q = 100 * alpha / 2, 100 * (1 - alpha / 2)
    ci = {n: tuple(np.percentile(v, [low_q, hi_q])) for n, v in samples.items()}
    diff_ci = {n: tuple(np.percentile(v, [low_q, hi_q])) for n, v in diff_samples.items()}

    return point, ci, diff_ci


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="matches.csv")
    ap.add_argument("--base", type=int, default=1500)
    ap.add_argument("--B", type=int, default=1000)
    args = ap.parse_args()

    point, ci, diff_ci = bootstrap_ci(args.file, args.base, args.B)

    # ---- 出力 ---------------------------------------------------------
    print(args.file)
    print("\n### Elo point estimates, 95% CI, and ΔElo vs AlphaZero ###")
    header = f"{'Player':20} {'Elo':>8} {'95% CI':>23} {'Δ vs AlphaZero':>20}"
    print(header)
    print("-" * len(header))

    # 1) 指定順に表示
    already = set()
    for name in DISPLAY_ORDER:
        if name in point:
            already.add(name)
            lo, hi = ci[name]
            if name == ALPHA_NAME:
                diff_str = "—"
            else:
                dlo, dhi = diff_ci.get(name, (0.0, 0.0))
                diff_str = f"${point[name] - point[ALPHA_NAME]:7.4g}$ [${dlo:+.4g}$,${dhi:+.4g}$]"
            print(f"{name:20} ${point[name]:8.4g}$ [${lo:.4g}$,${hi:.4g}$] {diff_str:>20}")
#            print(f"{name:20} ${point[name]}$ [${lo:.4g}$,${hi:.4g}$] {diff_str:>20}")

    # 2) DISPLAY_ORDER に載っていないプレーヤーは降順で後ろに
    for name, rating in sorted(point.items(), key=lambda x: -x[1]):
        if name in already:
            continue
        lo, hi = ci[name]
        dlo, dhi = diff_ci.get(name, (0.0, 0.0))
        diff_str = f"${rating - point[ALPHA_NAME]:7.4g}$ [${dlo:+.4g}$,${dhi:+.4g}$]"
        print(f"{name:20} ${rating:8.4g}$ [${lo:.4g}$,${hi:.4g}$] {diff_str:>20}")

if __name__ == "__main__":
    main()
