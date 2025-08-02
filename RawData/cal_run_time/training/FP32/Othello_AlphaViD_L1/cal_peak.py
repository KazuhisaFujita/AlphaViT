#---------------------------------------
#Since : 2025/07/07
#Update: 2025/07/07
# -*- coding: utf-8 -*-
#---------------------------------------


import pandas as pd

df = pd.read_csv("memlog.csv", header=None,
                 names=["idx", "total", "used"])

peak_by_gpu = df.groupby("idx")["used"].max()
sum_peak = peak_by_gpu.sum()

print("---- Peak per GPU (MiB) ----")
print(peak_by_gpu)
print(f"\nTotal peak (all GPUs): {sum_peak} MiB")
