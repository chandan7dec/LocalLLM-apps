import os
import subprocess
import requests
import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Vibe Stock Intelligence", layout="wide")
st.title("📈 Vibe Stock Intelligence Copilot")

tab1, tab2 = st.tabs(["🔍 Stock Copilot", "💬 AI Research Agent (CLI)"])

def get_stock_data(symbol):
    """
    Fetches real-time price info and historical data using yfinance.
    Handles missing info keys gracefully using fallback calculations from history.
    """
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1y")
        if hist.empty:
            return None, "No data found. Check symbol format."
            
        info = {}
        try:
            info = ticker.info
        except Exception:
            pass
            
        name = info.get("longName") or info.get("shortName") or symbol
        current_price = info.get("currentPrice") or info.get("regularMarketPrice") or hist["Close"].iloc[-1]
        prev_close = info.get("previousClose") or hist["Close"].iloc[-2] if len(hist) > 1 else current_price
        change = current_price - prev_close
        
        metrics = {
            "name": name,
            "price": current_price,
            "change": change,
            "pct_change": (change / prev_close) * 100 if prev_close else 0.0,
            "market_cap": info.get("marketCap") or 0.0,
            "pe": info.get("trailingPE") or "N/A",
            "high": hist["High"].max(),
            "low": hist["Low"].min(),
            "history": hist
        }
        return metrics, None
    except Exception as e:
        return None, str(e)

with tab1:
    st.markdown(
        "Enter any stock symbol (e.g. `AAPL`, `MSFT`, `RELIANCE.NS`, `TCS.NS`) "
        "to view key metrics, trend indicators, and generate an AI report."
    )
    symbol = st.text_input("Stock Symbol", value="RELIANCE.NS").upper().strip()
    
    if symbol:
        metrics, error = get_stock_data(symbol)
        if error:
            st.error(error)
        elif metrics:
            st.subheader(f"🏢 {metrics['name']} ({symbol})")
            
            # Metric Columns
            c1, c2, c3, c4 = st.columns(4)
            c1.metric(
                label="Current Price",
                value=f"{metrics['price']:.2f}",
                delta=f"{metrics['change']:.2f} ({metrics['pct_change']:.2f}%)"
            )
            c2.metric(label="P/E Ratio", value=f"{metrics['pe']}")
            c3.metric(label="52-Week High", value=f"{metrics['high']:.2f}")
            c4.metric(label="52-Week Low", value=f"{metrics['low']:.2f}")
            
            # Trend Chart Calculations
            hist = metrics["history"]
            hist["SMA50"] = hist["Close"].rolling(50).mean()
            hist["SMA200"] = hist["Close"].rolling(200).mean()
            
            st.subheader("📈 Price Trend & Moving Averages (50/200 SMA)")
            st.line_chart(hist[["Close", "SMA50", "SMA200"]])
            
            # AI Report Generator
            if st.button("🤖 Generate AI Intelligence Report"):
                with st.spinner("Analyzing with local Ollama model..."):
                    prompt = (
                        f"Analyze stock {symbol} ({metrics['name']}).\n"
                        f"- Current Price: {metrics['price']:.2f}\n"
                        f"- Daily Price Change: {metrics['change']:.2f} ({metrics['pct_change']:.2f}%)\n"
                        f"- 52-Week High: {metrics['high']:.2f}\n"
                        f"- 52-Week Low: {metrics['low']:.2f}\n"
                        f"- P/E Ratio: {metrics['pe']}\n"
                        f"- Latest 50-day SMA: {hist['SMA50'].iloc[-1]:.2f}\n"
                        f"- Latest 200-day SMA: {hist['SMA200'].iloc[-1]:.2f}\n\n"
                        f"Write a beginner-friendly stock report containing:\n"
                        f"1. Overview\n"
                        f"2. SMA Crossover trend analysis\n"
                        f"3. Pros & Cons (bullet points)\n"
                        f"4. Actionable Target Outlook."
                    )
                    
                    # payload = {
                    #     "model": "gemma4-e2b",
                    #     "messages": [{"role": "user", "content": prompt}],
                    #     "stream": False
                    # }
                    # Change this in your code:

                    payload = {
                        "messages": [{"role": "user", "content": prompt}],
                        "stream": False
                    }
                    
                    try:
                        resp = requests.post(
                            "http://192.168.29.60:11434/v1/chat/completions",
                            json=payload,
                            timeout=90
                        )
                        report = resp.json()["choices"][0]["message"]["content"]
                        
                        # Save the generated report directly to output.md on disk
                        with open("output.md", "w", encoding="utf-8") as f:
                            f.write(report)
                        
                        st.subheader("📝 Stock Intelligence Report")
                        st.markdown(report)
                        st.download_button(
                            label="Download Report",
                            data=report,
                            file_name="output.md"
                        )
                    except Exception as e:
                        st.error(f"Ollama connection error: {e}")

with tab2:
    st.subheader("🤖 Natural-Language Research Agent")
    st.markdown(
        "Enter any custom prompt to run the `vibe-trading` natural-language agent directly. "
        "The agent will build, backtest, and output results in real-time."
    )
    
    user_prompt = st.text_area(
        label="Research Prompt",
        value=(
            "Backtest a BTC-USDT 20/50 moving-average strategy for 2024, "
            "summarize return and drawdown, then export the report"
        ),
        height=100
    )
    
    if st.button("⚡ Run Research Agent"):
        log_container = st.empty()
        log_text = ""
        
        env = os.environ.copy()
        # env.update({
        #     "LANGCHAIN_PROVIDER": "ollama",
        #     "LANGCHAIN_MODEL_NAME": "gemma4-e2b",
        #     "OLLAMA_BASE_URL": "http://localhost:11434",
        #     "VIBE_TRADING_ENABLE_SHELL_TOOLS": "true"
        # })

        # Update this in your code:
        env.update({
            "LANGCHAIN_PROVIDER": "ollama",
            "LANGCHAIN_MODEL_NAME": "llama-3.2-3b-instruct.Q4_K_M.gguf", # Update to match your model
            "OLLAMA_BASE_URL": "http://192.168.29.60:11434/v1",
            "VIBE_TRADING_ENABLE_SHELL_TOOLS": "true"
        })
        
        process = subprocess.Popen(
            ["vibe-trading", "run", "-p", user_prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            bufsize=1
        )
        
        for line in process.stdout:
            log_text += line
            log_container.text_area("Agent Output Logs", log_text, height=400)
            
        process.wait()
        st.success("Agent completed execution!")
