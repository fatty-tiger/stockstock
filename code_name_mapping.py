import config
import tushare as ts

pro = ts.pro_api(config.token)

#查询当前所有正常上市交易的股票列表
df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
#df.to_json('data/all_stocks.json')
df.to_csv('data/all_stocks.tsv', sep='\t', index=None)
# codes = df.ts_code.tolist()
# names = df.name.tolist()
# with open('all_stocks.tsv', 'w', encoding='utf8') as wr:
#     for x, y in zip(codes, names):
#         wr.write(x + '\t' + y + '\n')
