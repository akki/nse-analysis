import datetime

from nsepy import get_history

from constants import NIFTY50
from monthly_closing_prices import (
    add_max_profit_percent_from_last_closing_column
)
from weekly_analysis import get_weekly_data

def main(WEEKLY_PROFIT_LAALACH=1, NO_OF_WEEKS=52, verbose=False):
    '''
        Finds the probability that a stock bought at a week's closing returned
        WEEKLY_PROFIT_LAALACH percent of profit in the next week, in the
        last `NO_OF_WEEKS` weeks
    '''
    print(
        'Calculating max profit from weekly closings with '
        f'WEEKLY_PROFIT_LAALACH={WEEKLY_PROFIT_LAALACH} and NO_OF_WEEKS={NO_OF_WEEKS}\n'
    )
    today = datetime.datetime.today()
    for symbol in NIFTY50:
        weekly_data = get_weekly_data(
            datetime.date(2020,8,10),
            datetime.date(today.year, today.month, today.day),
            symbol
        )
        add_max_profit_percent_from_last_closing_column(weekly_data)
        PROFITABLE_WEEKS_COUNT = 0
        weeks = sorted(weekly_data.index.tolist(), reverse=True)
        for week in weeks[:NO_OF_WEEKS]:
            if weekly_data.loc[week]['max profit percentage from last closing'] > WEEKLY_PROFIT_LAALACH:
                PROFITABLE_WEEKS_COUNT += 1
        if verbose:
            print(weekly_data)
        print('CONCLUSION ------ ', symbol, PROFITABLE_WEEKS_COUNT / NO_OF_WEEKS * 100)


if __name__ == '__main__':
    main(0.7, 65)
