import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def demo1():        
    # 示例数据
    data = {
        'date': ['230101', '230102', '230103', '230104'], # yyMMdd格式的日期
        'series1': [5, 7, 2, 8],
        'series2': [3, 6, 5, 4],
    }

    # 将数据转换为DataFrame
    df = pd.DataFrame(data)

    # 将'date'列转换为datetime类型
    df['date'] = pd.to_datetime(df['date'], format='%y%m%d')

    # 创建图形和子图
    fig, ax = plt.subplots()

    # 设置柱形图的位置
    bar_width = 0.35
    index = df.index

    # 绘制第一个序列的柱形图
    bar1 = ax.bar(index - bar_width/2, df['series1'], bar_width, label='Series 1')

    # 绘制第二个序列的柱形图
    bar2 = ax.bar(index + bar_width/2, df['series2'], bar_width, label='Series 2')

    # 设置x轴属性
    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    ax.set_title('Dual Bar Chart with Date on X-axis')
    ax.set_xticks(index)
    ax.set_xticklabels(df['date'].dt.strftime('%y%m%d')) # 格式化日期显示

    # 添加图例
    ax.legend()

    # 显示图表
    plt.show()

demo1()