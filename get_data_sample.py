import akshare as ak
import pandas as pd

def get_china_stock_data(symbol="sh600519"):
    """
    获取中国 A 股历史数据 (以贵州茅台为例)
    """
    print(f"正在获取股票 {symbol} 的历史数据...")
    stock_df = ak.stock_zh_a_hist(symbol=symbol.replace("sh", "").replace("sz", ""), 
                                  period="daily", 
                                  start_date="20240101", 
                                  end_date="20250205", 
                                  adjust="qfq")
    return stock_df

if __name__ == "__main__":
    try:
        df = get_china_stock_data()
        print("数据获取成功！前 5 行如下：")
        print(df.head())
        # 保存到本地
        df.to_csv("maotai_data.csv", index=False)
        print("数据已保存至 maotai_data.csv")
    except Exception as e:
        print(f"获取数据失败: {e}")
        print("提示: 请确保已安装 akshare (pip install akshare)")
