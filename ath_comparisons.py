import datetime
from datetime import date
from typing import List

from nsepy import get_history
import pandas as pd

from constants import NIFTY50


def get_monthly_data(start_date, end_date, symbol):
    '''Monthly closing, high, low & opening for the months [start_date, end_date)

    Only year & month of `start_date` & `end_date` are considered - rest values are ignored
    '''
    start_date = date(start_date.year, start_date.month, 1)
    end_date = date(end_date.year, end_date.month, 1) - datetime.timedelta(days=1)

    data = {'month': [], 'closing': [], 'high': [], 'low': [], 'opening': [], 'volume': []}
    if start_date > end_date:
        return pd.DataFrame(data)

    history = get_history(symbol=symbol, start=start_date, end=end_date)
    print('Fetched history...')
    if history.empty:
        print('No data received for the given inputs')
        return pd.DataFrame(data)
    history_dates = set(history.index.tolist())

    return pd.DataFrame(data).set_index('month')

def get_current_with_ath(symbol, ath_percentile=100, last_n_days=365):
    '''
        Get the All-Time-High (or some percentile high) with the Last-Traded-Price of
        a stock
    '''
    assert 0 <= ath_percentile <= 100, '`ath_percentile` should be in the range [0, 100]'

    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=last_n_days)

    print('Fetching data for %s' % symbol)
    history = get_history(symbol=symbol, start=start_date, end=end_date)
    print('Data fetched for %s' % symbol)
    percentile_highest_price = history.High.nlargest(int((1 - ath_percentile / 100) * len(history)) + 1)[-1]
    ath = history.High.max()
    ltp = history.Close[-1]

    return percentile_highest_price, ath, ltp


def bulk_ath_comparisons(company_symbols:List[str]=[]):
    data = {'symbol':[], 'LTP': [], 'ATH': [], 'nth_percentile_high': []}

    for symbol in company_symbols:
        percentile_highest_price, ath, ltp = get_current_with_ath(symbol, 95)
        data['symbol'].append(symbol)
        data['LTP'].append(ltp)
        data['ATH'].append(ath)
        data['nth_percentile_high'].append(percentile_highest_price)
    return pd.DataFrame(data).set_index('symbol')


def main(symbols):
    ath_comparison_data = bulk_ath_comparisons(symbols)
    ath_comparison_data.to_csv('output/nifty50_ath_comparisons.csv', index=True, header=True)

if __name__ == '__main__':
    symbols = NIFTY50

    import sys
    if len(sys.argv) > 1:
        symbols = sys.argv[1].split(',')

    main(symbols)
