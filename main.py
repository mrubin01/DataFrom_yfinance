import numpy as np
import pandas as pd
import functions
import fundamentals
import variables
import warnings
import csv
import yfinance as yf
warnings.filterwarnings('ignore')

""" 
This project downloads fundamental and price/volume data from Yahoo Finance for years 2020-2023
and put it in a multi-index dataframe. Some tickers have no data for every year, they will be stored 
into the file tickers_with_missing_years.csv
STEPS:

0 create a list of active tickers from active_tickers.txt (see tickers.py)
1 download the data for the first ticker (it must have all 4 years)
2 compute the average price and volume
3 create a dataframe with all the data
4 repeat steps 1-2 for all the other tickers and append the data to the dataframe
5 concatenate a class for each year with the difference in % between the price in year x and year x-1
6 store data into a csv file and an h5 file
7 go to fill_gaps.py for the next stage
8 the final dataframe with tickers having no gaps will be stored in final_data_2020_2023.csv,
  while the missing tickers will be stored in yfinance_tickers_with_gaps.csv
 
"""
# STEP 0
my_file = open("active_tickers.txt", "r")
data = my_file.read()
data_into_list = data.replace('\n', ', ').split(", ")
ticker_list = list(filter(None, data_into_list))


# STEP 1
# the features will be financials + fundamentals
features = ['Avg Close', 'Avg High', 'Avg Low', 'Avg Vol']
for i in fundamentals.fundamentals:
    features.append(fundamentals.fundamentals[i])

# download the fundamentals for the first ticker assuming it contains all years
ticker0 = ticker_list[0]

all_fundamentals = functions.get_fundamentals(ticker0, variables.years)
income_sheet = all_fundamentals[0]
balance_sheet = all_fundamentals[1]
cashflow = all_fundamentals[2]

# STEP 2
# compute the avg adjusted price and volume (Close, High, Low, Volume) for each year
try:
    data_price = functions.get_vol_and_price(ticker0, variables.years)  # dictionary
except Exception as e:
    print('ERROR IN STEP 2')
    print('The error is: ', e)

diz = {}
for y in variables.years:
    diz["".join(['avg_close_', y])] = data_price[y][0]
    diz["".join(['avg_high_', y])] = data_price[y][1]
    diz["".join(['avg_low_', y])] = data_price[y][2]
    diz["".join(['avg_vol_', y])] = data_price[y][3]

data_tmp2020 = [diz['avg_close_2020'], diz['avg_high_2020'], diz['avg_low_2020'], diz['avg_vol_2020']]
data_tmp2021 = [diz['avg_close_2021'], diz['avg_high_2021'], diz['avg_low_2021'], diz['avg_vol_2021']]
data_tmp2022 = [diz['avg_close_2022'], diz['avg_high_2022'], diz['avg_low_2022'], diz['avg_vol_2022']]
data_tmp2023 = [diz['avg_close_2023'], diz['avg_high_2023'], diz['avg_low_2023'], diz['avg_vol_2023']]

data = []
# append data for 2020: the order is volume/price, income_sheet, balance_sheet, cashflow
for d in data_tmp2020:
    data.append(d)  # volume/price
for i in range(0, len(fundamentals.income_fundamentals)):
    data.append(income_sheet["2020"].iloc[i])
for i in range(0, len(fundamentals.balancesheet_fundamentals)):
    data.append(balance_sheet["2020"].iloc[i])
for i in range(0, len(fundamentals.cashflow_fundamentals)):
    data.append(cashflow["2020"].iloc[i])

# 2021
for d in data_tmp2021:
    data.append(d)
for i in range(0, len(fundamentals.income_fundamentals)):
    data.append(income_sheet["2021"].iloc[i])
for i in range(0, len(fundamentals.balancesheet_fundamentals)):
    data.append(balance_sheet["2021"].iloc[i])
for i in range(0, len(fundamentals.cashflow_fundamentals)):
    data.append(cashflow["2021"].iloc[i])

# 2022
for d in data_tmp2022:
    data.append(d)
for i in range(0, len(fundamentals.income_fundamentals)):
    data.append(income_sheet["2022"].iloc[i])
for i in range(0, len(fundamentals.balancesheet_fundamentals)):
    data.append(balance_sheet["2022"].iloc[i])
for i in range(0, len(fundamentals.cashflow_fundamentals)):
    data.append(cashflow["2022"].iloc[i])

# 2023
for d in data_tmp2023:
    data.append(d)
for i in range(0, len(fundamentals.income_fundamentals)):
    data.append(income_sheet["2023"].iloc[i])
for i in range(0, len(fundamentals.balancesheet_fundamentals)):
    data.append(balance_sheet["2023"].iloc[i])
for i in range(0, len(fundamentals.cashflow_fundamentals)):
    data.append(cashflow["2023"].iloc[i])

# STEP 3
# hierarchical indices and columns (number of columns is years * features)
index = pd.MultiIndex.from_product([[ticker0]])
columns = pd.MultiIndex.from_product([variables.years, features], names=['Year', 'Fundamental'])

df = pd.DataFrame([data], index=index, columns=columns)

# STEP 4
# Append all the other tickers in the ticker_list if they have all years
# otherwise, add them into the list of tickers with missing data
tickers_with_missing_years = []
for t in ticker_list[1:]:
    print(t)
    all_statements = functions.get_fundamentals(t, variables.years)
    missing_data = all_statements[3]  # this is a boolean
    inc_stat = all_statements[0]
    bal_sheet = all_statements[1]
    cash_flow = all_statements[2]

    data_to_add = []
    if not missing_data:
        try:
            volume_price = functions.get_vol_and_price(t, variables.years)
            avg_close_2020 = volume_price[variables.years[0]][0]
            avg_high_2020 = volume_price[variables.years[0]][1]
            avg_low_2020 = volume_price[variables.years[0]][2]
            avg_vol_2020 = volume_price[variables.years[0]][3]
            avg_close_2021 = volume_price[variables.years[1]][0]
            avg_high_2021 = volume_price[variables.years[1]][1]
            avg_low_2021 = volume_price[variables.years[1]][2]
            avg_vol_2021 = volume_price[variables.years[1]][3]
            avg_close_2022 = volume_price[variables.years[2]][0]
            avg_high_2022 = volume_price[variables.years[2]][1]
            avg_low_2022 = volume_price[variables.years[2]][2]
            avg_vol_2022 = volume_price[variables.years[2]][3]
            avg_close_2023 = volume_price[variables.years[3]][0]
            avg_high_2023 = volume_price[variables.years[3]][1]
            avg_low_2023 = volume_price[variables.years[3]][2]
            avg_vol_2023 = volume_price[variables.years[3]][3]
            # append data for 2020
            # the order is volume/price, income_sheet, balance_sheet, cashflow
            data_to_add.append(avg_close_2020)
            data_to_add.append(avg_high_2020)
            data_to_add.append(avg_low_2020)
            data_to_add.append(avg_vol_2020)
            for i in range(0, len(fundamentals.income_fundamentals)):
                data_to_add.append(inc_stat["2020"].iloc[i])
            for i in range(0, len(fundamentals.balancesheet_fundamentals)):
                data_to_add.append(bal_sheet["2020"].iloc[i])
            for i in range(0, len(fundamentals.cashflow_fundamentals)):
                data_to_add.append(cash_flow["2020"].iloc[i])

            # 2021
            data_to_add.append(avg_close_2021)
            data_to_add.append(avg_high_2021)
            data_to_add.append(avg_low_2021)
            data_to_add.append(avg_vol_2021)
            for i in range(0, len(fundamentals.income_fundamentals)):
                data_to_add.append(inc_stat["2021"].iloc[i])
            for i in range(0, len(fundamentals.balancesheet_fundamentals)):
                data_to_add.append(bal_sheet["2021"].iloc[i])
            for i in range(0, len(fundamentals.cashflow_fundamentals)):
                data_to_add.append(cash_flow["2021"].iloc[i])

            # 2022
            data_to_add.append(avg_close_2022)
            data_to_add.append(avg_high_2022)
            data_to_add.append(avg_low_2022)
            data_to_add.append(avg_vol_2022)
            for i in range(0, len(fundamentals.income_fundamentals)):
                data_to_add.append(inc_stat["2022"].iloc[i])
            for i in range(0, len(fundamentals.balancesheet_fundamentals)):
                data_to_add.append(bal_sheet["2022"].iloc[i])
            for i in range(0, len(fundamentals.cashflow_fundamentals)):
                data_to_add.append(cash_flow["2022"].iloc[i])

            # 2023
            data_to_add.append(avg_close_2023)
            data_to_add.append(avg_high_2023)
            data_to_add.append(avg_low_2023)
            data_to_add.append(avg_vol_2023)
            for i in range(0, len(fundamentals.income_fundamentals)):
                data_to_add.append(inc_stat["2023"].iloc[i])
            for i in range(0, len(fundamentals.balancesheet_fundamentals)):
                data_to_add.append(bal_sheet["2023"].iloc[i])
            for i in range(0, len(fundamentals.cashflow_fundamentals)):
                data_to_add.append(cash_flow["2023"].iloc[i])

            # convert new data into a df
            new_index = pd.MultiIndex.from_product([[t]])
            data_to_add_df = pd.DataFrame([data_to_add], index=new_index, columns=columns)

            # concatenate the new row
            df = pd.concat([df, data_to_add_df], axis=0)
        except Exception as e:
            tickers_with_missing_years.append(t)
            pass

    else:
        tickers_with_missing_years.append(t)

#####
# STEP 5
# Compute the averages for 2019 that will be used for Increase % in 2020
only_two_years = ['2019', '2020']
diz_2019 = {}
avg_close_perc_2020 = []

diz_incr_2020 = {}
for t in ticker_list:
    if t not in tickers_with_missing_years:
        ticker_to_use = [t]
        # 2019
        diz_2019[t] = functions.get_vol_and_price(t, [only_two_years[0]])
        diz_avg = diz_2019[t]

        data_ticker_2019 = diz_2019[t]
        data_2019 = data_ticker_2019['2019']  # format [124.72, 125.54, 123.69, 24605.74]
        avg_close_2019 = data_2019[0]  # float

        # 2020
        diz = {}
        y2 = only_two_years[1]
        diz[y2] = yf.download(tickers=ticker_to_use, start="-".join([y2, '01-01']), end="-".join([y2, '12-31']), interval="1d", auto_adjust=True, prepost=False)

        # convert close values into lists
        close = diz[y2]["Close"].values.tolist()
        # compute the avg close
        avg_close_2020 = functions.get_avg_from_list(close)

        # calculate the increase/decrease between avg close in 2019 and 2020
        perc = round((avg_close_2020 - avg_close_2019) / avg_close_2019 * 100, 2)

        # this will contain the increase/decrease in 2019/2020 for every ticker
        diz_incr_2020[t] = perc


# Concatenate the class with the difference between one year and the previous one
# Increase in 2020 is calculated differently of the other years
df['2020', 'Increase %'] = np.nan
index_tuples = df.index.values.tolist()
index_list = []
for i in index_tuples:
    index_list.append(i[0])

for i in index_list:
    df.at[i, ('2020', 'Increase %')] = diz_incr_2020[i]


df['2021', 'Increase %'] = round((df['2021', 'Avg Close'] - df['2020', 'Avg Close']) / df['2020', 'Avg Close'] * 100, 2)
df['2022', 'Increase %'] = round((df['2022', 'Avg Close'] - df['2021', 'Avg Close']) / df['2021', 'Avg Close'] * 100, 2)
df['2023', 'Increase %'] = round((df['2023', 'Avg Close'] - df['2022', 'Avg Close']) / df['2022', 'Avg Close'] * 100, 2)

column_extract = df.pop(('2023', 'Increase %'))
df.insert(0, ('2023', 'Increase %'), column_extract)
column_extract = df.pop(('2022', 'Increase %'))
df.insert(0, ('2022', 'Increase %'), column_extract)
column_extract = df.pop(('2021', 'Increase %'))
df.insert(0, ('2021', 'Increase %'), column_extract)
column_extract = df.pop(('2020', 'Increase %'))
df.insert(0, ('2020', 'Increase %'), column_extract)

#####
# STEP 6
# store data into csv and h5
title = 'yfinance_data2020_2023'
path = '/Users/madararubino'
title_missing_tickers = 'yfinance_tickers_with_missing_years'
functions.write_to_csv(df, title)
functions.write_to_h5(df, title, path)

with open('yfinance_tickers_with_missing_years.csv', 'w', newline='') as file:
    # Step 4: Using csv.writer to write the list to the CSV file
    writer = csv.writer(file)
    writer.writerow(tickers_with_missing_years)

# To read a h5 file and convert it into a df: pd.read_hdf('yfinance_data2020_2023')


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')

