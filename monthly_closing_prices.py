'''
    Functions and utilities to play with monthly data
'''

import datetime
from datetime import date

from nsepy import get_history
import pandas as pd


def find_previous_thursday(check_date):
    '''
        To find the Thursday, just before `check_date`
        This is useful because Thursdays are used to find closing dates
    '''
    while True:
        if check_date.weekday() == 3:
            return check_date
        check_date = check_date - datetime.timedelta(days=1)

'''
Sample code for using `find_previous_thursday`
'''
# # 1st day of today's month
# first_day_of_today_month = date(date.today().year, date.today().month, 1)
# last_day_of_last_month = first_day_of_today_month - datetime.timedelta(days=1)
# print(find_previous_thursday(last_day_of_last_month))


def get_monthly_data(start_date, end_date, symbol, verbose=False):
    '''Monthly closing, high, low & opening for the months [start_date, end_date)

    Only year & month of `start_date` & `end_date` are considered - rest values are ignored
    '''
    start_date = date(start_date.year, start_date.month, 1)
    end_date = date(end_date.year, end_date.month, 1) - datetime.timedelta(days=1)

    data = {'month': [], 'closing': [], 'high': [], 'low': [], 'opening': [], 'volume': []}
    if start_date > end_date:
        return pd.DataFrame(data)

    history = get_history(symbol=symbol, start=start_date, end=end_date)
    print('Fetched history for %s, %s to %s...' % (symbol, start_date, end_date))
    if history.empty:
        print('No data received for the given inputs')
        return pd.DataFrame(data)
    history_dates = set(history.index.tolist())

    while end_date > start_date:
        current_month = '%s-%s' % (end_date.year, '{:02d}'.format(end_date.month))
        if verbose:
            print(current_month)
        closing = None
        high = None
        low = None
        opening = None
        volume = None
        while current_month == '%s-%s' % (end_date.year, '{:02d}'.format(end_date.month)):
            if end_date not in history_dates:
                end_date -= datetime.timedelta(days=1)
                continue
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
        data['month'].append(current_month)
        data['closing'].append(closing)
        data['high'].append(high)
        data['low'].append(low)
        data['opening'].append(opening)
        data['volume'].append(volume)

    return pd.DataFrame(data).set_index('month')

    # curr_date = end_date
    # first_day_of_curr_month = date(curr_date.year, curr_date.month, 1)
    # last_day_of_prev_month = first_day_of_curr_month - datetime.timedelta(days=1)

    # while True:
    #     maybe_closing_day = find_previous_thursday(last_day_of_prev_month)
    #     if maybe_closing_day < start_date:
    #         break
    #     while True:
    #         if maybe_closing_day < start_date:
    #             break
    #         if maybe_closing_day in history_dates:
    #             print('Found closing date: %s' % maybe_closing_day)
    #             closing_dates.append(maybe_closing_day)
    #             break
    #         else:
    #             maybe_closing_day -= datetime.timedelta(days=1)
    #     last_day_of_prev_month = date(last_day_of_prev_month.year, last_day_of_prev_month.month, 1) - datetime.timedelta(days=1)

    # return history[history.index.isin(closing_dates)]


def add_max_profit_percent_from_last_closing_column(monthly_data: pd.DataFrame) -> None:
    '''
        Adds the profit %age earned, if stock is bought at month closing & sold at next month's high
    '''
    months = sorted(monthly_data.index.tolist(), reverse=True)

    high_close_profit_percent = []
    for i in range(len(months) - 1):
        month_high = monthly_data.loc[months[i]]['high']
        last_month_closing = monthly_data.loc[months[i + 1]]['closing']
        profit_percent = (month_high - last_month_closing) / last_month_closing * 100
        high_close_profit_percent.append(profit_percent)

    monthly_data['max profit percentage from last closing'] = high_close_profit_percent + [0]


def add_max_profit_percent_from_opening_column(monthly_data: pd.DataFrame) -> None:
    '''
        Adds the profit %age earned, if stock is bought at a month opening & sold at next month's high
    '''
    COLUMN_NAME = 'max profit percentage from opening'

    # monthly_data[COLUMN_NAME] = ['N/A'] * len(monthly_data)
    high_open_profit_percent = []
    months = monthly_data.index.tolist()
    for i in range(len(monthly_data)):
        month_high = monthly_data.loc[months[i]]['high']
        month_opening = monthly_data.loc[months[i]]['opening']
        profit_percent = (month_high - month_opening) / month_opening * 100
        # monthly_data.loc[months[i]][COLUMN_NAME] = profit_percent
        high_open_profit_percent.append(profit_percent)

    monthly_data[COLUMN_NAME] = high_open_profit_percent


def main(symbol):
    today = datetime.datetime.today()
    monthly_data = get_monthly_data(
        date(2017,1,20),
        date(today.year, today.month, today.day),
        symbol
    )
    add_max_profit_percent_from_last_closing_column(monthly_data)
    monthly_data.to_csv(
        'output/%s_monthly_data.csv' % symbol,
        index=True,
        header=True
    )

if __name__ == '__main__':
    symbol = 'PIIND'

    import sys
    if len(sys.argv) > 1:
        symbol = sys.argv[1]

    main(symbol)
