# -*- coding: UTF-8 -*-

import pandas as pd
import datetime
from recurrent import RecurringEvent
from dateutil import rrule
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def update_totals(df):
    if df.columns.isin(['total', 'cum_total']).any():
        df['total'] = 0
        df['cum_total'] = 0
    df['total'] = df.sum(axis=1)
    df['cum_total'] = df['total'].cumsum()
    return df

def plot_budget(df):
    plt.figure(figsize = (10,5))
    plt.plot(df.index, df.total, label='Daily Total')
    plt.plot(df.index, df.cum_total, label='Cumulative Total')
    plt.legend()
    plt.show()

def get_dates(frequency, start, end):
    try:
        return [pd.Timestamp(frequency).normalize()]
    except ValueError:
        pass
    try:
        r = RecurringEvent()
        r.parse(frequency)
        rr = rrule.rrulestr(r.get_RFC_rrule())
        return [
            pd.to_datetime(date).normalize()
            for date in rr.between(start, end)
        ]
    except ValueError as e:
        raise ValueError('Invalid frequency')

TODAY = pd.Timestamp(datetime.datetime.now()).normalize()
END = pd.Timestamp(2019, 12, 31).normalize()

calender = pd.DataFrame(index=pd.date_range(start=TODAY, end=END))

income = pd.DataFrame(
    data={'income':36000},
    index=pd.date_range(start=TODAY, end=END, freq='M').shift(5, 'D')
)
income = income.loc[(income.index >= TODAY) & (income.index <= END)]

rent = pd.DataFrame(
    data = {'rent': -8000},
    index=pd.date_range(start=TODAY, end = END, freq='MS')
)
rent = rent.loc[(rent.index >= TODAY) & (rent.index <= END)]

bank = pd.DataFrame(
    data={'bank': 7259},
    index=pd.date_range(start=TODAY, end = TODAY)
)

calender = pd.concat([calender, bank], axis=1).fillna(0)
calender = pd.concat([calender, income], axis=1).fillna(0)
calender = pd.concat([calender, rent], axis=1).fillna(0)
calender['total'] = calender.sum(axis=1)
calender['cum_total'] = calender['total'].cumsum()

calender = update_totals(calender)
# print(calender.tail(1))

plot_budget(calender)