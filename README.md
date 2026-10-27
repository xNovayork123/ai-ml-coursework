# AI / Machine Learning Coursework

A collection of AI and machine learning projects from my Software Engineering studies
(University of Europe for Applied Sciences).

## [trading-agent/](trading-agent) — Stock Market Trading Agent (AI Final Exam)

Downloads real AAPL market data (`yfinance`), engineers technical-indicator features
(RSI, SMA ratio, Bollinger Bands, MACD, daily/volume returns), and trains Logistic
Regression and Random Forest classifiers to predict next-day price direction. Uses a
temporal train/test split to avoid look-ahead data leakage, and generates evaluation
plots (confusion matrices, correlation heatmap, feature importance, accuracy
comparison) plus an auto-built presentation deck (`python-pptx`).

**Stack:** Python, scikit-learn, pandas, yfinance, matplotlib/seaborn

## [vacuum-world-agent/](vacuum-world-agent) — Reflex Agent Simulation

A percept-driven reflex agent (Russell & Norvig *AI: A Modern Approach* model) that
cleans a multi-room "Vacuum World" environment using only local percepts — no
planning or search. Includes a configurable CLI simulation harness with presets,
logging, and animation. Built on a course-provided framework (see its own
README/LICENSE).

**Stack:** Python

## [classifiers/](classifiers) — ML Classifier Comparison

A CLI tool to train and compare SVM, Decision Tree, and Logistic Regression
classifiers on the Vacuum World dirt-distribution dataset; outputs confusion
matrices, classification reports, feature importances, and Graphviz decision-tree
visualizations.

**Stack:** Python, scikit-learn, pandas

## [heart-attack-prediction/](heart-attack-prediction) — Heart Attack Risk Prediction

A logistic regression model estimating cardiovascular risk from patient data, with a
preprocessing pipeline (`StandardScaler`, `OneHotEncoder` via `ColumnTransformer`)
and a tuned classification threshold to balance recall on an imbalanced dataset.

**Stack:** Python, scikit-learn, pandas
