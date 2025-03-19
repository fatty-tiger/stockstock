import os
token = os.environ['TUSHARE_TOKEN']

import tushare as ts
import statistics
import pandas as pd
import matplotlib.pyplot as plt


from cache_util import StockInfoCache

stock_info_cache = StockInfoCache()


pro = ts.pro_api(token)
# 获取股票滚动市盈率

def main(ts_name, start_date, end_date, period):
    ts_code = stock_info_cache.get_code_by_name(ts_name)

    df = pro.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date, fields='ts_code,trade_date,pe,pe_ttm,close,dv_ttm')
    df = df.sort_values(by='trade_date')
    # df['trade_datetime'] = 
    df.index = pd.to_datetime(df['trade_date'])

    df.interpolate(method='time', inplace=True)

    if period == 'W':
        # 只保留日期为星期五的行
        df = df[df.index.dayofweek == 4]
    elif period == 'M':
        df = df[df.index.isin(df.groupby([df.index.year, df.index.month]).apply(lambda x: x.index.max()).values)]
    
    #dates = df.index.tolist()
    #datas = [x for x in df.pe_ttm.tolist() if isinstance(x, float)]    
    # 计算统计量
    mean_val = statistics.mean(df.pe_ttm)
    std_dev_val = statistics.stdev(df.pe_ttm)
    quartiles = statistics.quantiles(df.pe_ttm, n=4)
    print('mean_val', mean_val)
    print('std_dev_val', std_dev_val)
    print('quartiles', quartiles)

    # 绘制图表
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df.pe_ttm, 'b-', label='pe_ttm', marker='o')
    plt.plot(df.index, df.close, 'r--', label='price', marker='o')

    # 绘制均值和标准差线
    plt.axhline(y=mean_val, color='g', linestyle='--', label='Mean')
    plt.axhline(y=mean_val + std_dev_val, color='r', linestyle='--', label='Mean + Std Dev')
    plt.axhline(y=mean_val - std_dev_val, color='b', linestyle='--', label='Mean - Std Dev')
    plt.axhline(y=quartiles[2], color='r', linestyle='-.', label='75% percetile')
    plt.axhline(y=quartiles[1], color='g', linestyle='-.', label='50% percetile')
    plt.axhline(y=quartiles[0], color='b', linestyle='-.', label='25% percetile')

    # 设置x轴日期格式
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y%m%d'))
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记

    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Data with Mean and Standard Deviation')
    plt.legend()
    plt.show()


# 解决方案：使每个y轴的spine可见
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def main2(ts_name, start_date, end_date, period):
    ts_code = stock_info_cache.get_code_by_name(ts_name)

    df = pro.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date, fields='ts_code,trade_date,pe,pe_ttm,close,dv_ttm')
    df = df.sort_values(by='trade_date')
    df.index = pd.to_datetime(df['trade_date'])

    df.interpolate(method='time', inplace=True)

    if period == 'W':
        # 只保留日期为星期五的行
        df = df[df.index.dayofweek == 4]
    elif period == 'M':
        df = df[df.index.isin(df.groupby([df.index.year, df.index.month]).apply(lambda x: x.index.max()).values)]
    
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

    # 设置图表标题
    plt.title(f'Stock basic analysis of {ts_code}')

    # 显示图例
    fig.legend(loc="upper left")

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
    ts_name = '双汇发展'
    ts_name = '中国神华'
    # ts_name = '贵州茅台'
    ts_name = '华菱钢铁'
    ts_name = '洛阳钼业'
    start_date, end_date = '20040101', '20250315'
    # start_date, end_date = '20040101', '20211231'
    period = 'M'
    main2(ts_name, start_date, end_date, period)
    # test(ts_name, start_date, end_date, period)