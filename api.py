"""
examples
"""
import tushare as ts
import config

pro = ts.pro_api(config.token)

def dailybasic():
    """
    https://tushare.pro/document/2?doc_id=128
    """
    # df = pro.index_dailybasic(
    #     #ts_code='000001.SH',
    #     # ts_code='000423.SZ',
    #     # ts_code='000977.SZ',
    #     trade_date='20240311',
    #     # start_date='20250301',
    #     # end_date='20250310',
    #     fields='ts_code,trade_date,turnover_rate,pe,pe_ttm'
    # )
    df = pro.daily_basic(ts_code='000423.SZ', trade_date='20250310', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pe_ttm,pb')
    #print(df.head())
    #print(df.tail())
    print(df)


def income():
    df = pro.income(
        ts_code='000799.SZ', start_date='20220101', end_date='20250301', 
        fields='ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,total_revenue,revenue,n_income')
    df['total_revenue_yi'] = df['total_revenue'] / 1e8
    df['n_income_yi'] = df['n_income'] / 1e8
    df = df.sort_values(by='end_date')
    print(df)

#dailybasic()
income()