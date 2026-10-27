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
