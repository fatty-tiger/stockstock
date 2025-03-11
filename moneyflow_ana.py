import config
import tushare as ts


pro = ts.pro_api(config.token)


#df = pro.moneyflow(ts_code='000977.SZ', start_date='20241227', end_date='20250115')
# df = pro.moneyflow(ts_code='000977.SZ', start_date='20241216', end_date='20250214')
#df = pro.moneyflow(ts_code='000977.SZ', start_date='20250217', end_date='20250311')

# df = pro.moneyflow(ts_code='002714.SZ', start_date='20241101', end_date='20250115')
df = pro.moneyflow(ts_code='002714.SZ', start_date='20250116', end_date='20250311')
df = df.sort_values(by='trade_date')

for k in ['sm', 'md', 'lg', 'elg']:
    df[f'even_{k}_vol'] = df[f'buy_{k}_vol'] - df[f'sell_{k}_vol']
for k in ['sm', 'md', 'lg', 'elg']:
    df[f'cum_even_{k}_vol'] = df[f'even_{k}_vol'].cumsum()
df['cum_net_mf_vol'] = df['net_mf_vol'].cumsum()

show_cols = ['trade_date']
show_cols.extend([f'even_{k}_vol' for k in ['sm', 'md', 'lg', 'elg']])
show_cols.extend([f'cum_even_{k}_vol' for k in ['sm', 'md', 'lg', 'elg']])
show_cols.extend(['net_mf_vol', 'cum_net_mf_vol'])
print(df[show_cols])

# for _, row in df.iterrows():
#     print(row)

# df = pro.margin(trade_date='20250227')
# print(df)


# 集合竞价
# df = pro.stk_auction(ts_code='000977.SZ', trade_date='20250227', fields='ts_code, trade_date,vol,price,amount,turnover_rate,volume_ratio')
# df = pro.stk_auction_o(ts_code='000977.SZ', trade_date='20250227')
# print(df)