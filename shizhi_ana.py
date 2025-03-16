import tushare as ts
import config
import statistics
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pro = ts.pro_api(config.token)
# 获取股票滚动市盈率



def main():
    df = pro.daily_basic(ts_code='000423.SZ', start_date='20150101', end_date='20250313', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pe_ttm,pb')
    data = df.pe_ttm.tolist()

    # 输入分桶数量
    k = 20
    
    # 计算分界点，确保包含最大值
    min_val = min(data)
    # max_val = max(data)
    max_val = 150
    epsilon = 1e-8  # 防止因浮点精度问题导致最大值被排除
    max_val += epsilon
    width = (max_val - min_val) / k
    bins = [min_val + i * width for i in range(k + 1)]
    
    # 统计每个桶的频率
    counts, _ = np.histogram(data, bins=bins)
    
    # 计算均值和标准差
    mean_val = np.mean(data)
    std_val = np.std(data)
    
    # 输出结果
    print("\nBucket Boundaries:")
    print(bins)
    
    print("\nFrequencies per Bucket:")
    for i in range(k):
        print(f"Bucket {i+1}: [{bins[i]:.4f}, {bins[i+1]:.4f}) has {counts[i]} elements")
    
    print(f"\nEstimated Mean: {mean_val:.4f}")
    print(f"Estimated Standard Deviation: {std_val:.4f}")
    
    # 绘制图表
    plt.figure(figsize=(12, 6))
    plt.plot(data, marker='o', linestyle='-', linewidth=2, markersize=8, label='Original Data')
    
    # 绘制均线（均值水平线）
    plt.axhline(y=mean_val, color='r', linestyle='--', linewidth=2, label='Mean')
    
    # 绘制±1标准差虚线
    upper = mean_val + std_val
    lower = mean_val - std_val
    plt.axhline(y=upper, color='g', linestyle=':', linewidth=2, label='+1σ')
    plt.axhline(y=lower, color='g', linestyle=':', linewidth=2, label='-1σ')
    
    # 图表装饰
    plt.title('Data Distribution with Mean and ±1σ Boundaries')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def test():
    #df = pro.daily_basic(ts_code='000423.SZ', start_date='20180101', end_date='20250313', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pe_ttm,pb')
    #df = pro.daily_basic(ts_code='000977.SZ', start_date='20180101', end_date='20250313', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pe_ttm,pb')
    #df = pro.daily_basic(ts_code='000858.SZ', start_date='20170101', end_date='20250313', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pe_ttm,pb')
    #df = pro.daily_basic(ts_code='600809.SH', start_date='20100101', end_date='20250313', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pe_ttm,pb')
    # df = pro.daily_basic(ts_code='000799.SZ', start_date='20170101', end_date='20250313', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pe_ttm,pb')
    # 山西汾酒
    # df = pro.daily_basic(ts_code='600809.SH', start_date='20170101', end_date='20250313', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pe_ttm,pb')
    # 洋河股份
    df = pro.daily_basic(ts_code='002304.SZ', start_date='20170101', end_date='20250313', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pe_ttm,pb')
    
    # df = pro.daily_basic(ts_code='601919.SH', start_date='20170101', end_date='20250313', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pe_ttm,pb')
    # df = pro.daily_basic(ts_code='600026.SH', start_date='20170101', end_date='20250313', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pe_ttm,pb')
    
    df = df.sort_values(by='trade_date')

    # 确保日期列被转换为 datetime
    df['trade_datetime'] = pd.to_datetime(df['trade_date'])

    # 只保留日期为星期五的行
    df = df[df['trade_datetime'].dt.weekday == 4]
    print(df.head())

    dates = df.trade_datetime.tolist()
    # datas = [x for x in df.pe.tolist() if isinstance(x, float)]
    datas = [x for x in df.pe_ttm.tolist() if isinstance(x, float)]
    datas_for_mean_std = [x for x in datas if not np.isnan(x)]
    # print(datas[:10])
    # print(type(datas[0]))
    
    # 计算统计量
    mean_val = statistics.mean(datas_for_mean_std)
    std_dev_val = statistics.stdev(datas_for_mean_std)
    # 第二步：计算每个数值与均值之差的平方，然后求和
    # squared_diff_sum = sum((x - mean_val) ** 2 for x in datas_for_mean_std)
    # std_dev_val = math.sqrt(squared_diff_sum / len(datas_for_mean_std))
    print('mean_val', mean_val)
    print('std_dev_val', std_dev_val)

    # 绘制图表
    plt.figure(figsize=(10, 5))
    plt.plot(dates, datas, label='Data', marker='o')

    # 绘制均值和标准差线
    plt.axhline(y=mean_val, color='r', linestyle='--', label='Mean')
    plt.axhline(y=mean_val + std_dev_val, color='g', linestyle='--', label='Mean + Std Dev')
    plt.axhline(y=mean_val - std_dev_val, color='b', linestyle='--', label='Mean - Std Dev')

    # 设置x轴日期格式
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y%m%d'))
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记

    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Data with Mean and Standard Deviation')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    test()
    # 示例数据集
    # data = [4.0, 8.0, 6.0, 5.0, 3.0, 2.0, 8.0, 9.0, 2.0, 5.0]
    # print(type(data[0]))
    # # 计算标准差
    # std_dev_value = statistics.stdev(data)
    # print(std_dev_value)