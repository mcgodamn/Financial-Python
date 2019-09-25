# -*- coding: UTF-8 -*-
import yaml
import pandas as pd
import datetime
from recurrent import RecurringEvent
from dateutil import rrule
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


class Budget:
    def __init__(self, setting_, frame_):
        self.__setting = setting_
        self.__frame = frame_

    def __update_totals(self, df):
        if df.columns.isin(['total', 'cum_total']).any():
            df['total'] = 0
            df['cum_total'] = 0
        df['total'] = df.sum(axis=1)
        df['cum_total'] = df['total'].cumsum()
        return df

    def __plot_budget(self, df):
        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df.total, label='Daily Total')
        plt.plot(df.index, df.cum_total, label='Cumulative Total')
        plt.legend()
        plt.show()

    def __get_dates(self, frequency, start, end):
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


    def __build_Calendar(self, budget, start, end):
        calendar = pd.DataFrame(index=pd.date_range(start=start, end=end))

        for k, v in budget.items():
            frequency = v.get('frequency')
            amount = v.get('amount')
            if v.get('predict') == True:
                dates = self.__get_dates(frequency, pd.Timestamp(
                    datetime.datetime.now()).normalize() + pd.DateOffset(1), end)
            else:
                dates = self.__get_dates(frequency, start, end)
            i = pd.DataFrame(
                data={k: amount},
                index=pd.DatetimeIndex(pd.Series(dates))
            )
            calendar = pd.concat([calendar, i], axis=1).fillna(0)
        calendar = calendar.loc[
            (calendar.index >= start) & 
            (calendar.index <= end) ]
        calendar['total'] = calendar.sum(axis=1)
        calendar['cum_total'] = calendar['total'].cumsum()

        return calendar

    def Show(self):
        with open(self.__setting) as f:
            setting = yaml.safe_load(f.read())
        START = pd.Timestamp(setting.get('start')).normalize()
        END = pd.Timestamp(setting.get('end')).normalize()
        with open(self.__frame) as f:
            budget = yaml.safe_load(f.read())
        self.__plot_budget(self.__build_Calendar(budget, START, END))

calendar = Budget("setting.yaml", "budget.yaml")
calendar.Show()
