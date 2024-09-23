import datetime

from nsepy import get_history

from constants import NIFTY50, NIFTY_NEXT_50
from monthly_closing_prices import (
    add_max_profit_percent_from_last_closing_column
)
from weekly_analysis import get_weekly_data


def get_trend_by_count(
    symbol,
    num_units=15,
    uptrend_if_above_percent=0.7,
    downtrend_if_below_percent=0.3,
    chart_type='weekly',
    return_human_readable=True,
    verbose=False,
):
    '''
        Tells the current trend (uptrend, downtrend or consolidation) of given stock.

        Params:
            symbol: Symbol of the stock to get trend for
            num_units: Number of past units (on selected chart) to look at
            uptrend_if_above_percent: Stock will be considered in uptrend if it has grown
                for at least this percent of units. For example, it is in uptrend if
                it grew for at least 75% of the weeks in the last 20 weeks (i.e. 15 weeks).
            downtrend_if_below_percent: Stock will be considered in downtrend if it has grown
                for at less than this percent of units. For example, it is in downtrend if
                it gained for less than 25% of the weeks in the last 20 weeks (i.e. 15 weeks).
            chart_type: Currently, on 'weekly' is supported
            return_human_readable: If True, returns a human readable string, else an integer code

        Return the trend of the symbol:
            1 or 'uptrend'
            0 or 'consolidtion'
            -1 or 'downtrend'
    '''
    SUPPORTED_CHART_TYPES = ['weekly']
    assert chart_type in SUPPORTED_CHART_TYPES, (
        f"chart_type should be one of {SUPPORTED_CHART_TYPES}, received {chart_type}"
    )
    if verbose:
        print(
            f'Finding trend of {symbol} on {chart_type} chart with '
            f'num_units={num_units}, '
            f'uptrend_if_above_percent={uptrend_if_above_percent}, '
            f'downtrend_if_below_percent={downtrend_if_below_percent}\n'
        )
    if chart_type=='weekly':
        chart_multiplier = 7
    elif chart_type=='monthly':
        chart_multiplier = 31
    else:  # daily
        chart_multiplier = 1
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(
        days=((num_units + 1) * chart_multiplier)
    )
    weekly_data = get_weekly_data(
        start_date,
        end_date,
        symbol
    )
    gain_counts = 0
    units = sorted(weekly_data.index.tolist(), reverse=True)
    if len(units) < num_units: # Might be because company is newly listed & doesn't have enough data
        print(
            f'WARNING: Calculating trend for {symbol} based on only {len(units)} '
            f'units of data ({num_units} were requested).'
        )
    if len(units) > num_units + 2:
        print(
            f'WARNING: Calculating trend for {symbol} based on {len(units)} units '
            f'of data ({num_units} were requested). This might indicate a bug.'
        )

    if verbose:
        print(f'Got {len(units)} units of data')
        print(units)
        print(weekly_data)

    num_compares = len(units) - 1
    for i in range(num_compares):
        if weekly_data.loc[units[i]]['closing'] > weekly_data.loc[units[i+1]]['closing']:
            gain_counts += 1
    if gain_counts / num_compares > uptrend_if_above_percent:
        answer = 1
    elif gain_counts / num_compares < downtrend_if_below_percent:
        answer = -1
    else:
        answer = 0

    if verbose:
        print('gain_counts:', gain_counts)
        print('len(units):', num_compares)

    HUMAN_READABLE_TREND = {
        1: 'uptrend',
        0: 'consolidation',
        -1: 'downtrend',
    }
    if return_human_readable:
        return HUMAN_READABLE_TREND[answer]
    return answer

def get_trend_by_peaks(
    symbol,
    num_units=15,
    uptrend_if_above_percent=0.7,
    downtrend_if_below_percent=0.3,
    chart_type='weekly',
    return_human_readable=True,
    verbose=False,
):
    '''
        Tells the current trend (uptrend, downtrend or consolidation) of given stock.

        Params:
            symbol: Symbol of the stock to get trend for
            num_units: Number of past units (on selected chart) to look at
            uptrend_if_above_percent: Stock will be considered in uptrend if it has grown
                for at least this percent of units. For example, it is in uptrend if
                it grew for at least 75% of the weeks in the last 20 weeks (i.e. 15 weeks).
            downtrend_if_below_percent: Stock will be considered in downtrend if it has grown
                for at less than this percent of units. For example, it is in downtrend if
                it gained for less than 25% of the weeks in the last 20 weeks (i.e. 15 weeks).
            chart_type: Currently, on 'weekly' is supported
            return_human_readable: If True, returns a human readable string, else an integer code

        Return the trend of the symbol:
            1 or 'uptrend'
            0 or 'consolidtion'
            -1 or 'downtrend'
    '''
    SUPPORTED_CHART_TYPES = ['weekly']
    assert chart_type in SUPPORTED_CHART_TYPES, (
        f"chart_type should be one of {SUPPORTED_CHART_TYPES}, received {chart_type}"
    )
    if verbose:
        print(
            f'Finding trend of {symbol} on {chart_type} chart with '
            f'num_units={num_units}, '
            f'uptrend_if_above_percent={uptrend_if_above_percent}, '
            f'downtrend_if_below_percent={downtrend_if_below_percent}\n'
        )
    if chart_type=='weekly':
        chart_multiplier = 7
    elif chart_type=='monthly':
        chart_multiplier = 31
    else:  # daily
        chart_multiplier = 1
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(
        days=((num_units + 1) * chart_multiplier)
    )
    weekly_data = get_weekly_data(
        start_date,
        end_date,
        symbol
    )
    units = sorted(weekly_data.index.tolist(), reverse=True)
    if len(units) < num_units: # Might be because company is newly listed & doesn't have enough data
        print(
            f'WARNING: Calculating trend for {symbol} based on only {len(units)} '
            f'units of data ({num_units} were requested).'
        )
    if len(units) > num_units + 2:
        print(
            f'WARNING: Calculating trend for {symbol} based on {len(units)} units '
            f'of data ({num_units} were requested). This might indicate a bug.'
        )

    if verbose:
        print(f'Got {len(units)} units of data')
        print(units)
        print(weekly_data)

    num_compares = len(units) - 2
    # find bottoms (first element of list is latest)
    bottoms = []
    for i in range(1, num_compares + 1):
        if weekly_data.loc[units[i - 1]]['closing'] > weekly_data.loc[units[i]]['closing'] < weekly_data.loc[units[i + 1]]['closing']:
            bottoms.append(weekly_data.loc[units[i]]['closing'])
    if bottoms and weekly_data.loc[units[0]]['closing'] < bottoms[0]:
        answer = -1
    elif len(bottoms) < 2:
        print('WARNING: raise NotImplementedError("")')
        answer = get_trend_by_count(
            symbol,
            num_units,
            uptrend_if_above_percent,
            downtrend_if_below_percent,
            chart_type,
            return_human_readable=False,
            verbose=False,
        )
    elif len(bottoms) >= 3 and bottoms[0] > bottoms[1] > bottoms[2]:
        answer = 1
    elif bottoms[0] > bottoms[1]:
        answer = 0
    else:
        answer = -1

    if verbose:
        print('bottoms:', bottoms)
        print('len(units):', num_compares)

    HUMAN_READABLE_TREND = {
        1: 'uptrend',
        0: 'consolidation',
        -1: 'downtrend',
    }
    if return_human_readable:
        return HUMAN_READABLE_TREND[answer]
    return answer


def main(
    num_units=15,
    uptrend_if_above_percent=0.7,
    downtrend_if_below_percent=0.3,
    chart_type='weekly',
    return_human_readable=True,
    verbose=False,
):
    print(
        'Getting trends with '
        f'num_units={num_units}, uptrend_if_above_percent={uptrend_if_above_percent}, '
        f'downtrend_if_below_percent={downtrend_if_below_percent}, chart_type={chart_type}'
    )
    for symbol in NIFTY50 + NIFTY_NEXT_50:
        trend = get_trend_by_peaks(symbol, num_units, uptrend_if_above_percent, downtrend_if_below_percent, chart_type, return_human_readable, verbose=False)
        print('CONCLUSION ------ ', symbol, trend)


if __name__ == '__main__':
    main()
