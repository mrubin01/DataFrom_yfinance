"""
The features have been chosen on the basis of:
- the features used in the dissertation,
- the features considered the most important in Medium,
- the features considered relevant for Peter Lynch

Check the file fundamental_features.rtf

To check the gaps in the df use the function functions.print_feature_gaps
After an initial exploration, there are only 12 features with no gaps.
The Cashflow statement is the one with more gaps

12 Features with no gaps:
Normalized Income IS
Net Income IS
Pretax Income IS
Total Revenue IS
Operating Revenue IS
Total Liabilities Net Minority Interest BS
Tangible Book Value BS
Net Tangible Assets BS
Common Stock Equity BS
Stockholders Equity BS
Total Assets BS
Free Cash Flow CF

8 Features with gaps < 5%
Net Interest Income IS
Diluted EPS IS
Basic EPS IS
Selling General And Administration IS
Ordinary Shares Number BS
Total Debt BS
Capital Stock BS
Common Stock BS

3 Features with gaps < 10%
Interest Expense IS
Operating Expense IS
Accounts Payable BS

14 Features with gaps between 10% and 20%
Normalized EBITDA IS
EBITDA IS
EBIT IS
Total Expenses IS
Tax Provision IS
Operating Income IS
Net PPE BS
Gross PPE BS
Accounts Receivable BS
Capital Expenditure CF
Cash Flow From Continuing Financing Activities CF
Net Common Stock Issuance CF
Cash Flow From Continuing Investing Activities CF
Cash Flow From Continuing Operating Activities CF

"""

fundamentals = {
    # all fundamentals
    1: 'Normalized EBITDA',
    2: 'EBITDA',
    3: 'EBIT',
    4: 'Net Interest Income',
    5: 'Interest Expense',
    6: 'Interest Income',
    7: 'Normalized Income',
    8: 'Total Expenses',
    9: 'Diluted EPS',
    10: 'Basic EPS',
    11: 'Net Income',
    12: 'Tax Provision',
    13: 'Pretax Income',
    14: 'Operating Income',
    15: 'Operating Expense',
    16: 'Research And Development',
    17: 'Selling General And Administration',
    18: 'Gross Profit',
    19: 'Cost Of Revenue',
    20: 'Total Revenue',
    21: 'Operating Revenue',

    22: 'Ordinary Shares Number',
    23: 'Net Debt',
    24: 'Total Debt',
    25: 'Tangible Book Value',
    26: 'Net Tangible Assets',
    27: 'Common Stock Equity',
    28: 'Stockholders Equity',
    29: 'Capital Stock',
    30: 'Common Stock',
    31: 'Preferred Stock',
    32: 'Total Liabilities Net Minority Interest',
    33: 'Accounts Payable',
    34: 'Total Assets',
    35: 'Other Non Current Assets',
    36: 'Net PPE',
    37: 'Gross PPE',
    38: 'Machinery Furniture Equipment',
    39: 'Other Current Assets',
    40: 'Accounts Receivable',

    41: 'Free Cash Flow',
    42: 'Capital Expenditure',
    43: 'Cash Flow From Continuing Financing Activities',
    44: 'Cash Dividends Paid',
    45: 'Common Stock Dividend Paid',
    46: 'Net Common Stock Issuance',
    47: 'Cash Flow From Continuing Investing Activities',
    48: 'Cash Flow From Continuing Operating Activities'
}

income_fundamentals = {
    1: 'Normalized EBITDA',
    2: 'EBITDA',
    3: 'EBIT',
    4: 'Net Interest Income',
    5: 'Interest Expense',
    6: 'Interest Income',
    7: 'Normalized Income',
    8: 'Total Expenses',
    9: 'Diluted EPS',
    10: 'Basic EPS',
    11: 'Net Income',
    12: 'Tax Provision',
    13: 'Pretax Income',
    14: 'Operating Income',
    15: 'Operating Expense',
    16: 'Research And Development',
    17: 'Selling General And Administration',
    18: 'Gross Profit',
    19: 'Cost Of Revenue',
    20: 'Total Revenue',
    21: 'Operating Revenue'
}

balancesheet_fundamentals = {
    22: 'Ordinary Shares Number',
    23: 'Net Debt',
    24: 'Total Debt',
    25: 'Tangible Book Value',
    26: 'Net Tangible Assets',
    27: 'Common Stock Equity',
    28: 'Stockholders Equity',
    29: 'Capital Stock',
    30: 'Common Stock',
    31: 'Preferred Stock',
    32: 'Total Liabilities Net Minority Interest',
    33: 'Accounts Payable',
    34: 'Total Assets',
    35: 'Other Non Current Assets',
    36: 'Net PPE',
    37: 'Gross PPE',
    38: 'Machinery Furniture Equipment',
    39: 'Other Current Assets',
    40: 'Accounts Receivable'
}

cashflow_fundamentals = {
    41: 'Free Cash Flow',
    42: 'Capital Expenditure',
    43: 'Cash Flow From Continuing Financing Activities',
    44: 'Cash Dividends Paid',
    45: 'Common Stock Dividend Paid',
    46: 'Net Common Stock Issuance',
    47: 'Cash Flow From Continuing Investing Activities',
    48: 'Cash Flow From Continuing Operating Activities'
}
