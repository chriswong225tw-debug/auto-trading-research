import pandas as pd
import numpy as np

class MimicTrader:
    def __init__(self, initial_capital=10000.0):
        self.capital = initial_capital
        self.balance = initial_capital
        self.position = 0  # 股数
        self.history = []  # 交易记录
        
    def buy(self, date, price, share_amount):
        cost = price * share_amount
        if cost <= self.balance:
            self.balance -= cost
            self.position += share_amount
            self.history.append({"Date": date, "Action": "BUY", "Price": price, "Shares": share_amount, "Balance": self.balance})
            return True
        return False

    def sell(self, date, price, share_amount):
        if self.position >= share_amount:
            self.balance += price * share_amount
            self.position -= share_amount
            self.history.append({"Date": date, "Action": "SELL", "Price": price, "Shares": share_amount, "Balance": self.balance})
            return True
        return False

    def get_net_worth(self, current_price):
        return self.balance + (self.position * current_price)

def run_simple_ma_strategy(csv_file):
    """
    一个简单的双均线策略模拟:
    当 5 日均线 向上穿过 20 日均线时买入 (金叉)
    当 5 日均线 向下穿过 20 日均线时卖出 (死叉)
    """
    df = pd.read_csv(csv_file)
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df = df.sort_values('Date')

    # 计算均线
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()

    trader = MimicTrader(initial_capital=10000.0)
    
    for i in range(1, len(df)):
        current_date = df.iloc[i]['Date']
        price = df.iloc[i]['Close']
        ma5_prev = df.iloc[i-1]['MA5']
        ma20_prev = df.iloc[i-1]['MA20']
        ma5_curr = df.iloc[i]['MA5']
        ma20_curr = df.iloc[i]['MA20']

        # 策略逻辑
        if pd.isna(ma20_curr): continue

        # 金叉: MA5 从下方穿过 MA20
        if ma5_prev <= ma20_prev and ma5_curr > ma20_curr:
            if trader.position == 0:
                shares_to_buy = int(trader.balance // price)
                if shares_to_buy > 0:
                    trader.buy(current_date, price, shares_to_buy)
                    print(f"[{current_date.date()}] 买入: 价格 {price:.2f}, 股数 {shares_to_buy}")

        # 死叉: MA5 从上方穿过 MA20
        elif ma5_prev >= ma20_prev and ma5_curr < ma20_curr:
            if trader.position > 0:
                print(f"[{current_date.date()}] 卖出: 价格 {price:.2f}, 股数 {trader.position}")
                trader.sell(current_date, price, trader.position)

    final_price = df.iloc[-1]['Close']
    print(f"\n模拟结束报告:")
    print(f"初始资金: 10000.00")
    print(f"最终净资产: {trader.get_net_worth(final_price):.2f}")
    print(f"收益率: {((trader.get_net_worth(final_price) - 10000) / 10000 * 100):.2f}%")

if __name__ == "__main__":
    print("开始模拟美股 NVDA 的交易逻辑...")
    run_simple_ma_strategy("us_nvda_data.csv")
