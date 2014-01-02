import datetime

WEEKDAYS = range(0, 5)
HOLIDAYS = (
    datetime.date(2011, 9, 5),      # labor day
    datetime.date(2011, 10, 10),    # columbus day
    datetime.date(2011, 11, 11),    # veterans day
    datetime.date(2011, 11, 24),    # thanksgiving
    datetime.date(2011, 11, 25),    # thanksgiving friday
    datetime.date(2011, 12, 23),    # winter break
    datetime.date(2011, 12, 26),    # winter break
    datetime.date(2011, 12, 27),    # winter break
    datetime.date(2011, 12, 28),    # winter break
    datetime.date(2011, 12, 29),    # winter break
    datetime.date(2011, 12, 30),    # winter break
    datetime.date(2012, 1, 2),      # winter break
    datetime.date(2012, 1, 16),     # mlk day
    datetime.date(2012, 2, 20),     # presidents day
    ### skipped some
    datetime.date(2012, 9, 3),      # labor day
    datetime.date(2012, 10, 8),     # columbus day
    datetime.date(2012, 11, 12),    # veterans day
    datetime.date(2012, 11, 22),    # thanksgiving
    datetime.date(2012, 11, 23),    # thanksgiving friday
    datetime.date(2012, 12, 24),    # winter break
    datetime.date(2012, 12, 25),    # winter break
    datetime.date(2012, 12, 26),    # winter break
    datetime.date(2012, 12, 27),    # winter break
    datetime.date(2012, 12, 28),    # winter break
    datetime.date(2012, 12, 31),    # winter break
    datetime.date(2013, 1, 1),      # winter break
    datetime.date(2013, 1, 21),     # mlk day
    datetime.date(2013, 2, 18),     # presidents day

    datetime.date(2014, 1, 1),      # new years
    datetime.date(2014, 1, 20),     # MLK
    datetime.date(2014, 2, 17),     # Washington's birthday
    datetime.date(2014, 5, 26),     # Memorial day
    datetime.date(2014, 7, 4),      # Independence day
    datetime.date(2014, 9, 1),      # Labor day
    datetime.date(2014, 10, 13),    # Columbus day
    datetime.date(2014, 11, 11),    # Veteran's day
    datetime.date(2014, 11, 27),    # Thanksgiving
    datetime.date(2014, 12, 25),    # Christmas
)

def is_workday(date):
    """ Test to see if given date is a work day.
        Work days are defined as weekdays that are not paid holidays.
    """

    day_of_week = date.weekday()
    return day_of_week in WEEKDAYS and date not in HOLIDAYS

def is_holiday(date):
    return date in HOLIDAYS

def is_weekend(date):
    return date.weekday() not in WEEKDAYS

def date_range(start_date, end_date):
    """ Generate days from start_date to end_date, inclusive
    """

    days = (end_date - start_date).days
    for i in xrange(days + 1):
        yield start_date + datetime.timedelta(i)

def weekdays(date_range):
    for dt in date_range:
        if 0 <= dt.weekday() < 5:
            yield dt

def workdays(start_date):
    current = start_date
    while True:
        if is_workday(current):
            yield current
        current = current + datetime.timedelta(days=1)


def next_workday(after):
    days = date_range(after + datetime.timedelta(1),
                      after + datetime.timedelta(days=365))
    for d in days:
        if is_workday(d):
            return d

