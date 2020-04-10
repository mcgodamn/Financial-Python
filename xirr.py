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
    Values = [-16345, -4326, -530, 3371, 7396, 9694,
    6116,4387,
    4474,
     203045-198449
    ]
    Dates = [
        pd.Timestamp('2019-09-30 00:00:00'),
        pd.Timestamp('2020-09-30 00:00:00'),
        pd.Timestamp('2021-09-30 00:00:00'),
        pd.Timestamp('2022-09-30 00:00:00'),
        pd.Timestamp('2023-09-30 00:00:00'),
        pd.Timestamp('2024-09-30 00:00:00'),
        pd.Timestamp('2025-09-30 00:00:00'),
        pd.Timestamp('2026-09-30 00:00:00'),
        pd.Timestamp('2027-09-30 00:00:00'),
        pd.Timestamp('2028-09-30 00:00:00'),
    ]
    print(xirr(Values, Dates))

test()