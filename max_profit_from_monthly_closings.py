import datetime

from nsepy import get_history

from constants import NIFTY50
from monthly_closing_prices import (
    add_max_profit_percent_from_last_closing_column, get_monthly_data
)

def main(MONTHLY_PROFIT_LAALACH=4, NO_OF_MONTHS=18, verbose=False, output_format='human'):
    '''
        Finds the probability that a stock bought at a month's closing returned
        MONTHLY_PROFIT_LAALACH percent of profit in the next month, in the
        last `NO_OF_MONTHS` months
        Args:
            format:
                If 'tsv' -> results are printed in tab-separated format
                elif 'human' -> results are printed in human readable format
    '''
    today = datetime.datetime.today()
    for symbol in NIFTY50:
        monthly_data = get_monthly_data(
            datetime.date(2020,1,20),
            datetime.date(today.year, today.month, today.day),
            symbol
        )
        add_max_profit_percent_from_last_closing_column(monthly_data)
        PROFITABLE_MONTHS_COUNT = 0
        months = sorted(monthly_data.index.tolist(), reverse=True)
        for month in months[:NO_OF_MONTHS]:
            if monthly_data.loc[month]['max profit percentage from last closing'] > MONTHLY_PROFIT_LAALACH:
                PROFITABLE_MONTHS_COUNT += 1
        if verbose:
            print(monthly_data)
        output_string = ''
        if output_format == 'human':
            output_string += 'CONCLUSION ------ '
        output_string += '%s\t%s' % (symbol, str(PROFITABLE_MONTHS_COUNT / NO_OF_MONTHS * 100))
        print(output_string)


if __name__ == '__main__':
    main()
