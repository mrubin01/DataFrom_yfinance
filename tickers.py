"""
Use this code to filter out the tickers that cannot be used in the main.
Instead, the tickers active from 2019 on, will be stored in active_tickers.txt
STEPS:
- use tickers coming from NYSE and NASDAQ
- the two lists of tickers are merged
- if flag is set to 0, check that tickers are active and store them in a file

"""

import pandas as pd
import functions

ticker_list = []
tickers_to_check_flag = 0


nyse = pd.read_csv('/Users/madararubino/nyse_screener.csv')
nyse_ticks = nyse['Symbol'].values.tolist()

nasdaq = pd.read_csv('/Users/madararubino/nasdaq_screener.csv')
nasdaq_ticks = nasdaq['Symbol'].values.tolist()


for t in nyse_ticks:
    if pd.isnull(t):
        pass
    else:
        if '^' in t:
            t = t.split('^')[0]
        if t not in ticker_list:
            ticker_list.append(t)

for t in nasdaq_ticks:
    if pd.isnull(t):
        pass
    else:
        if '^' in t:
            t = t.split('^')[0]
        if t not in ticker_list:
            ticker_list.append(t)

# Check data for 2019: if no data, remove them from the ticker list and store the new list
# if the flag is set to 1, it will take several minutes to complete
if tickers_to_check_flag:
    functions.check_active_tickers('2019', ticker_list)

