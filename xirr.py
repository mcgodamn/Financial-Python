import pandas as pd
from scipy.optimize import newton
from datetime import date

def xnpv(rate, values, dates):
    min_date = min(dates)
    return sum([
        value / (1 + rate)**((date - min_date).days / 365)
        for value, date in zip(values, dates)
    ])

def xirr(values, dates):
    return newton(lambda r: xnpv(r, values, dates), 0)

def test():
    Values = [-3000, 1000, 1000, 1000, 1000]
    Dates = [
        pd.Timestamp('2017-01-01 00:00:00'),
        pd.Timestamp('2018-01-01 00:00:00'),
        pd.Timestamp('2019-01-01 00:00:00'),
        pd.Timestamp('2020-01-01 00:00:00'),
        pd.Timestamp('2021-01-01 00:00:00'),
    ]

    print(xnpv(0.05,Values,Dates))
    print(xirr(Values, Dates))