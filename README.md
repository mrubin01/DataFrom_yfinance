# Overview 

This project downloads fundamental and price/volume data from Yahoo Finance for years 2020-2023
and store it in a multi-index dataframe. Some tickers may have missing years, they will be stored 
into the file tickers_with_missing_years.csv
# Steps:

0. create a list of active tickers from active_tickers.txt (see tickers.py)
1. download the data for the first ticker (it must have all 4 years)
2. compute the average price and volume
3. create a dataframe with all the data
4. repeat steps 1-2 for all the other tickers and append the data to the dataframe
5. concatenate a class for each year with the difference in % between the price in year x and year x-1
6. store data into a csv file and an h5 file
7. go to fill_gaps.py for the next stage
8. the final dataframe with tickers having no gaps will be stored in final_data_2020_2023.csv,
  while the missing tickers will be stored in yfinance_tickers_with_gaps.csv
