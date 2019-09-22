import pandas as pd
import datetime
from recurrent import RecurringEvent
from dateutil import rrule

def get_dates(freq, start, end):
    try:
        return [pd.Timestamp(freq).normalize()]
    except ValueError:
        pass
    try:
        r = RecurringEvent()
        r.parse(freq)
        print(r.get_RFC_rrule())
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
print(calender.head())

print(get_dates('every 5', TODAY, END))

# income = pd.DataFrame(
#     data={'income':36000},
#     index=pd.date_range(start=TODAY, end=END, freq=freq)
# )
# print(income)
