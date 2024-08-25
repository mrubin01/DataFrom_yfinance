import warnings
import pandas as pd
import numpy as np
import yfinance as yf
import functions
import fundamentals
import variables
import h5py

warnings.filterwarnings('ignore')

only_two_years = ['2019', '2020']
ticker = ['ABR', 'MSFT', 'ADX', 'ADEE']
diz_2019 = {}
avg_close_perc_2020 = []
# all_statements = functions.get_fundamentals('AWP', variables.years)

#title = 'yfinance_data2020_2023'
#pd.read_hdf(title, "/Users/madararubino/PycharmProjects/DataFrom_yfinance/yfinance_data2020_2023")

#f = h5py.File('yfinance_data2020_2023', 'r')
#dset = f.create_dataset('df')

# for y in variables.years:
#     for f in fundamentals.fundamentals:
#         print(df[y, 'EBIDTA'])

# select a row with every columns df.xs('ABT') OR df.xs(key='ACN')
# select an entire column highest level df.xs('2020', axis=1)
#values = df.loc[:, ('2020', 'EBIDTA')]
#loc[:, (quarters_to_train, features_to_train)]

my_file = open("active_tickers.txt", "r")
d = my_file.read()
data_into_list = d.replace('\n', ', ').split(", ")
ticker_list = list(filter(None, data_into_list))
ticker0 = ticker_list[0]

years = variables.years
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

# Create a df using only the features with no gaps or with < 5%
tckrs = ['A', 'AA', 'AAT', 'AB', 'ABBV', 'ABM', 'ABR', 'ABT', 'ACM', 'ACN']
df_subset = df.loc[df_tickers, (variables.years, features)]
#df_subset = df.loc[tckrs, (variables.years, features)]
print(df_tickers)

# FROM A SUBSET OF THE DF WITH 12+8 FEATURES, TRY TO FILL THE GAPS

no_rows = len(df_subset) - 2  # subtract the two-level column name
no_tickers = len(df_subset.columns)
tickers_no_gaps = []
tickers_with_gaps = []

for t in tckrs:
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
    for i in tckrs:
        d = df_subset.loc[i, ("2023", f)][0]
        c = df_subset.loc[i, ("2022", f)][0]
        b = df_subset.loc[i, ("2021", f)][0]
        a = df_subset.loc[i, ("2020", f)][0]

        if not pd.isnull(d) and (pd.isnull(a) and pd.isnull(b) and pd.isnull(c)):
            df_subset.loc[i, ("2020", f)][0] = df_subset.loc[i, ("2023", f)][0]
            df_subset.loc[i, ("2021", f)][0] = df_subset.loc[i, ("2023", f)][0]
            df_subset.loc[i, ("2022", f)][0] = df_subset.loc[i, ("2023", f)][0]
        # this scan backward
        if pd.isnull(d) and not pd.isnull(c):
            df_subset.loc[i, ("2023", f)][0] = df_subset.loc[i, ("2022", f)][0]
        if pd.isnull(c) and not pd.isnull(b):
            df_subset.loc[i, ("2022", f)][0] = df_subset.loc[i, ("2021", f)][0]
        if pd.isnull(b) and not pd.isnull(a):
            df_subset.loc[i, ("2021", f)][0] = df_subset.loc[i, ("2020", f)][0]
        # this scan forward
        if pd.isnull(a) and not pd.isnull(b):
            df_subset.loc[i, ("2020", f)][0] = df_subset.loc[i, ("2021", f)][0]
        if pd.isnull(a) and pd.isnull(b) and not pd.isnull(c):
            df_subset.loc[i, ("2020", f)][0] = df_subset.loc[i, ("2022", f)][0]
            df_subset.loc[i, ("2021", f)][0] = df_subset.loc[i, ("2022", f)][0]
        if pd.isnull(a) and pd.isnull(b) and pd.isnull(c) and not pd.isnull(d):
            df_subset.loc[i, ("2020", f)][0] = df_subset.loc[i, ("2023", f)][0]
            df_subset.loc[i, ("2021", f)][0] = df_subset.loc[i, ("2023", f)][0]
            df_subset.loc[i, ("2022", f)][0] = df_subset.loc[i, ("2023", f)][0]

#functions.print_feature_gaps_from_df(df_subset, features)
tickers_no_gaps = []
tickers_with_gaps = []

for t in tckrs:
    try:
        perc = float(round(df_subset.loc[t].isnull().sum(axis=1) / no_tickers * 100, 2))
        if perc > 0:
            tickers_with_gaps.append(t)
        else:
            tickers_no_gaps.append(t)
        #print(t + ' ' + str(perc[0]))
    except Exception:
        pass

print('After scanning...')
print('Tickers with no gaps ' + str(len(tickers_no_gaps)))
print('Tickers with gaps ' + str(len(tickers_with_gaps)))
print(df_subset.isnull().sum().sum())
print()

"""
12 Features with no gaps:
Normalized Income
Net Income
Pretax Income
Total Revenue
Operating Revenue
Total Liabilities Net Minority Interest 
Tangible Book Value 
Net Tangible Assets 
Common Stock Equity 
Stockholders Equity 
Total Assets 
Free Cash Flow

8 Features with gaps < 5%
Net Interest Income
Diluted EPS
Basic EPS
Selling General And Administration
Ordinary Shares Number 
Total Debt 
Capital Stock 
Common Stock 
"""
