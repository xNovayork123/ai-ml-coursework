"""
Stock Market Trading Agent — AI Final Exam
Emiliano | SoSe26 | 3sem B
"""

import warnings
warnings.filterwarnings("ignore")

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay
)
from sklearn.preprocessing import StandardScaler
import os

# ── Output folder for slide images ────────────────────────────────────────────
os.makedirs("slides_output", exist_ok=True)
plt.rcParams.update({"figure.dpi": 150, "font.size": 11})

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Download data
# ══════════════════════════════════════════════════════════════════════════════
print("Downloading AAPL data (2019-2024)...")
df = yf.download("AAPL", start="2019-01-01", end="2024-12-31", auto_adjust=True, progress=False)
df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
df.columns = ["Open", "High", "Low", "Close", "Volume"]
print(f"Shape: {df.shape}  |  Date range: {df.index[0].date()} to {df.index[-1].date()}")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Feature engineering (agent percepts)
# ══════════════════════════════════════════════════════════════════════════════

# RSI (14-day)
delta = df["Close"].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()
rs = avg_gain / avg_loss
df["RSI"] = 100 - (100 / (1 + rs))

# Simple Moving Averages
df["SMA_20"] = df["Close"].rolling(20).mean()
df["SMA_50"] = df["Close"].rolling(50).mean()

# SMA ratio — captures trend direction
df["SMA_ratio"] = df["SMA_20"] / df["SMA_50"]

# Bollinger Bands (20-day, 2 std)
bb_std = df["Close"].rolling(20).std()
df["BB_upper"] = df["SMA_20"] + 2 * bb_std
df["BB_lower"] = df["SMA_20"] - 2 * bb_std
df["BB_position"] = (df["Close"] - df["BB_lower"]) / (df["BB_upper"] - df["BB_lower"])

# MACD (12-day EMA - 26-day EMA)
ema12 = df["Close"].ewm(span=12, adjust=False).mean()
ema26 = df["Close"].ewm(span=26, adjust=False).mean()
df["MACD"] = ema12 - ema26

# Daily return
df["Daily_return"] = df["Close"].pct_change()

# Volume change
df["Volume_change"] = df["Volume"].pct_change()

# ── Label: will tomorrow's close be higher than today's? ──────────────────────
df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

# Drop NaN rows from rolling calculations
df.dropna(inplace=True)

FEATURES = ["RSI", "SMA_ratio", "BB_position", "MACD", "Daily_return", "Volume_change"]
print(f"\nFeatures: {FEATURES}")
print(f"Dataset after cleaning: {df.shape[0]} rows")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — EDA / Data analysis (slides)
# ══════════════════════════════════════════════════════════════════════════════

# ── Plot 1: Price chart with SMA & Bollinger Bands ───────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df.index, df["Close"], label="AAPL Close", linewidth=1, color="#1f77b4")
ax.plot(df.index, df["SMA_20"], label="SMA 20", linewidth=1.2, linestyle="--", color="orange")
ax.plot(df.index, df["SMA_50"], label="SMA 50", linewidth=1.2, linestyle="--", color="green")
ax.fill_between(df.index, df["BB_lower"], df["BB_upper"], alpha=0.15, color="gray", label="Bollinger Bands")
ax.set_xlim(df.index[0], df.index[-1])
ax.set_title("AAPL — Price, Moving Averages & Bollinger Bands (2019-2024)")
ax.set_ylabel("Price (USD)")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("slides_output/01_price_chart.png")
plt.close()
print("Saved: 01_price_chart.png")

# ── Plot 2: Class balance ────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

counts = df["Target"].value_counts().sort_index()  # sort_index: 0=Down first, 1=Up second
axes[0].bar(["Down (0)", "Up (1)"], counts.values, color=["#e74c3c", "#2ecc71"], edgecolor="white", width=0.5)
axes[0].set_title("Class Balance: Up vs Down Days", pad=10)
axes[0].set_ylabel("Number of days")
axes[0].set_ylim(0, max(counts.values) * 1.22)  # headroom so text doesn't hit title
for i, v in enumerate(counts.values):
    axes[0].text(i, v + max(counts.values) * 0.02,
                 f"{v}  ({v/len(df)*100:.1f}%)", ha="center", fontweight="bold", fontsize=11)

# Daily return distribution
axes[1].hist(df["Daily_return"] * 100, bins=60, color="#3498db", edgecolor="white", alpha=0.85)
axes[1].axvline(0, color="red", linestyle="--", linewidth=1.5, label="Zero return")
axes[1].set_title("Distribution of Daily Returns (%)", pad=10)
axes[1].set_xlabel("Daily Return (%)")
axes[1].set_ylabel("Frequency")
axes[1].legend()

plt.tight_layout(pad=1.5)
plt.savefig("slides_output/02_class_balance_and_returns.png", bbox_inches="tight")
plt.close()
print("Saved: 02_class_balance_and_returns.png")

# ── Plot 3: Correlation heatmap ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
corr = df[FEATURES + ["Target"]].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn", center=0,
            mask=mask, ax=ax, linewidths=0.5, cbar_kws={"shrink": 0.8})
ax.set_title("Feature Correlation Matrix", fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig("slides_output/03_correlation_heatmap.png")
plt.close()
print("Saved: 03_correlation_heatmap.png")

# Print basic stats
print("\n── Data Summary ────────────────────────────────")
print(df[FEATURES + ["Target"]].describe().round(3))
print(f"\nClass balance:\n{df['Target'].value_counts(normalize=True).round(3)}")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — Train/Test split (temporal — no data leakage)
# ══════════════════════════════════════════════════════════════════════════════
split_idx = int(len(df) * 0.80)
train_df = df.iloc[:split_idx]
test_df  = df.iloc[split_idx:]

X_train, y_train = train_df[FEATURES], train_df["Target"]
X_test,  y_test  = test_df[FEATURES],  test_df["Target"]

print(f"\nTrain: {len(train_df)} rows  |  Test: {len(test_df)} rows")
print(f"Train period: {train_df.index[0].date()} to {train_df.index[-1].date()}")
print(f"Test  period: {test_df.index[0].date()} to {test_df.index[-1].date()}")

# Scale for Logistic Regression
scaler  = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — Train models
# ══════════════════════════════════════════════════════════════════════════════

# Logistic Regression (baseline)
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_sc, y_train)
lr_pred = lr.predict(X_test_sc)
lr_acc  = accuracy_score(y_test, lr_pred)

# Random Forest (main model)
rf = RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_acc  = accuracy_score(y_test, rf_pred)

print(f"\n── Model Results ───────────────────────────────")
print(f"Logistic Regression accuracy : {lr_acc:.4f} ({lr_acc*100:.1f}%)")
print(f"Random Forest accuracy       : {rf_acc:.4f} ({rf_acc*100:.1f}%)")
print(f"\nRandom Forest Classification Report:\n")
print(classification_report(y_test, rf_pred, target_names=["Down", "Up"]))

# ══════════════════════════════════════════════════════════════════════════════
# STEP 6 — Results plots (slides)
# ══════════════════════════════════════════════════════════════════════════════

# ── Plot 4: Confusion matrices side by side ───────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

for ax, pred, title, acc in zip(
    axes,
    [lr_pred, rf_pred],
    ["Logistic Regression", "Random Forest"],
    [lr_acc, rf_acc]
):
    cm = confusion_matrix(y_test, pred)
    disp = ConfusionMatrixDisplay(cm, display_labels=["Down", "Up"])
    disp.plot(ax=ax, colorbar=False, cmap="Blues")
    ax.set_title(f"{title}\nAccuracy: {acc*100:.1f}%", fontweight="bold")

plt.suptitle("Model Results — Confusion Matrices", fontweight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.93])  # reserve top space for suptitle
plt.savefig("slides_output/04_confusion_matrices.png", bbox_inches="tight")
plt.close()
print("Saved: 04_confusion_matrices.png")

# ── Plot 5: Feature importance ────────────────────────────────────────────────
importances = pd.Series(rf.feature_importances_, index=FEATURES).sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(8, 4))
colors = ["#2ecc71" if v == importances.max() else "#3498db" for v in importances.values]
importances.plot(kind="barh", ax=ax, color=colors, edgecolor="white")
ax.set_title("Random Forest — Feature Importance", fontweight="bold")
ax.set_xlabel("Importance")
ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig("slides_output/05_feature_importance.png")
plt.close()
print("Saved: 05_feature_importance.png")

# ── Plot 6: Accuracy comparison bar ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 4))
models = ["Logistic\nRegression", "Random\nForest"]
accs   = [lr_acc * 100, rf_acc * 100]
bars   = ax.bar(models, accs, color=["#95a5a6", "#2ecc71"], edgecolor="white", width=0.4)
ax.axhline(50, color="red", linestyle="--", linewidth=1.5, label="Random baseline (50%)")
ax.set_ylim(40, 62)  # tighter range, label at ~52% stays clear
ax.set_ylabel("Accuracy (%)")
ax.set_title("Model Accuracy Comparison", fontweight="bold", pad=10)
ax.legend()
for bar, acc in zip(bars, accs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
            f"{acc:.1f}%", ha="center", fontweight="bold", fontsize=12)
plt.tight_layout()
plt.savefig("slides_output/06_accuracy_comparison.png")
plt.close()
print("Saved: 06_accuracy_comparison.png")

print("\nAll done! Check the 'slides_output' folder for all charts.")
print(f"\nSummary for presentation:")
print(f"  Dataset      : AAPL, 2019-2024, {df.shape[0]} trading days")
print(f"  Features     : {len(FEATURES)} technical indicators")
print(f"  Best model   : Random Forest ({rf_acc*100:.1f}% accuracy)")
print(f"  Baseline     : Logistic Regression ({lr_acc*100:.1f}% accuracy)")
