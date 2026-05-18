# 📺 Netflix vs. Steps: Does Screen Time Affect Physical Activity?
### DSA210 — Data Science Final Report | Sena Berfin Kızıldas

---

## Table of Contents
1. [Project Motivation](#1-project-motivation)
2. [Research Question & Hypotheses](#2-research-question--hypotheses)
3. [Data Sources & Collection](#3-data-sources--collection)
4. [Data Preprocessing](#4-data-preprocessing)
5. [Exploratory Data Analysis (EDA)](#5-exploratory-data-analysis-eda)
6. [Statistical Hypothesis Testing](#6-statistical-hypothesis-testing)
7. [Results & Key Findings](#7-results--key-findings)
8. [Limitations](#8-limitations)
9. [Conclusion & Future Work](#9-conclusion--future-work)
10. [How to Run](#10-how-to-run)
11. [AI Usage](#11-ai-usage)
12. [How Others Can Reproduce This Project](#12-how-others-can-reproduce-this-project)

---

## 1. Project Motivation

We live in the age of binge-watching. Streaming platforms like Netflix are designed to be addictive — the autoplay feature, cliffhangers, and endless content libraries make it easy to spend hours on the couch without noticing. But what does this mean for our bodies?

This project investigates a simple but personally relevant question: **when I watch more Netflix, do I move less?**

Rather than relying on intuition or generic health advice, I turned to my own data. By combining my Netflix watch history with Apple Health step counts, I aimed to build a personal evidence base for understanding how passive screen consumption correlates with daily physical activity.

The ultimate goal: **replace gut feelings with statistical evidence.**

---

## 2. Research Question & Hypotheses

**Main Question:** Is there a statistically significant negative relationship between daily Netflix watch time and daily step count?

### Hypotheses Tested

| # | Hypothesis | Test Used |
|---|-----------|-----------|
| H1 | Step count is lower on days with Netflix watching vs. no watching | Mann-Whitney U |
| H2 | Step count differs significantly across watch intensity categories (No Watch / Light / Moderate / Heavy) | Kruskal-Wallis |
| H3 | There is a negative correlation between watch minutes and step count | Spearman Correlation |

All tests used α = 0.05.

> **Why non-parametric tests?** A Shapiro-Wilk normality check on both datasets confirmed that step count is **not normally distributed** (right-skewed). Parametric tests (t-test, ANOVA, Pearson) assume normality, so their non-parametric equivalents were used instead.

---

## 3. Data Sources & Collection

### Dataset A — Steps Only
- **Source:** Apple Health (exported via iPhone)
- **Content:** Daily step count
- **Coverage:** Personal data over several months

### Dataset B — Full Features
- **Source:** Apple Health + Netflix viewing history
- **Content:** Daily step count, watch minutes, watch category
- **Watch Categories:**
  - `No Watch` — 0 minutes
  - `Light` — 1–60 minutes
  - `Moderate` — 61–180 minutes
  - `Heavy` — 180+ minutes

Both datasets were aligned by date and stored as CSV files (`dataset_A_step_only.csv`, `dataset_B_full_features.csv`).

---

## 4. Data Preprocessing

- Parsed dates using `pandas` with `parse_dates`
- Created `watch_category` as an **ordered categorical variable** (`No Watch < Light < Moderate < Heavy`)
- Handled missing values by dropping NaN rows before statistical tests
- Verified dataset sizes and date ranges before analysis

```python
cat_order = ["No Watch", "Light", "Moderate", "Heavy"]
A["watch_category"] = pd.Categorical(A["watch_category"], categories=cat_order, ordered=True)
```

---

## 5. Exploratory Data Analysis (EDA)

The EDA notebooks (located in the `/EDA` folder) explore the data visually before applying formal tests.

### 5.1 Step Count Distribution

Step count data showed a clear **right skew** in both datasets — most days had moderate walking, but there were occasional high-step outlier days (e.g., travel, events). This right skew is the main reason non-parametric tests were chosen over parametric ones.

### 5.2 Watch Time Distribution

Netflix watch minutes were also heavily skewed — many days with zero or very low watching, and a smaller number of heavy binge days. This is consistent with real-life viewing patterns.

### 5.3 Step Count by Watch Category

Box plots comparing step counts across `No Watch`, `Light`, `Moderate`, and `Heavy` categories suggested a general downward trend: days with no Netflix tended to have higher median step counts than heavy-watching days. However, there was considerable overlap between groups, making formal hypothesis testing necessary.

### 5.4 Correlation Scatter Plot

A scatter plot of daily watch minutes vs. step count showed a weakly negative trend, but with high variance — no clean linear relationship was visible, consistent with the non-parametric approach chosen.

---

## 6. Statistical Hypothesis Testing

The full testing code is in `hypothesistestingdsa210.py`. All results are shown for both Dataset A and Dataset B.

### Step 0: Normality Check — Shapiro-Wilk

Before selecting tests, normality was verified.

- **H₀:** Step count is normally distributed
- **Hₐ:** Step count is NOT normally distributed
- **Result (both datasets):** p < 0.05 → **Reject H₀** → Non-parametric tests required

---

### Test 1: Mann-Whitney U
**Are step counts lower on Netflix-watching days vs. non-watching days?**

- **H₀:** No difference in step count between watching and non-watching days
- **Hₐ:** Step count is higher on non-watching days (one-sided)

```python
stat, pval = stats.mannwhitneyu(no_watch_steps, watch_steps, alternative="greater")
```

| Dataset | p-value | Decision |
|---------|---------|----------|
| Dataset A | — | See output |
| Dataset B | — | See output |

---

### Test 2: Kruskal-Wallis
**Does step count differ across watch intensity categories?**

- **H₀:** All watch categories have the same step count distribution
- **Hₐ:** At least one category is different

```python
stat, pval = stats.kruskal(*[group_steps for group in cat_order])
```

| Dataset | p-value | Decision |
|---------|---------|----------|
| Dataset A | — | See output |
| Dataset B | — | See output |

---

### Test 3: Spearman Correlation
**Is there a negative correlation between watch minutes and step count?**

- **H₀:** No correlation (ρ = 0)
- **Hₐ:** Negative correlation (ρ < 0)

```python
rho, pval = stats.spearmanr(df["watch_minutes"], df["step_count"])
```

| Dataset | ρ (rho) | p-value | Decision |
|---------|---------|---------|----------|
| Dataset A | — | — | See output |
| Dataset B | — | — | See output |

> Run `hypothesistestingdsa210.py` to see exact p-values and decisions printed to the console.

---

## 7. Results & Key Findings

After running all three tests across both datasets, the following patterns emerged:

1. **Netflix watching days and step count:** The Mann-Whitney U test evaluated whether non-watching days had significantly higher step counts. Results varied across datasets, reflecting the complexity of real-life behavior — external factors (weather, work schedule, social plans) also influence step count.

2. **Watch intensity matters:** The Kruskal-Wallis test assessed whether the four watch categories produced different step count distributions. Even if average differences seem small, statistical testing provides a principled way to evaluate whether observed differences could be due to chance.

3. **Correlation is weak but directional:** The Spearman correlation captured the monotonic relationship between watch minutes and steps. A negative ρ would confirm the expected pattern: more screen time → fewer steps, even if the effect size is modest.

4. **Two datasets, more robust conclusions:** By testing on both Dataset A (step data only) and Dataset B (full features), results could be cross-validated. Consistent findings across both datasets strengthen any conclusions drawn.

---

## 8. Limitations

- **Confounding variables:** Step count is influenced by many factors beyond Netflix — work schedule, weather, social activities, illness, and travel. These were not controlled for.
- **Self-reported / automated data:** Apple Health step counts are estimated from phone movement; users who leave their phone at home or use it inconsistently may see data gaps.
- **Personal data only:** All data is from a single individual. Findings cannot be generalized to a broader population.
- **Causality vs. correlation:** Even if a statistical relationship exists between watch time and step count, this does not prove that Netflix causes reduced activity. The direction of causation could be reversed (low-activity days → more Netflix) or both could be driven by a third factor.
- **Watch category thresholds:** The boundaries for Light / Moderate / Heavy watching were defined manually and could reasonably be set differently.

---

## 9. Conclusion & Future Work

This project applied a full data science pipeline — data collection, preprocessing, EDA, and formal statistical testing — to a personal behavioral question about screen time and physical activity.

The methodology was appropriate for the data structure: because step counts are non-normally distributed, non-parametric tests (Mann-Whitney U, Kruskal-Wallis, Spearman) were chosen over their parametric counterparts, ensuring the validity of conclusions.

**Potential future extensions:**

- Incorporate additional behavioral variables (sleep duration, mood, calendar events) to control for confounders
- Apply machine learning models (e.g., Random Forest or Logistic Regression) to predict "low activity days" from watch patterns
- Extend to a longer time window for greater statistical power
- Compare results across multiple individuals to explore whether the pattern generalizes

---

## 10. How to Run

### Prerequisites
```bash
pip install pandas numpy matplotlib scipy
```

### Repository Structure
```
├── data/
│   ├── dataset_A_step_only.csv
│   └── dataset_B_full_features.csv
├── EDA/
│   └── (EDA notebooks and visualizations)
├── hypothesistestingdsa210.py
├── Project_proposal_dsa210_senaberfinkizildas.pdf
└── README.md
```

### Run Hypothesis Tests
```bash
python hypothesistestingdsa210.py
```

This will print normality check results, then all three hypothesis test outcomes (p-values and decisions) for both datasets.

---

*This project was conducted for the Sabanci University DSA 210 — Introduction to Data Science course.*  
*Author: Sena Berfin Kızılda*

---

## 11. AI Usage

Claude (Anthropic) was used in this project for structuring the final report and improving code readability. All data collection, analysis decisions, hypothesis formulation, and interpretation of results are the author's own work.

---

## 12. How Others Can Reproduce This Project

This section is for anyone who wants to replicate this analysis using their **own** Netflix and step count data.

---

### Step 1: Export Your Netflix Watch History

1. Log in to [netflix.com](https://www.netflix.com)
2. Go to **Account → Profile & Parental Controls → [Your Profile] → Viewing Activity**
3. Scroll to the bottom and click **"Download all"**
4. You will receive a `NetflixViewingHistory.csv` file with columns: `Title`, `Date`

> ⚠️ Netflix only gives you the date and title — not the exact duration. You'll need to either manually look up episode lengths or estimate watch minutes using average episode runtimes per title.

---

### Step 2: Export Your Step Count from Apple Health

1. On your iPhone, open the **Health** app
2. Tap your profile picture (top right) → **Export Health Data**
3. Tap **Export** and share the resulting `export.zip` file to your computer
4. Unzip it — you'll find `export.xml` inside
5. Extract daily step counts with a script like this:

```python
import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse("export.xml")
root = tree.getroot()

records = []
for record in root.findall("Record"):
    if record.attrib.get("type") == "HKQuantityTypeIdentifierStepCount":
        records.append({
            "date": record.attrib["startDate"][:10],
            "steps": float(record.attrib["value"])
        })

df = pd.DataFrame(records)
daily_steps = df.groupby("date")["steps"].sum().reset_index()
daily_steps.columns = ["date", "step_count"]
daily_steps.to_csv("my_step_data.csv", index=False)
```

> 📱 **Android / Google Fit users:** Export your data from [Google Takeout](https://takeout.google.com/) and look for `Fit/Daily activity metrics/` CSV files.

---

### Step 3: Build Your Combined Dataset

Once you have both files, merge them by date and compute daily watch minutes:

```python
import pandas as pd

steps = pd.read_csv("my_step_data.csv", parse_dates=["date"])
netflix = pd.read_csv("NetflixViewingHistory.csv")

# Clean and parse Netflix dates
netflix["Date"] = pd.to_datetime(netflix["Date"], format="%m/%d/%y")
netflix = netflix.rename(columns={"Date": "date"})

# Assign estimated duration per title (manual or lookup)
# Example: assume average 45 min per row
netflix["watch_minutes"] = 45

# Aggregate to daily totals
daily_watch = netflix.groupby("date")["watch_minutes"].sum().reset_index()

# Merge with step data
merged = pd.merge(steps, daily_watch, on="date", how="left")
merged["watch_minutes"] = merged["watch_minutes"].fillna(0)

# Create watch category
def categorize(mins):
    if mins == 0:
        return "No Watch"
    elif mins <= 60:
        return "Light"
    elif mins <= 180:
        return "Moderate"
    else:
        return "Heavy"

merged["watch_category"] = merged["watch_minutes"].apply(categorize)
merged.to_csv("dataset_B_full_features.csv", index=False)
```

---

### Step 4: Run the Analysis

Clone this repository and replace the data files with your own:

```bash
git clone https://github.com/senaberfin/Sena-Berfin-K-z-lda-DSA210-Project.git
cd Sena-Berfin-K-z-lda-DSA210-Project
pip install pandas numpy matplotlib scipy
```

Replace `data/dataset_A_step_only.csv` and `data/dataset_B_full_features.csv` with your merged files, then run:

```bash
python hypothesistestingdsa210.py
```

---

### Tips & Notes

| Tip | Detail |
|-----|--------|
| **More data = better results** | At least 3–6 months of data is recommended for meaningful statistical power |
| **Be consistent with your phone** | If you frequently leave your phone at home, step count data will be unreliable |
| **Netflix duration estimates** | For more accuracy, look up actual episode lengths per title using an API like [OMDb](https://www.omdbapi.com/) or [TVmaze](https://www.tvmaze.com/api) |
| **Other streaming platforms** | You can extend this project to include YouTube, Disney+, or any service that lets you export watch history |
| **Privacy note** | Your personal health and viewing data is sensitive. Never upload raw export files (e.g., `export.xml`) to a public repository — only upload the cleaned, aggregated CSVs |
