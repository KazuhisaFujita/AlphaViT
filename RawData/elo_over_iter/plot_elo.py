#---------------------------------------
#Since : 2025/06/20
#Update: 2025/06/20
# -*- coding: utf-8 -*-
#---------------------------------------


#!/usr/bin/env python3
"""
plot_elo.py – draw Elo‑learning curves for Alpha‑* agents, split into
large‑board and small‑board figures.

* Two images are produced next to **plot_elo.py**:
    • **fig_large_boards.png**   – Connect4 / Gomoku / Othello (large)
    • **fig_small_boards.png**   – Connect4‑5×4 / Gomoku‑6×6 / Othello‑6×6 (small)

* Large‑board plots render 4 single‑task + 3 multi‑task agents.
* Small‑board plots render 3 small‑board agents + AlphaZero.
* 95 % confidence intervals are drawn as translucent bands.
* Colour‑blind‑safe Okabe‑Ito palette.

Usage examples
--------------
Default (searches for the six game folders in the script directory):
```bash
python plot_elo.py
```
Specify a custom **data root** (e.g. `elo_over_iter`) :
```bash
python plot_elo.py --data-root elo_over_iter
```

The script expects *_Test_elos.csv files with columns:
    iter, elo, ci_low, ci_high

Version 1.2 – adds `--data-root` option and fixes TypeError when
`--data-root` is a string.  Now all internal paths are `pathlib.Path`
objects, so the `/` operator always works.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# ---------------------------------------------------------------------------
# CLI arguments --------------------------------------------------------------
# ---------------------------------------------------------------------------

parser = argparse.ArgumentParser(description="Plot Elo‑learning curves for Alpha‑* agents.")
parser.add_argument("--data-root", default=".", help="Root directory that contains the six game sub‑folders (default: current directory)")
args = parser.parse_args()

DATA_ROOT: Path = Path(args.data_root).expanduser().resolve()
if not DATA_ROOT.exists():
    parser.error(f"--data-root directory does not exist: {DATA_ROOT}")

# game‑specific sub‑folder names ------------------------------------------------

game_dirs = {
    "Connect4": "Connect4",
    "Gomoku": "Gomoku",
    "Othello": "Othello",
    "Connect4 5×4": "Connect4_54",
    "Gomoku 6×6": "Gomoku66",
    "Othello 6×6": "Othello66",
}

# ---------------------------------------------------------------------------
# Board configuration dictionaries ------------------------------------------
# ---------------------------------------------------------------------------

LARGE_BOARDS = {
    "Connect4": {
        "dir": DATA_ROOT / game_dirs["Connect4"],
        "prefixes": {
            "AlphaViT_Large": "AlphaViT (single)",
            "AlphaViD_Large": "AlphaViD (single)",
            "AlphaVDA_Large": "AlphaVDA (single)",
            "AlphaZero": "AlphaZero",
            "AlphaViT_Multi": "AlphaViT (multi)",
            "AlphaViD_Multi": "AlphaViD (multi)",
            "AlphaVDA_Multi": "AlphaVDA (multi)",
        },
    },
    "Gomoku": {
        "dir": DATA_ROOT / game_dirs["Gomoku"],
        "prefixes": {
            "AlphaViT_Large": "AlphaViT (single)",
            "AlphaViD_Large": "AlphaViD (single)",
            "AlphaVDA_Large": "AlphaVDA (single)",
            "AlphaZero": "AlphaZero",
            "AlphaViT_Multi": "AlphaViT (multi)",
            "AlphaViD_Multi": "AlphaViD (multi)",
            "AlphaVDA_Multi": "AlphaVDA (multi)",
        },
    },
    "Othello": {
        "dir": DATA_ROOT / game_dirs["Othello"],
        "prefixes": {
            "AlphaViT_Large": "AlphaViT (single)",
            "AlphaViD_Large": "AlphaViD (single)",
            "AlphaVDA_Large": "AlphaVDA (single)",
            "AlphaZero": "AlphaZero",
            "AlphaViT_Multi": "AlphaViT (multi)",
            "AlphaViD_Multi": "AlphaViD (multi)",
            "AlphaVDA_Multi": "AlphaVDA (multi)",
        },
    },
}

SMALL_BOARDS = {
    "Connect4 5×4": {
        "dir": DATA_ROOT / game_dirs["Connect4 5×4"],
        "prefixes": {
            "AlphaViT_Small": "AlphaViT (small)",
            "AlphaViD_Small": "AlphaViD (small)",
            "AlphaVDA_Small": "AlphaVDA (small)",
            "AlphaZero": "AlphaZero",
        },
    },
    "Gomoku 6×6": {
        "dir": DATA_ROOT / game_dirs["Gomoku 6×6"],
        "prefixes": {
            "AlphaViT_Small": "AlphaViT (small)",
            "AlphaViD_Small": "AlphaViD (small)",
            "AlphaVDA_Small": "AlphaVDA (small)",
            "AlphaZero": "AlphaZero",
        },
    },
    "Othello 6×6": {
        "dir": DATA_ROOT / game_dirs["Othello 6×6"],
        "prefixes": {
            "AlphaViT_Small": "AlphaViT (small)",
            "AlphaViD_Small": "AlphaViD (small)",
            "AlphaVDA_Small": "AlphaVDA (small)",
            "AlphaZero": "AlphaZero",
        },
    },
}

# ---------------------------------------------------------------------------
# Matplotlib style -----------------------------------------------------------
# ---------------------------------------------------------------------------

OKABE_ITO = [
    "#E69F00", "#56B4E9", "#009E73", "#F0E442",
    "#0072B2", "#D55E00", "#CC79A7", "#000000",
]

mpl.rcParams.update({
    "figure.dpi": 120,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.linestyle": ":",
    "grid.alpha": 0.6,
})

# ---------------------------------------------------------------------------
# Helper functions -----------------------------------------------------------
# ---------------------------------------------------------------------------

def _load_curve(directory: Path, prefix: str) -> pd.DataFrame:
    """Load a CSV and return a DataFrame sorted by iteration."""
    fpath = directory / f"{prefix}_Test_elos.csv"
    if not fpath.exists():
        raise FileNotFoundError(f"Expected file not found: {fpath}")
    df = pd.read_csv(fpath).sort_values("iter")
    return df


# ---------------------------------------------------------------------------
# Plotting -------------------------------------------------------------------
# ---------------------------------------------------------------------------

def _plot_board_group(group_cfg: dict[str, dict], outfile: Path, *, is_small: bool) -> None:
    n_rows = len(group_cfg)
    fig, axes = plt.subplots(n_rows, 1, figsize=(7, 3.4 * n_rows), sharey=True)
    axes = axes if isinstance(axes, (list, tuple)) else [axes]  # ensure iterable

    for ax, (board_name, cfg) in zip(axes, group_cfg.items()):
        palette = iter(OKABE_ITO)
        for prefix, label in cfg["prefixes"].items():
            colour = next(palette)
            df = _load_curve(cfg["dir"], prefix)
            x, y = df["iter"], df["elo"]
            ax.plot(x, y, label=label, color=colour, linewidth=2)
            if {"ci_low", "ci_high"}.issubset(df.columns):
                ax.fill_between(x, df["ci_low"], df["ci_high"], color=colour, alpha=0.18, linewidth=0)

        ax.set_title(board_name, fontweight="bold")
        ax.set_ylabel("Elo rating")
        ax.set_ylim(800, 2300)
        ax.set_xlim(0, 1000 if is_small else 3000)
        ax.set_xlabel("Iterations")
        ax.legend(loc="lower right", fontsize=9, frameon=False)

    fig.tight_layout()
    fig.savefig(outfile, bbox_inches="tight")
    print(f"✔ saved {outfile.relative_to(DATA_ROOT)}")


# ---------------------------------------------------------------------------
# Entry‑point ----------------------------------------------------------------
# ---------------------------------------------------------------------------

def main() -> None:
    _plot_board_group(LARGE_BOARDS, DATA_ROOT / "fig_large_boards.png", is_small=False)
    _plot_board_group(SMALL_BOARDS, DATA_ROOT / "fig_small_boards.png", is_small=True)


if __name__ == "__main__":
    main()
