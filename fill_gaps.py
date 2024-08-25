import numpy as np
import pandas as pd
import datetime as dt
import io
import json
import requests
import requests_html
import h5py as h5
import time
import functions
import fundamentals
import variables
import warnings
import csv
import yfinance as yf
warnings.filterwarnings('ignore')

"""
The starting point is the file yfinance_data2020_2023 which contains tickers with data for every year from
2020 to 2023. Tickers with missing years are in yfinance_tickers_with_missing_years.csv.

By using the functions print_feature_gaps_from_df or print_feature_gaps_from_file, there are only 12 features 
with no gaps and 8 with a low percentage of gaps (< 5%).

12 Features with no gaps: Normalized Income IS Net Income IS Pretax Income IS, Total Revenue IS, Operating Revenue IS
,Total Liabilities Net Minority Interest BS, Tangible Book Value BS, Net Tangible Assets BS, Common Stock Equity BS,
Stockholders Equity BS, Total Assets BS, Free Cash Flow CF

8 Features with gaps < 5%: Net Interest Income IS, Diluted EPS IS, Basic EPS IS, Selling General And Administration IS, 
Ordinary Shares Number BS, Total Debt BS, Capital Stock BS, Common Stock BS

With these 20 features I will try to fill the gaps by using these passes:
- if 2023 has a value while the other years are empty, fill the gaps with 2023
- if year y is empty but y-1 has a value, use that value (backward scan)
- if year y is empty but y+1 has a value, use that value (forward scan)

After these passes, the tickers with gaps decrease from 525 to 166 (out of 1522),
the gaps from 1594 to 707. 1356 tickers with no gaps will be used

"""

# file with the dataset
file_name = "yfinance_data2020_2023"

# create a multiindex df
index_list = [0, 1]
data = pd.read_hdf(f"{file_name}", header=index_list, index_col=0, na_values=[0])
df = pd.DataFrame(data)

# extract the tickers as a list
df_tuple_indexes = df.index.values.tolist()
df_tickers = []
for i in df_tuple_indexes:
    df_tickers.append(i[0])

print("Tickers no. " + str(len(df_tickers)))
print()

selected_features = ["Increase %", "Increase %", "Increase %", "Increase %", "Avg Close", "Avg High", "Avg Low",
                     "Avg Vol", "Normalized Income", "Net Income", "Pretax Income", "Total Revenue", "Operating Revenue",
                     "Total Liabilities Net Minority Interest", "Tangible Book Value", "Net Tangible Assets",
                     "Common Stock Equity", "Stockholders Equity", "Total Assets", "Free Cash Flow",
                     "Net Interest Income", "Diluted EPS", "Basic EPS", "Selling General And Administration",
                     "Ordinary Shares Number", "Total Debt", "Capital Stock", "Common Stock"]

# create a new df with a selected numbers of features (those with gaps < 5%)
df_subset = df.loc[df_tickers, (variables.years, selected_features)]

# list variables that will contain tickers with no gaps and those with gaps
tickers_no_gaps = []
tickers_with_gaps = []

# compute the number of gaps before scanning
for t in df_tickers:
    try:
        perc = float(round(df_subset.loc[t].isnull().sum(axis=1) / len(df_tickers) * 100, 2))
        if perc > 0:
            tickers_with_gaps.append(t)
        else:
            tickers_no_gaps.append(t)
    except Exception:
        tickers_with_gaps.append(t)
        pass

print('Before scanning...')
print('Tickers with no gaps ' + str(len(tickers_no_gaps)))
print('Tickers with gaps ' + str(len(tickers_with_gaps)))
print(df_subset.isnull().sum().sum())
print()


# Scan the df to fill as many gaps as possible
for f in selected_features:
    for i in df_tickers:
        d = df_subset.loc[i, ("2023", f)][0]
        c = df_subset.loc[i, ("2022", f)][0]
        b = df_subset.loc[i, ("2021", f)][0]
        a = df_subset.loc[i, ("2020", f)][0]
        # if we have only the most recent value, replace the gaps with this one
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

# set the ticker lists to be empty and recompute the gaps
tickers_no_gaps = []
tickers_with_gaps = []

for t in df_tickers:
    try:
        perc = float(round(df_subset.loc[t].isnull().sum(axis=1) / len(df_tickers) * 100, 2))
        if perc > 0:
            tickers_with_gaps.append(t)
        else:
            tickers_no_gaps.append(t)
    except Exception:
        tickers_with_gaps.append(t)
        pass

print('After scanning...')
print('Tickers with no gaps ' + str(len(tickers_no_gaps)))
print('Tickers with gaps ' + str(len(tickers_with_gaps)))
print(df_subset.isnull().sum().sum())
print()

# drop tickers with gaps
final_data = df_subset.drop(tickers_with_gaps)

store_df_subset = True

if store_df_subset:
    title = 'final_data_2020_2023'
    path = '/Users/madararubino/PycharmProjects/DataFrom_yfinance'
    functions.write_to_csv(final_data, title)
    functions.write_to_h5(final_data, title, path)

    # with open('yfinance_tickers_with_gaps.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(tickers_with_gaps)

    # store tickers with gaps and with gaps into txt files
    title1 = 'yfinance_tickers_with_no_gaps'
    functions.write_list_to_txt(tickers_no_gaps, title1)
    title2 = 'yfinance_tickers_with_gaps'
    functions.write_list_to_txt(tickers_with_gaps, title2)
