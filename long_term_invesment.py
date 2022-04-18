import datetime

import pandas as pd

from constants import NIFTY50
from monthly_closing_prices import get_monthly_data

def main():
    '''
        Strategy:
            Keep buying 1 (or X) amount of shares at the closing of every month
            Sell all of them together after a long period of time (say 3 years)
    '''
    data = {'symbol': [], 'Invested amount (₹)': [], 'Last closing (₹)': [], 'Profit (%)': []}
    today = datetime.datetime.today()
    for symbol in NIFTY50:
        monthly_data = get_monthly_data(
            datetime.date(2019, 1, 20),
            datetime.date(today.year, today.month, today.day),
            symbol
        )
        current_value = float(monthly_data[:1]['closing'])
        investment_amounts = monthly_data['closing'][1:]
        data['symbol'].append(symbol)
        data['Invested amount (₹)'].append(sum(investment_amounts))
        data['Last closing (₹)'].append(current_value)
        data['Profit (%)'].append(
            '{:0.2f}'.format(
                (
                    current_value * len(investment_amounts) - sum(investment_amounts)
                ) / sum(investment_amounts) * 100
            )
        )

    pd.DataFrame(data).set_index('symbol').to_csv(
        'output/long_term_investment_%smonths.csv' % len(investment_amounts),
        index=True,
        header=True,
    )


if __name__ == '__main__':
    main()
