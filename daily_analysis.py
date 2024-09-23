'''
    Functions and utilities to play with daily data
'''

import datetime
from datetime import date

from nsepy import get_history
import pandas as pd


def get_daily_data(start_date, end_date, symbol, verbose=False):
    '''Daily closing, high, low & opening for the days in [start_date, end_date)

    Only year, month & date of `start_date` & `end_date` are considered - rest values
    are ignored
    '''
    start_date = date(start_date.year, start_date.month, start_date.day)
    end_date = date(end_date.year, end_date.month, end_date.day)

    data = {'day': [], 'closing': [], 'high': [], 'low': [], 'opening': [], 'volume': []}
    if start_date > end_date:
        return pd.DataFrame(data)

    history = get_history(symbol=symbol, start=start_date, end=end_date)
    print('Fetched history for %s, %s to %s...' % (symbol, start_date, end_date))
    if history.empty:
        print('WARN: No data received for the given inputs')
        return pd.DataFrame(data)
    history_dates = set(history.index.tolist())

    while end_date > start_date:
        current_date = '%s-%s-%s' % (
            end_date.year,
            '{:02d}'.format(end_date.month),
            '{:02d}'.format(end_date.day)
        )
        if end_date in history_dates:
            data['closing'].append(history.loc[end_date]['Close'])
            data['low'].append(history.loc[end_date]['Low'])
            data['high'].append(history.loc[end_date]['High'])
            data['opening'].append(history.loc[end_date]['Open'])
            data['volume'].append(history.loc[end_date]['Volume'])
            data['day'].append(current_date)
        end_date -= datetime.timedelta(days=1)

    return pd.DataFrame(data).set_index('day')


def main(symbol):
    today = datetime.datetime.today()
    daily_data = get_daily_data(
        date(2022,11,20),
        date(today.year, today.month, today.day),
        symbol
    )
    daily_data.to_csv(
        'output/%s_daily_data.csv' % symbol,
        index=True,
        header=True
    )

if __name__ == '__main__':
    symbol = 'PIIND'

    import sys
    if len(sys.argv) > 1:
        symbol = sys.argv[1]

    main(symbol)
