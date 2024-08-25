import warnings
import pandas as pd
import numpy as np
import sys
import functions
import fundamentals
import variables
from contextlib import suppress

warnings.filterwarnings('ignore')


features = ["Increase %", "Increase %", "Increase %", "Increase %", "Avg Close", "Avg High", "Avg Low", "Avg Vol",
            "Normalized Income", "Net Income", "Pretax Income", "Total Revenue", "Operating Revenue",
            "Total Liabilities Net Minority Interest", "Tangible Book Value", "Net Tangible Assets",
            "Common Stock Equity", "Stockholders Equity", "Total Assets", "Free Cash Flow",
            "Net Interest Income", "Diluted EPS", "Basic EPS", "Selling General And Administration",
            "Ordinary Shares Number", "Total Debt", "Capital Stock", "Common Stock"
            ]

index_list = [0, 1]

data = pd.read_hdf('yfinance_data2020_2023', header=index_list, index_col=0, na_values=[0])
df = pd.DataFrame(data)

# extract the tickers as a list
df_indexes = df.index.values.tolist()
df_tickers = []
for i in df_indexes:
    df_tickers.append(i[0])

df_subset = df.loc[df_tickers, (variables.years, features)]

no_tickers = len(df_tickers)
tickers_no_gaps = []
tickers_with_gaps = []

print("Tickers no. " + str(no_tickers))

# compute the number of gaps before scanning
for t in df_tickers:
    try:
        perc = float(round(df_subset.loc[t].isnull().sum(axis=1) / no_tickers * 100, 2))
        if perc > 0:
            tickers_with_gaps.append(t)
        else:
            tickers_no_gaps.append(t)
        #print(t + ' ' + str(perc[0]))
    except Exception:
        pass

print('Before scanning...')
print('Tickers with no gaps ' + str(len(tickers_no_gaps)))
print('Tickers with gaps ' + str(len(tickers_with_gaps)))
print(df_subset.isnull().sum().sum())
print()

for f in features:
    for i in df_tickers:
        d = df_subset.loc[i, ("2023", f)][0]
        c = df_subset.loc[i, ("2022", f)][0]
        b = df_subset.loc[i, ("2021", f)][0]
        a = df_subset.loc[i, ("2020", f)][0]

        if not pd.isnull(d) and (pd.isnull(a) and pd.isnull(b) and pd.isnull(c)):
            df_subset.loc[i, ("2020", f)] = df_subset.loc[i, ("2023", f)]
            df_subset.loc[i, ("2021", f)] = df_subset.loc[i, ("2023", f)]
            df_subset.loc[i, ("2022", f)] = df_subset.loc[i, ("2023", f)]
        # this scan backward
        if pd.isnull(d) and not pd.isnull(c):
            df_subset.loc[i, ("2023", f)] = df_subset.loc[i, ("2022", f)]
        if pd.isnull(c) and not pd.isnull(b):
            df_subset.loc[i, ("2022", f)] = df_subset.loc[i, ("2021", f)]
        if pd.isnull(b) and not pd.isnull(a):
            df_subset.loc[i, ("2021", f)] = df_subset.loc[i, ("2020", f)]
        # this scan forward
        if pd.isnull(a) and not pd.isnull(b):
            df_subset.loc[i, ("2020", f)] = df_subset.loc[i, ("2021", f)]
        if pd.isnull(a) and pd.isnull(b) and not pd.isnull(c):
            df_subset.loc[i, ("2020", f)] = df_subset.loc[i, ("2022", f)]
            df_subset.loc[i, ("2021", f)] = df_subset.loc[i, ("2022", f)]
        if pd.isnull(a) and pd.isnull(b) and pd.isnull(c) and not pd.isnull(d):
            df_subset.loc[i, ("2020", f)] = df_subset.loc[i, ("2023", f)]
            df_subset.loc[i, ("2021", f)] = df_subset.loc[i, ("2023", f)]
            df_subset.loc[i, ("2022", f)] = df_subset.loc[i, ("2023", f)]


tickers_no_gaps_final = []
tickers_with_gaps_final = []

for t in df_tickers:
    try:
        perc = float(round(df_subset.loc[t].isnull().sum(axis=1) / no_tickers * 100, 2))
        if perc > 0:
            tickers_with_gaps_final.append(t)
        else:
            tickers_no_gaps_final.append(t)
        #print(t + ' ' + str(perc[0]))
    except Exception:
        pass

print('After scanning...')
print('Tickers with no gaps ' + str(len(tickers_no_gaps_final)))
print('Tickers with gaps ' + str(len(tickers_with_gaps_final)))
print(df_subset.isnull().sum().sum())
print()
