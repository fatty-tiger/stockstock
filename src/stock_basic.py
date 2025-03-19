import os
token = os.environ['TUSHARE_TOKEN']

import tushare as ts
import numpy as np
import statistics
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot

from cache_util import StockInfoCache

stock_info_cache = StockInfoCache()


pro = ts.pro_api(token)
# 获取股票滚动市盈率

# 解决方案：使每个y轴的spine可见
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def main(ts_name, start_date, end_date, period):
    ts_code = stock_info_cache.get_code_by_name(ts_name)

    # df = pro.income(ts_code='000799.SZ', start_date='20220101', end_date='20250301', 
    #     fields='ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,total_revenue,revenue,n_income')
    

    df = pro.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date, fields='ts_code,trade_date,pe,pe_ttm,close,dv_ttm')
    df = df.sort_values(by='trade_date')
    df.index = pd.to_datetime(df['trade_date'])
    df['pe_ttm'] = [min(100, x) if isinstance(x, float) else np.nan for x in df.pe_ttm.tolist()]

    df.interpolate(method='time', inplace=True)

    if period == 'W':
        # 只保留日期为星期五的行
        df = df[df.index.dayofweek == 4]
    elif period == 'M':
        df = df[df.index.isin(df.groupby([df.index.year, df.index.month]).apply(lambda x: x.index.max()).values)]
    
    df2 = pro.income(
        ts_code=ts_code, start_date=start_date, end_date=end_date,
        fields='ts_code,end_date,report_type,comp_type,total_revenue,n_income')
    df2['n_income'] = df2['n_income'] / 1e8
    df2.index = pd.to_datetime(df2['end_date'])
    
    df_joined = df.join(df2, how='inner', lsuffix='_x', rsuffix='_y')
    df_joined = df_joined[~df_joined.index.duplicated(keep='first')]
    # print(df_joined.head())
    

    #dates = df.index.tolist()
    #datas = [x for x in df.pe_ttm.tolist() if isinstance(x, float)]    
    # 计算统计量
    mean_val = statistics.mean(df.pe_ttm)
    std_dev_val = statistics.stdev(df.pe_ttm)
    quartiles = statistics.quantiles(df.pe_ttm, n=4)
    print('mean_val', mean_val)
    print('std_dev_val', std_dev_val)
    print('quartiles', quartiles)

    # 创建图形和第一个坐标轴
    fig, ax1 = plt.subplots()

    # 在第一个坐标轴上绘制第一条折线图
    ax1.plot(df.index, df.pe_ttm, 'b-', label='pe_ttm', marker='^')
    ax1.axhline(y=mean_val, color='g', linestyle='--', label='Mean of pe_ttm')
    ax1.axhline(y=mean_val + std_dev_val, color='r', linestyle='--', label='Mean+StdDev of pe_ttm')
    ax1.axhline(y=mean_val - std_dev_val, color='b', linestyle='--', label='Mean-StdDev of pe_ttm')
    ax1.axhline(y=quartiles[2], color='r', linestyle='-.', label='75% Percetile of pe_ttm')
    ax1.axhline(y=quartiles[1], color='g', linestyle='-.', label='50% Percetile of pe_ttm')
    ax1.axhline(y=quartiles[0], color='b', linestyle='-.', label='25% Percetile of pe_ttm')

    ax1.set_xlabel('Date')
    ax1.set_ylabel('pe_ttm', color='b')
    ax1.tick_params(axis='y', labelcolor='b')


    # 使用twinx()创建第二个坐标轴，与第一个共享X轴
    ax2 = ax1.twinx()
    # 在第二个坐标轴上绘制第二条折线图
    ax2.plot(df.index, df.close, 'r--', label='price', marker='*')
    ax2.set_ylabel('price', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    ax22 = ax1.twinx()
    
    # 调整第二个副y轴的位置，使其不与第一个重叠
    ax22.spines["right"].set_position(("axes", 1.05))
    make_patch_spines_invisible(ax22)
    ax22.spines["right"].set_visible(True)
    ax22.plot(df.index, df.dv_ttm, 'y--', label='dv_ttm', marker='o')
    ax22.set_ylabel('dv_ttm', color='y')
    ax22.tick_params(axis='y', labelcolor='y')

    ax3 = ax1.twinx()
    # 调整第二个副y轴的位置，使其不与第一个重叠
    ax3.spines["left"].set_position(("axes", -1.05))
    make_patch_spines_invisible(ax3)
    ax3.spines["left"].set_visible(True)
    ax3.bar(df_joined.index, df_joined.n_income)
    ax3.set_ylabel('n_income', color='c')
    ax3.tick_params(axis='y', labelcolor='c')

    # 设置图表标题
    plt.title(f'Stock basic analysis of {ts_code}')

    # 显示图例
    fig.legend(loc="upper left")

    # 展示图形
    plt.show()


def main2(ts_name, start_date, end_date, period):
    ts_code = stock_info_cache.get_code_by_name(ts_name)

    df = pro.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date, fields='ts_code,trade_date,pe,pe_ttm,close,dv_ttm')
    df = df.sort_values(by='trade_date')
    df.index = pd.to_datetime(df['trade_date'])
    df['pe_ttm'] = [min(100, x) if isinstance(x, float) else np.nan for x in df.pe_ttm.tolist()]

    df.interpolate(method='time', inplace=True)

    if period == 'W':
        # 只保留日期为星期五的行
        df = df[df.index.dayofweek == 4]
    elif period == 'M':
        df = df[df.index.isin(df.groupby([df.index.year, df.index.month]).apply(lambda x: x.index.max()).values)]
    # print(df)

    df2 = pro.income(
        ts_code=ts_code, start_date=start_date, end_date=end_date,
        fields='ts_code,end_date,report_type,comp_type,total_revenue,n_income')
    df2.rename(columns={'end_date': 'trade_date'}, inplace=True)
    #df2['n_income'] = df2['n_income'] / 1e8
    df2['n_income'] = [x / 1e8 if x > 0 else 0 for x in df2.n_income.tolist()]
    df2.index = pd.to_datetime(df2['trade_date'])
    df2 = df2[~df2.index.duplicated(keep='first')]
    # print(df2)
    
    # df_joined = df.join(df2, how='inner', lsuffix='_x', rsuffix='_y')
    # print(df_joined)


    #dates = df.index.tolist()
    #datas = [x for x in df.pe_ttm.tolist() if isinstance(x, float)]    
    # 计算统计量
    mean_val = statistics.mean(df.pe_ttm)
    std_dev_val = statistics.stdev(df.pe_ttm)
    quartiles = statistics.quantiles(df.pe_ttm, n=4)
    print('mean_val', mean_val)
    print('std_dev_val', std_dev_val)
    print('quartiles', quartiles)

    # 创建图形和第一个坐标轴
    host = host_subplot(111)
    ax1 = host.twinx()  # 第一个副y轴
    ax2 = host.twinx()  # 第二个副y轴
    ax3 = host.twinx()  # 第三个副y轴

    # 在第一个坐标轴上绘制第一条折线图
    host.plot(df.index, df.pe_ttm, 'b-', label='pe_ttm', marker='^')
    host.axhline(y=mean_val, color='g', linestyle='--', label='Mean of pe_ttm')
    host.axhline(y=mean_val + std_dev_val, color='r', linestyle='--', label='Mean+StdDev of pe_ttm')
    host.axhline(y=mean_val - std_dev_val, color='b', linestyle='--', label='Mean-StdDev of pe_ttm')
    host.axhline(y=quartiles[2], color='r', linestyle='-.', label='75% Percetile of pe_ttm')
    host.axhline(y=quartiles[1], color='g', linestyle='-.', label='50% Percetile of pe_ttm')
    host.axhline(y=quartiles[0], color='b', linestyle='-.', label='25% Percetile of pe_ttm')
    host.set_xlabel('Date')
    host.set_ylabel('pe_ttm', color='b')
    host.tick_params(axis='y', labelcolor='b')

    bars = ax1.bar(df2.index, df2.n_income, width=20)
    # 在每个柱形的上方添加文本
    for bar in bars:
        yval = bar.get_height()  # 获取柱的高度
        ax1.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    ax2.spines["right"].set_position(("axes", 1.04))
    make_patch_spines_invisible(ax2)
    ax2.spines["right"].set_visible(True)
    ax2.plot(df.index, df.close, 'r--', label='price', marker='*')
    ax2.set_ylabel('price', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    ax3.spines["right"].set_position(("axes", 1.08))
    make_patch_spines_invisible(ax3)
    ax3.spines["right"].set_visible(True)
    ax3.plot(df.index, df.dv_ttm, 'y--', label='dv_ttm', marker='o')
    ax3.set_ylabel('dv_ttm', color='y')
    ax3.tick_params(axis='y', labelcolor='y')

    # ax3.spines["right"].set_position(("axes", 1.25))
    # make_patch_spines_invisible(ax3)
    # ax3.spines["right"].set_visible(True)
    

    # 设置图表标题
    plt.title(f'Stock basic analysis of {ts_code}')

    # 显示图例
    plt.legend(loc="upper left")

    # 展示图形
    plt.show()

def test(ts_name, start_date, end_date, period):
    ts_code = stock_info_cache.get_code_by_name(ts_name)
    df = pro.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date, fields='ts_code,trade_date,pe,pe_ttm')
    df = df.sort_values(by='trade_date')
    print(df)



if __name__ == "__main__":
    ts_name = '东阿阿胶'
    ts_name = '山西汾酒'
    ts_name = '五粮液'
    # ts_name = '双汇发展'
    ts_name = '中国神华'
    # ts_name = '贵州茅台'
    # ts_name = '华菱钢铁'
    # ts_name = '洛阳钼业'
    ts_name = '燕京啤酒'
    # ts_name = ['顺丰控股', '申通快递', '韵达股份'][0]
    start_date, end_date = '20170101', '20250315'
    # start_date, end_date = '20100101', '20241231'
    period = 'M'
    main2(ts_name, start_date, end_date, period)
    
    # test(ts_name, start_date, end_date, period)