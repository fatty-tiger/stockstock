import os
token = os.environ['TUSHARE_TOKEN']

import tushare as ts

pro = ts.pro_api(token)

#查询当前所有正常上市交易的股票列表
# df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# df.to_json('data/all_stocks.json')
# df.to_csv('data/all_stocks.tsv', sep='\t', index=None)


# df = pro.index_basic(market='SZSE')
# df.to_csv('data/szse_indexs.tsv', sep='\t', index=None)


# df = pro.fund_basic(market='E')
# df.to_csv('data/inside_funds.tsv', sep='\t', index=None)

df = pro.fund_portfolio(ts_code='512890.SH')
df.to_csv('data/512890.SH.tsv', sep='\t', index=None)