import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def compare_revenue_and_profit():

    # 假设数据如下所示，其中 index 是日期，columns 包含两个公司的总收入和净利润
    data = {
        'Company1_TotalRevenue': [200, 220, 250, 270, 300],
        'Company1_NetProfit': [20, 25, 30, 35, 40],
        'Company2_TotalRevenue': [180, 190, 210, 230, 260],
        'Company2_NetProfit': [15, 18, 20, 22, 25],
    }
    # dates = pd.date_range(start="2020-01-01", periods=5, freq='M') # 创建时间范围
    dates = [1, 2, 3, 4, 5]

    df = pd.DataFrame(data, index=dates)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True) # 创建共享X轴的上下子图

    bar_width = 0.35

    # 第一个公司图表
    bars1 = ax1.bar(df.index - bar_width/2, df['Company1_TotalRevenue'], bar_width, label='Total Revenue', color='blue')
    bars2 = ax1.bar(df.index + bar_width/2, df['Company1_NetProfit'], bar_width, label='Net Profit', color='red')
    ax1.set_ylabel('Amount in units')
    ax1.legend()

    # 第二个公司图表
    bars3 = ax2.bar(df.index - bar_width/2, df['Company2_TotalRevenue'], bar_width, label='Total Revenue', color='green')
    bars4 = ax2.bar(df.index + bar_width/2, df['Company2_NetProfit'], bar_width, label='Net Profit', color='orange')
    ax2.set_ylabel('Amount in units')
    ax2.legend()

    plt.xlabel('Date')
    plt.suptitle('Comparison of Total Revenue and Net Profit Between Two Companies')
    plt.xticks(rotation=45)
    plt.tight_layout(rect=[0, 0, 1, 0.96]) # 调整布局避免标签重叠

    plt.show()


if __name__ == '__main__':
    compare_revenue_and_profit()