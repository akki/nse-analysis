import datetime

from constants import NIFTY50
from monthly_closing_prices import (
    add_max_profit_percent_from_last_closing_column, add_max_profit_percent_from_opening_column
)
from daily_analysis import get_daily_data

def main(PROFIT_LAALACH=0.5, NO_OF_UNITS=250, verbose=False, output_format='human'):
    '''
        Finds the probability that a stock bought at a days's closing returned
        PROFIT_LAALACH percent of profit within the next day, in the
        last `NO_OF_DAYS` days
        Args:
            format:
                If 'tsv' -> results are printed in tab-separated format
                elif 'human' -> results are printed in human readable format
    '''
    today = datetime.datetime.today()
    for symbol in NIFTY50:
        data = get_daily_data(
            datetime.date(2020,1,20),
            datetime.date(today.year, today.month, today.day),
            symbol
        )
        add_max_profit_percent_from_last_closing_column(data)
        PROFITABLE_COUNT = 0
        units = sorted(data.index.tolist(), reverse=True)
        for unit in units[:NO_OF_UNITS]:
            if data.loc[unit]['max profit percentage from last closing'] > PROFIT_LAALACH:
                PROFITABLE_COUNT += 1
        if verbose:
            print(data)
        output_string = ''
        if output_format == 'human':
            output_string += 'CONCLUSION ------ '
        output_string += '%s\t%s' % (symbol, str(PROFITABLE_COUNT / NO_OF_UNITS * 100))
        # output_string += '\n%s\t%s' % (symbol, min_profit)
        print(output_string)


if __name__ == '__main__':
    main(PROFIT_LAALACH=0.37, output_format='tsv')
