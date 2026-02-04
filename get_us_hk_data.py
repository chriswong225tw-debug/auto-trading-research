import yfinance as yf
import pandas as pd

def get_us_stock_data(symbol="AAPL"):
    """
    获取美股历史数据 (以 Apple 为例)
    """
    print(f"正在获取美股 {symbol} 的历史数据...")
    stock = yf.Ticker(symbol)
    df = stock.history(period="1y")
    return df

def get_hk_stock_data(symbol="0700.HK"):
    """
    获取港股历史数据 (以腾讯控股为例)
    注意：港股在 Yahoo Finance 中需要添加 .HK 后缀
    """
    print(f"正在获取港股 {symbol} 的历史数据...")
    stock = yf.Ticker(symbol)
    df = stock.history(period="1y")
    return df

if __name__ == "__main__":
    try:
        # 测试美股
        us_df = get_us_stock_data("NVDA") # 英伟达
        print(f"\n美股 NVDA 数据获取成功 (前 5 行):")
        print(us_df.head())
        us_df.to_csv("us_nvda_data.csv")
        
        # 测试港股
        hk_df = get_hk_stock_data("0700.HK") # 腾讯
        print(f"\n港股 0700.HK 数据获取成功 (前 5 行):")
        print(hk_df.head())
        hk_df.to_csv("hk_tencent_data.csv")
        
        print("\n所有测试数据已保存。")
        
    except Exception as e:
        print(f"获取数据失败: {e}")
        print("提示: 请确保已安装 yfinance (pip install yfinance)")
