'''
    Functions and utilities to play with weekly data
'''

import datetime
from datetime import date

from nsepy import get_history
import pandas as pd


def get_weekly_data(start_date, end_date, symbol, verbose=False):
    '''Weekly closing, high, low & opening for the weeks in [start_date, end_date)

    Only year, month & date of `start_date` & `end_date` are considered - rest values
    are ignored
    '''
    start_date = date(start_date.year, start_date.month, start_date.day)
    # Go to next Monday
    while start_date.weekday() != 0:
        start_date += datetime.timedelta(days=1)
    end_date = date(end_date.year, end_date.month, end_date.day)
    # Go to last Friday
    while end_date.weekday() != 4:
        end_date -= datetime.timedelta(days=1)
    if verbose:
        print('start_date', start_date, start_date.weekday())
        print('end_date', end_date, end_date.weekday())

    data = {'week': [], 'closing': [], 'high': [], 'low': [], 'opening': [], 'volume': []}
    if start_date > end_date:
        return pd.DataFrame(data)

    history = get_history(symbol=symbol, start=start_date, end=end_date)
    print('Fetched history for %s, %s to %s...' % (symbol, start_date, end_date))
    if history.empty:
        print('No data received for the given inputs')
        return pd.DataFrame(data)
    history_dates = set(history.index.tolist())

    while end_date > start_date:
        current_week_monday = end_date - datetime.timedelta(days=4)
        current_week = '%s-%s-%s' % (
            current_week_monday.year,
            '{:02d}'.format(current_week_monday.month),
            '{:02d}'.format(current_week_monday.day)
        )
        if verbose:
            print(current_week)
        closing = None
        high = None
        low = None
        opening = None
        volume = None

        # This loop will break when end_date becomes Sunday
        while current_week_monday <= end_date:
            if end_date in history_dates:
                if not closing:
                    closing = history.loc[end_date]['Close']
                    low = history.loc[end_date]['Low']
                    high = history.loc[end_date]['High']
                    opening = history.loc[end_date]['Open']
                    volume = history.loc[end_date]['Volume']
                else:
                    low = min(low, history.loc[end_date]['Low'])
                    high = max(high, history.loc[end_date]['High'])
                    opening = history.loc[end_date]['Open']
                    volume += history.loc[end_date]['Volume']
            end_date -= datetime.timedelta(days=1)
        data['week'].append(current_week)
        data['closing'].append(closing)
        data['high'].append(high)
        data['low'].append(low)
        data['opening'].append(opening)
        data['volume'].append(volume)

        # Set end_date to last Friday
        end_date = current_week_monday - datetime.timedelta(days=3)

    return pd.DataFrame(data).set_index('week')


def main(symbol):
    today = datetime.datetime.today()
    weekly_data = get_weekly_data(
        date(2019,1,20),
        date(today.year, today.month, today.day),
        symbol
    )
    weekly_data.to_csv(
        'output/%s_weekly_data.csv' % symbol,
        index=True,
        header=True
    )

if __name__ == '__main__':
    symbol = 'PIIND'

    import sys
    if len(sys.argv) > 1:
        symbol = sys.argv[1]

    main(symbol)
