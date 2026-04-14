import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

# HYPOTHESIS TESTS — DSA210 Project
# In this script, we test whether there is a relationship betweenNetflix watching time and daily step count using statistical tests.
# From EDA, we saw that step count is right-skewed,so we cannot assume normal distribution.
#That means parametric tests (like t-test, ANOVA) are not suitable.
# Instead, we use non-parametric tests:
#t-test          → Mann-Whitney U
#ANOVA           → Kruskal-Wallis
#Pearson corr.   → Spearman corr.

A = pd.read_csv("dataset_A_step_only.csv", parse_dates=["date"])
B = pd.read_csv("dataset_B_full_features.csv", parse_dates=["date"])

cat_order = ["No Watch", "Light", "Moderate", "Heavy"]
A["watch_category"] = pd.Categorical(A["watch_category"], categories=cat_order, ordered=True)
B["watch_category"] = pd.Categorical(B["watch_category"], categories=cat_order, ordered=True)

print("Data loaded:")
print(f"  Dataset A: {A.shape[0]} days ({A['date'].min().date()} → {A['date'].max().date()})")
print(f"  Dataset B: {B.shape[0]} days ({B['date'].min().date()} → {B['date'].max().date()})")

# CHECK NORMALITY FIRST
# Before choosing a test, we should check if data is normally distributed.
# Parametric tests assume normality.
# If this assumption is violated → we switch to non-parametric tests.
# Shapiro-Wilk test:
#   H0: data is normally distributed
#   HA: data is NOT normally distributed
# For large samples (n > 5000), Shapiro is not reliable,
# so we take a sample (n=500).

print("\n" + "="*60)
print("NORMALITY CHECK (Shapiro-Wilk)")
print("="*60)
print("H0: data is normally distributed")
print("HA: data is NOT normally distributed")
print("α = 0.05\n")

np.random.seed(42)
for df, label in [(A, "Dataset A"), (B, "Dataset B")]:
    sample = df["step_count"].dropna().sample(min(500, len(df)))
    stat, pval = stats.shapiro(sample)

    if pval < 0.05:
        decision = "Reject H0 → NOT normal → use non-parametric tests"
    else:
        decision = "Fail to reject H0 → looks normal"

    print(f"{label}:")
    print(f"  W = {stat:.4f}")
    print(f"  p = {pval:.6f}")
    print(f"  Decision: {decision}\n")

print("→ Step count is NOT normally distributed in both datasets.")
print("→ So we use NON-PARAMETRIC tests.\n")

# TEST 1: MANN-WHITNEY U
# Are steps lower on days when Netflix is watched?
# H0: No difference between groups
# HA: Steps are higher on non-watching days (one-sided)

print("="*60)
print("TEST 1: MANN-WHITNEY U")
print("="*60)

for df, label in [(A, "Dataset A"), (B, "Dataset B")]:
    no_watch = df[df["watch_minutes"] == 0]["step_count"]
    watch    = df[df["watch_minutes"] > 0]["step_count"]

    stat, pval = stats.mannwhitneyu(no_watch, watch, alternative="greater")

    if pval < 0.05:
        decision = "Reject H0 → significant difference"
    else:
        decision = "Fail to reject H0 → not enough evidence"

    print(f"{label}:")
    print(f"  p = {pval:.6f}")
    print(f"  Decision: {decision}\n")

# TEST 2: KRUSKAL-WALLIS
# Is there a difference in steps across watch categories?
# H0: all groups are the same
# HA: at least one group is different

print("="*60)
print("TEST 2: KRUSKAL-WALLIS")
print("="*60)

for df, label in [(A, "Dataset A"), (B, "Dataset B")]:
    groups = [df[df["watch_category"] == cat]["step_count"].dropna()
              for cat in cat_order]

    stat, pval = stats.kruskal(*groups)

    if pval < 0.05:
        decision = "Reject H0 → at least one group is different"
    else:
        decision = "Fail to reject H0 → no significant difference"

    print(f"{label}:")
    print(f"  p = {pval:.6f}")
    print(f"  Decision: {decision}\n")

# TEST 3: SPEARMAN CORRELATION
# Does step count decrease as watching time increases?
# H0: no correlation (ρ = 0)
# HA: negative correlation (ρ < 0)

print("="*60)
print("TEST 3: SPEARMAN CORRELATION")
print("="*60)

for df, label in [(A, "Dataset A"), (B, "Dataset B")]:
    rho, pval = stats.spearmanr(df["watch_minutes"], df["step_count"])

    if pval < 0.05:
        decision = "Reject H0 → significant correlation"
    else:
        decision = "Fail to reject H0 → no significant correlation"

    print(f"{label}:")
    print(f"  rho = {rho:.4f}")
    print(f"  p = {pval:.6f}")
    print(f"  Decision: {decision}\n")



print("""
In this project, we analyzed the relationship between Netflix watching
and daily step count using different statistical tests.

Since the data was not normally distributed, we used non-parametric tests.

Overall, results are saved and visualized for interpretation.
""")