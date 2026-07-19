# Vibe Trading: AI Trading Agent Running Offline Securely 📈

Watch the walkthrough video: **[Vibe Trading: AI Trading Agent Running Offline Securely (YouTube)](https://youtu.be/BNusMWuyVQw)**

---

A clean, beginner-friendly quantitative analysis dashboard using **Vibe-Trading v0.1.11** integrations, real-time yfinance metrics, 50/200 SMA trend charts, and a local Ollama model (`gemma4-e2b`) for generating day-to-day stock intelligence reports.

This project is built as a single-file codebase (`app.py`), integrating real-time price monitoring and streaming the `vibe-trading` CLI research agent directly to your browser.

---

## 💡 Key Features of the Dashboard

### Tab 1: 🔍 Stock Copilot
- **What it does**: Enter any global or Indian ticker (e.g. `AAPL`, `MSFT`, `RELIANCE.NS`, `TCS.NS`). Instantly retrieves key metrics:
  - Current Price and Daily Price Change (%)
  - P/E Ratio
  - 52-Week High & Low
- **Moving Average Trends**: Automatically plots the historical price curve overlaid with the **50-day and 200-day Simple Moving Averages (SMAs)** so you can easily spot trends.
- **AI Report**: Generates a beginner-friendly markdown Stock Intelligence Report using your local Ollama instance with a single click.

### Tab 2: 💬 AI Research Agent (CLI)
- **What it does**: Leverages the official `vibe-trading run` command-line utility. You can type any natural-language prompt (e.g. *“Backtest a BTC-USDT 20/50 moving-average strategy for 2024...”*).
- **How it works**: The app executes the command in a background thread and streams the agent's real-time reasoning, tool calls, and outputs directly into a log window in your browser.

---

## 🛠 Step-by-Step Setup

### Step 1: Install Python Dependencies
Activate your virtual environment and install the required packages:
```powershell
pip install vibe-trading-ai streamlit pandas requests yfinance
```

### Step 2: Start the Web Dashboard
Launch the interactive visual interface in your browser:
```powershell
streamlit run app.py
or
python -m streamlit run app.py
```

---

## 📖 Key Terms (Beginner Friendly)

- **📈 50-day & 200-day Simple Moving Average (SMA)**: Indicates the average price of a stock over the last 50/200 trading days.
  - **Golden Cross**: When the short-term 50 SMA crosses above the long-term 200 SMA (typically a bullish buy signal).
  - **Death Cross**: When the 50 SMA crosses below the 200 SMA (typically a bearish sell signal).
- **📊 P/E Ratio (Price-to-Earnings)**: Measures the stock's current price relative to its per-share earnings. A high P/E could mean the stock is overvalued or growing fast, while a low P/E could indicate undervaluation.
- **🤖 Natural-Language Research Agent**: The core feature of Vibe-Trading which allows you to run backtests, fetch data, and formulate trading rules simply by writing prompts in plain English.
