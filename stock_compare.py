import tushare as ts
import config
import matplotlib.pyplot as plt
import pandas as pd

from cache_util import StockBasic

stock_basic = StockBasic()

class StockCompare:
    def __init__(self, name1, name2):
        self.name1 = name1
        self.name2 = name2

        self.ts_code1 = stock_basic.get_code_by_name(name1)
        self.ts_code2 = stock_basic.get_code_by_name(name2)

    def compare_revenue_and_income(self, pro, start_date, end_date):
        df1 = pro.income(ts_code=self.ts_code1, start_date=start_date, end_date=end_date, fields='ts_code,end_date,report_type,comp_type,total_revenue,revenue,n_income')
        df1['total_revenue'] = df1['total_revenue'] / 1e8
        df1['n_income'] = df1['n_income'] / 1e8
        
        df2 = pro.income(ts_code=self.ts_code2, start_date=start_date, end_date=end_date, fields='ts_code,end_date,report_type,comp_type,total_revenue,revenue,n_income')
        df2['total_revenue'] = df2['total_revenue'] / 1e8
        df2['n_income'] = df2['n_income'] / 1e8
        
        df3 = pd.merge(df1, df2, on='end_date', how='outer')
        df3['date'] = pd.to_datetime(df3['end_date'], format='%Y%m%d')
        # print(df3.head())
        # print(df3.index)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True) # 创建共享X轴的上下子图

        bar_width = 0.35

        # 第一个公司图表
        bars1 = ax1.bar(df3.index - bar_width/2, df3['total_revenue_x'], bar_width, label=f'Total Revenue of {self.name1}', color='blue')
        bars2 = ax1.bar(df3.index + bar_width/2, df3['total_revenue_y'], bar_width, label=f'Total Revenue of {self.name2}', color='red')
        ax1.set_ylabel('单位：亿元')
        ax1.legend()

        # 第二个公司图表
        bars3 = ax2.bar(df3.index - bar_width/2, df3['n_income_x'], bar_width, label=f'Net Profit of {self.name1}', color='green')
        bars4 = ax2.bar(df3.index + bar_width/2, df3['n_income_y'], bar_width, label=f'Net Profit of {self.name2}', color='orange')
        ax2.set_ylabel('单位：亿元')
        ax2.legend()

        plt.xlabel('Date')
        plt.suptitle('Comparison of Total Revenue and Net Profit Between Two Companies')
        plt.xticks(df3.index, rotation=45, labels=df3['date'].dt.strftime('%y%m%d'))
        
        # 设置中文字体，这里以SimHei（黑体）为例。请确保你的系统中安装了这个字体。
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

        plt.show()
        

if __name__ == '__main__':
    pro = ts.pro_api(config.token)
    # start_date, end_date = '20240101', '20250313'
    start_date, end_date = '20170101', '20250313'

    name1 = '泸州老窖'
    name1 = '五粮液'
    name1 = '贵州茅台'
    name2 = '山西汾酒'
    comparator = StockCompare(name1, name2)
    comparator.compare_revenue_and_income(pro, start_date, end_date)