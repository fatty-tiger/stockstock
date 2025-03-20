import os
token = os.environ['TUSHARE_TOKEN']

import tushare as ts
import numpy as np
import statistics
import pandas as pd
import matplotlib.pyplot as plt

from cache_util import StockInfoCache

stock_info_cache = StockInfoCache()

pro = ts.pro_api(token)


def main(ts_name, start_date, end_date):
    ts_code = stock_info_cache.get_code_by_name(ts_name)

    df = pro.income(ts_code=ts_code, start_date=start_date, end_date=end_date, 
                    fields='ts_code,end_date,total_revenue,revenue,sell_exp,admin_exp,fin_exp,rd_exp,total_profit,operate_profit,n_income,n_income_attr_p')
    df['total_revenue'] = df['total_revenue'] / 1e8
    df['revenue'] = df['revenue'] / 1e8
    df['n_income'] = df['n_income'] / 1e8
    df['n_income_attr_p'] = df['n_income_attr_p'] / 1e8
    df['sell_exp'] = df['sell_exp'] / 1e4
    df['admin_exp'] = df['admin_exp'] / 1e4
    df['fin_exp'] = df['fin_exp'] / 1e4
    df['rd_exp'] = df['rd_exp'] / 1e4

    df = df.sort_values(by='end_date')
    df.index = pd.to_datetime(df['end_date'])
    
    
    total_revenue = df.total_revenue.tolist()
    operating_revenue = df.revenue.tolist()
    net_profit = df.n_income.tolist()
    parent_net_profit = df.n_income_attr_p.tolist()
    
    sales_expense = df.sell_exp.tolist()
    management_expense = df.admin_exp.tolist()
    financial_expense = df.fin_exp.tolist()
    rd_expense = df.rd_exp.tolist()
    
    # 创建画布和子图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [1, 1]})
    plt.subplots_adjust(hspace=0.4)
    
    # 创建双Y轴
    ax1_right = ax1.twinx()

    # 上子图配置
    width = 0.2  # 柱状图宽度
    offset = 0.1  # 组内偏移量
    x = np.arange(len(df.end_date))  # 将日期转换为数值位置

    # 绘制总营收和营收
    for i in x:
        ax1.bar(i - offset, total_revenue[i], width=width, color='royalblue', label='Total Revenue' if i == 0 else "")
        ax1.bar(i - offset, operating_revenue[i], width=width, color='lightblue', label='Operating Revenue' if i == 0 else "")
        
    # 绘制净利润和归母净利润
    for i in x:
        ax1_right.bar(i + offset, net_profit[i], width=width, color='forestgreen', label='Net Profit' if i == 0 else "")
        ax1_right.bar(i + offset, parent_net_profit[i], width=width, color='limegreen', label='Parent Net Profit' if i == 0 else "")

    # 左轴设置
    ax1.set_title('Financial Performance Comparison')
    ax1.set_ylabel('Revenue (Billion)', color='royalblue')
    ax1.tick_params(axis='y', colors='royalblue')
    ax1.set_xticks(x)
    ax1.set_xticklabels([date.strftime('%Y%m%d') for date in df.index.tolist()])
    
    # 右轴设置
    ax1_right.set_ylabel('Profit (Billion)', color='forestgreen')
    ax1_right.tick_params(axis='y', colors='forestgreen')

    # 添加一些格式化设置，使两个y轴的零值水平线对齐
    min_profit = min(net_profit)
    ax1_min = -1 * abs(min(net_profit)*1.2 / (max(net_profit)*1.2)) * (max(operating_revenue)*1.1) if min_profit < 0 else 0
    ax1_right_min = min(net_profit)*1.2 if min_profit < 0 else 0
    ax1.set_ylim(bottom=ax1_min, top=max(operating_revenue)*1.2)
    ax1_right.set_ylim(bottom=ax1_right_min, top=max(net_profit)*1.2)

    # 合并图例
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_right.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # 下子图配置
    width2 = 0.15  # 每个柱子的宽度
    positions = [-0.3, -0.1, 0.1, 0.3]  # 四个柱子的位置偏移

    # 绘制四个费用柱状图
    for i in x:
        ax2.bar(i + positions[0], sales_expense[i], width2, color='tomato', label='Sales' if i == 0 else "")
        ax2.bar(i + positions[1], management_expense[i], width2, color='gold', label='Management' if i == 0 else "")
        ax2.bar(i + positions[2], financial_expense[i], width2, color='limegreen', label='Financial' if i == 0 else "")
        ax2.bar(i + positions[3], rd_expense[i], width2, color='cornflowerblue', label='R&D' if i == 0 else "")

    ax2.set_title('Expense Breakdown')
    ax2.set_ylabel('Amount (Million)')
    ax2.set_xticks(x)
    ax2.set_xticklabels([date.strftime('%Y%m%d') for date in df.index.tolist()])
    ax2.legend(loc='upper left')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    # 调整x轴标签角度
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    ts_name = '燕京啤酒'
    ts_name = '五粮液'
    start_date, end_date = '20170101', '20250315'
    main(ts_name, start_date, end_date)