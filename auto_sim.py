import sys
import os
import yfinance as yf
import pandas as pd
from backtest_logic import run_simple_ma_strategy

def auto_sim(symbol):
    print(f"🚀 Starting automatic simulation for: {symbol}")
    
    # 1. Fetch data
    print(f"📥 Fetching historical data for {symbol}...")
    stock = yf.Ticker(symbol)
    df = stock.history(period="1y")
    
    if df.empty:
        print(f"❌ Error: No data found for symbol '{symbol}'. Please check if it's correct.")
        return
    
    csv_filename = f"{symbol.replace('.', '_')}_data.csv"
    df.to_csv(csv_filename)
    print(f"✅ Data saved to {csv_filename}")
    
    # 2. Run simulation (it will generate the public/index.html)
    print(f"⚙️ Running strategy logic...")
    run_simple_ma_strategy(csv_filename, symbol)
    
    # 3. Deploy to Vercel
    print(f"📦 Deploying updated report to Vercel...")
    os.system("vercel deploy public --prod --yes --public")
    
    print(f"\n✨ Simulation complete! View results at: https://public-rho-umber.vercel.app")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_symbol = sys.argv[1]
        auto_sim(target_symbol)
    else:
        print("Usage: python auto_sim.py <SYMBOL>")
        print("Example: python auto_sim.py TSLA")
        print("Example: python auto_sim.py 9988.HK")
