import pandas as pd
import yfinance as yf
from statistics import mean
import fundamentals
import numpy as np
import variables


def df_index_list(multiindex_df):
    """
    This function returns the number of indexes of a multiindex dataframe
    :param multiindex_df: a pandas multiindex dataframe
    :return: a list of indexes
    """
    index_list = []
    index_tuples = multiindex_df.index.values.tolist()

    for i in index_tuples:
        index_list.append(i[0])

    return index_list


def print_feature_gaps_from_df(df, feature_list):
    """
    This function checks the gaps for each feature in the dataframe
    and print the percentage out of the number of rows
    :param df: a multiindex dataframe
    :param feature_list: a list with the features to check
    :return: nothing, it just prints the results
    """

    no_rows = len(df) - 2  # subtract the two-level column name

    for f in feature_list:
        for y in variables.years:
            perc = (df.loc[:, (y, f)].isnull().sum() / no_rows) * 100
            print(y + ' ' + f + ' ' + str(round(perc, 2)))


def print_ticker_gaps_from_file(file_df):
    """
    This function checks the gaps for each ticker in the dataframe
    and print the percentage out of the number of rows
    :param file_df: the name of the hdf file containing the dataset
    :return: nothing, it just prints the percentages
    """
    # create a multiindex df
    index_list = [0, 1]
    data = pd.read_hdf(f"{file_df}", header=index_list, index_col=0, na_values=[0])
    df = pd.DataFrame(data)

    no_tickers = len(df.columns)

    for t in df_index_list(df):
        try:
            perc = round(df.loc[t].isnull().sum(axis=1) / no_tickers * 100, 2)
            print(t + ' ' + str(perc[0]))
        except Exception:
            pass


def print_feature_gaps_from_file(file_df):
    """
    This function checks the gaps for each feature in the dataframe
    and print the percentage out of the number of rows
    :param file_df: the name of the hdf file containing the dataset
    :return: nothing, it just prints the results
    """

    # create a multiindex df
    index_list = [0, 1]
    data = pd.read_hdf(f"{file_df}", header=index_list, index_col=0, na_values=[0])
    df = pd.DataFrame(data)

    no_rows = len(df) - 2  # subtract the two-level column name

    for f in fundamentals.fundamentals:
        for y in variables.years:
            perc = (df.loc[:, (y, fundamentals.fundamentals[f])].isnull().sum() / no_rows) * 100
            print(y + ' ' + fundamentals.fundamentals[f] + ' ' + str(round(perc, 2)))


def print_ticker_gaps(file_df):
    """
    This function checks the gaps for each feature in the dataframe
    and print the percentage out of the number of rows
    :param file_df: the name of the hdf file containing the dataset
    :return: nothing, it just prints the results
    """

    # create a multiindex df
    index_list = [0, 1]
    data = pd.read_hdf(f"{file_df}", header=index_list, index_col=0, na_values=[0])
    df = pd.DataFrame(data)

    no_rows = len(df) - 2  # subtract the two-level column name

    for f in fundamentals.fundamentals:
        for y in variables.years:
            perc = (df.loc[:, (y, fundamentals.fundamentals[f])].isnull().sum() / no_rows) * 100
            print(y + ' ' + fundamentals.fundamentals[f] + ' ' + str(round(perc, 2)))


def check_active_tickers(year, ticker_lst):
    """
    This function takes a list of tickers and checks if the tickers are active on a certain year
    :return: it does not return anything, it stores the list of active tickers into a txt file
    """
    for t in ticker_lst:
        try:
            get_vol_and_price(t, [year])
        except Exception:
            ticker_lst.remove(t)
        pass

    # store tickers into a txt file
    with open('active_tickers.txt', 'w+') as f:
        for items in ticker_lst:
            f.write('%s\n' %items)
    f.close()


def write_list_to_txt(lst, title):
    with open(f'{title}.txt', 'w+') as f:
        for items in lst:
            f.write('%s\n' %items)
    f.close()


def write_to_csv(df, title):
    """
    Store a df into a csv file
    """
    csv_data = df.to_csv('%s.csv' % title, index=True)


def write_to_h5(df, title, path):
    """
    Store a df into an h5 file
    path must be in format '/Users/madararubino'
    """
    h5_data = df.to_hdf(title, path)


def check_current_price(ticker):
    data = yf.Ticker(ticker)
    try:
        price = str(round(data.info["currentPrice"], 2))
        return price
    except ValueError:
        print('No current price available for ' + ticker)
        return "N/A"


def get_avg_from_list(lst):
    avg = round(mean(lst), 2)
    return avg


def get_vol_and_price(ticker, list_of_years):
    """
    This function returns the tickers' average Close, High, Low and Volume for every year in the list. 2023 must be added
    The object returned is a dictionary with a list for each year in the format [Close, High, Low, Volume]
    """

    # create a dictionary with the data for each year
    diz = {}
    diz1 = {}
    for y in list_of_years:
        diz[y] = yf.download(tickers=ticker, start="-".join([y, '01-01']), end="-".join([y, '12-31']), interval="1d", auto_adjust=True, prepost=False)

        # convert values into lists
        close = diz[y]["Close"].values.tolist()
        high = diz[y]["High"].values.tolist()
        low = diz[y]["Low"].values.tolist()
        vol = diz[y]["Volume"].values.tolist()

        # compute the avg for each field
        avg_close = get_avg_from_list(close)
        avg_high = get_avg_from_list(high)
        avg_low = get_avg_from_list(low)
        avg_vol = round(get_avg_from_list(vol) / 1000, 2)

        # a dic will contain the 4 average values for each year
        diz1[y] = [avg_close, avg_high, avg_low, avg_vol]

    # Close, High, Low, Volume
    return diz1


def get_fundamentals(ticker, list_of_years):
    """
    This function returns the 3 annual financial statements starting from a ticker for the last 4 years.
    The 3 statements returned are dataframe and then can be queried as usual with statement["YYYY"]["Field Name"]
    missing_data_flag will be True if:
    - the ticker is not in yfinance
    - one statement is empty
    - there are missing years
    """
    missing_data_flag = False
    missing_years_flag = False

    # set 3 variables to contain the statements and 1 to contain all data
    inc_stat = pd.DataFrame()
    bal_sheet = pd.DataFrame()
    cash_flow = pd.DataFrame()
    stock_data = pd.DataFrame()

    # this is the number of years to download
    no_of_years = len(list_of_years)

    try:
        stock_data = yf.Ticker(ticker)
    except Exception as e:
        missing_data_flag = True  # no data in yfinance
        pass

    if not missing_data_flag:
        no_of_years_in_yfinance = len(stock_data.financials.columns)  # the number of years currently in yfinance

        # this flag is True when the ticker has missing years
        if no_of_years_in_yfinance == no_of_years:
            pass
        else:
            missing_years_flag = True

        # download the 3 statements
        inc_stat = stock_data.financials
        bal_sheet = stock_data.balance_sheet
        cash_flow = stock_data.cashflow

        # keep only YYYY
        inc_stat.columns = inc_stat.columns.astype(str).str[:4]
        bal_sheet.columns = bal_sheet.columns.astype(str).str[:4]
        cash_flow.columns = cash_flow.columns.astype(str).str[:4]

        # sort oldest to most recent year
        inc_stat = inc_stat[inc_stat.columns[::-1]]
        bal_sheet = bal_sheet[bal_sheet.columns[::-1]]
        cash_flow = cash_flow[cash_flow.columns[::-1]]

        # set the flag to True if one of the statements is empty, otherwise leave it as it is
        if inc_stat.empty or bal_sheet.empty or cash_flow.empty:
            missing_years_flag = True

        # check if the 3 statements have all the required fundamentals
        # provided that the dataframes are not empty and have all years
        if not missing_years_flag:
            indexes_stat = inc_stat.index.tolist()
            indexes_bal = bal_sheet.index.tolist()
            indexes_cash = cash_flow.index.tolist()

            income_fundamentals_to_have = []
            balance_fundamentals_to_have = []
            cash_fundamentals_to_have = []

            for i in fundamentals.income_fundamentals:
                income_fundamentals_to_have.append(fundamentals.income_fundamentals[i])
            for i in fundamentals.balancesheet_fundamentals:
                balance_fundamentals_to_have.append(fundamentals.balancesheet_fundamentals[i])
            for i in fundamentals.cashflow_fundamentals:
                cash_fundamentals_to_have.append(fundamentals.cashflow_fundamentals[i])

            # if a required fundamental field is missing, append it with NaN
            for f in income_fundamentals_to_have:
                if f in indexes_stat:
                    pass
                else:
                    inc_stat.loc[f] = [np.NaN for c in range(len(inc_stat.columns))]

            for f in balance_fundamentals_to_have:
                if f in indexes_bal:
                    pass
                else:
                    bal_sheet.loc[f] = [np.NaN for c in range(len(bal_sheet.columns))]

            for f in cash_fundamentals_to_have:
                if f in indexes_cash:
                    pass
                else:
                    cash_flow.loc[f] = [np.NaN for c in range(len(cash_flow.columns))]

            inc_stat = inc_stat.reindex(income_fundamentals_to_have)
            bal_sheet = bal_sheet.reindex(balance_fundamentals_to_have)
            cash_flow = cash_flow.reindex(cash_fundamentals_to_have)

    # final check
    inc_stat_cols = len(inc_stat.columns)
    bal_sheet_cols = len(bal_sheet.columns)
    cash_flow_cols = len(cash_flow.columns)

    if missing_data_flag or missing_years_flag \
            or inc_stat_cols < no_of_years\
            or bal_sheet_cols < no_of_years\
            or cash_flow_cols < no_of_years:
        missing_data_flag = True

    return inc_stat, bal_sheet, cash_flow, missing_data_flag


