"""
A dedicated Date calculator for a science experiment.
"""

import re
from enum import Enum

from .exceptions import InvalidDateException, InvalidDateFormatException


# The number of seconds for a day
SECONDS_PER_DAY = 60 * 60 * 24

# The number of days of a non-leap year
NORMAL_DAYS_PER_YEAR = 365

# The number of days of each month (for non-leap years)
NORMAL_DAYS_OF_MONTH = [
    31,  # Jan
    28,  # Feb
    31,  # Mar
    30,  # Apr
    31,  # May
    30,  # Jun
    31,  # Jul
    31,  # Aug
    30,  # Sep
    31,  # Oct
    30,  # Nov
    31   # Dec
]

KEY_YEAR = 'year'
KEY_MONTH = 'month'
KEY_DAY = 'day'

DATE_FORMAT = {
    '%d': r'(?P<day>\d{1,2})',
    '%m': r'(?P<month>\d{1,2})',
    '%Y': r'(?P<year>\d{4})'
}


def is_leap_year(year: int) -> bool:
    """
    Determine whether a given year is a leap year.

    A year is a leap year when:
        The year is evenly divisible by 4 but not 100,
    OR
        The year is evenly divisible by 4 and 100, and 400 at the
        same time - simplify to evenly divisible by 400.

    :param year: The given year
    :return: True for is a leap year, False for is not a leap year
    """
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0


def num_leap_years(year_start: int, year_end: int) -> int:
    """
    Calculate the number of leap years between year_start inclusive and year_end exclusive.

    (2000, 2004) will return 1, as 2004 is excluded
    (2000, 2000) will return 0, as 2000 is excluded

    :param year_start: the start year, inclusive
    :param year_end: the end year, exclusive
    :return: the number of leap years between year_start (inclusive) and year_end (exclusive)
    """
    start = year_start - 1
    end = year_end - 1

    return (end // 4 - start // 4) - (end // 100 - start // 100) + (end // 400 - start // 400)


class Month(Enum):
    """
    The Month Enum, it will ensure month is valid value (1 ~ 12).
    """

    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12

    def __init__(self, month: int):
        """
        Initialise the Month Enum with given month value (index).

        :param month: the month value (index), start from 1
        """
        self.month = month

        # numbers of days will be attached to each month,
        # note that Feb will have normal days 28. Leap year will be handled separately.
        self.days = NORMAL_DAYS_OF_MONTH[month-1]

    @classmethod
    def of(cls, month: int) -> 'Month':
        """
        A way to initialise a Month Enum instance. Same as Month(month).

        :param month: The given month value (index)
        :return: The Month Enum instance
        """
        return Month(month)


class SciDate:
    """
    SciDate is a specialised and simple date entity. It's only represent year, month and day so far.

    When calling epoch(), it returns the seconds since SciDate's Epoch of 1900.01.01.

    SciDate is read-only, once initialised it becomes immutable. This read-only design fulfil the requirements,
    and keep the implementation simple as well as improved performance at the same time.
    """

    _epoch_year = 1900
    _epoch_month = 1
    _epoch_day = 1

    def __init__(self, year: int, month: int, day: int):
        """
        Initialise the SciDate instance with given year, month and day.

        Validation will ensure the date is valid and date is in the expected range.

        Due to extra calculation, epoch will be None initially, once called it will be calculated and then cached.

        :param year: The given year
        :param month: The given month
        :param day: The given day
        """

        if SciDate.validate(year, month, day) is False:
            raise InvalidDateException(f'Invalid Date: {day}/{month}/{year} (d/m/y)')

        self._year = year
        self._month = month
        self._day = day
        self._epoch = None

    @property
    def year(self):
        """
        Getter for year.

        :return: The value of year
        """
        return self._year

    @property
    def month(self):
        """
        Getter for month.

        :return: The value of month
        """

        return self._month

    @property
    def day(self):
        """
        Getter for day.

        :return: The value of day
        """

        return self._day

    @property
    def epoch(self):
        """
        Calculate or return the epoch value. Epoch is defined as the total seconds since `_base_year`.
        It only been calculated when required, and cached once calculated to prevent re-calculation.

        Epoch will include the `_base_year` 00:00:00 but exclude end day's 00:00:00.
        For example, The epoch of 1900.01.01 is 0, and the epoch of 1900.01.02 is 86400.

        :return: This SciDate's total seconds since `_base_year`.
        """

        if self._epoch is None:
            # calculate the epoch passively, and cache it once calculated

            # calculate days across years since _base_year, don't consider whether the end year is a leap year
            days = (self.year - self._epoch_year) * NORMAL_DAYS_PER_YEAR + num_leap_years(self._epoch_year, self.year)

            if self.month > 2 and is_leap_year(self.year):
                # if the end year include the last day of Feb, check whether it is leap year,
                # add one more day if it is leap year
                days += 1

            for it in range(1, self.month):
                # sum up the end year's days across all months, leap year is already considered in the previous step
                mon = Month(it)
                days += mon.days

            # always treat end day as 00:00:00 (excluded)
            days += self.day - self._epoch_day

            # convert days into seconds, we finally get epoch
            self._epoch = days * SECONDS_PER_DAY
        return self._epoch

    @classmethod
    def validate(cls, year: int, month: int, day: int) -> bool:
        """
        Valid the year, month and day. The month range is [1, 12], and the day range is [28, 31] depends
        on which year/month it is.

        :param year: The given year
        :param month: The given month
        :param day: The given day
        :return: Whether the value of the given SciDate is valid.
        """

        try:
            mon = Month.of(month)
        except ValueError as ex:
            raise InvalidDateException(f'Invalid month value: {month}, should be in [1, 12]') from ex
        else:
            if mon is Month.February and day == mon.days + 1 and is_leap_year(year):
                # leap year will have one more day for Feb
                return True

            # the Month Enum helps to ensure the day value for each month is valid
            return day <= mon.days

    @classmethod
    def parse(cls, date: str, fmt: str = '%d/%m/%Y') -> 'SciDate':
        """
        Only support simple customised format for now.
        Should only and must contain year, month and day.

        :param date: The give date in str format
        :param fmt: The date format
        :return: The parsed SciDate
        """

        _fmt = fmt
        for k, v in DATE_FORMAT.items():
            _fmt = _fmt.replace(k, v)

        if '%' in _fmt:
            raise InvalidDateFormatException(f'Unexpected given format {fmt}')

        matches = re.match(_fmt, date)

        if not matches:
            raise InvalidDateFormatException(f'given date {date} does not match give format {fmt}')

        group_dict = matches.groupdict()
        if KEY_YEAR not in group_dict or KEY_MONTH not in group_dict or KEY_DAY not in group_dict:
            raise InvalidDateFormatException(f'year is mandatory in the given date but got {date} with format {fmt}')

        year = int(group_dict[KEY_YEAR])
        month = int(group_dict[KEY_MONTH])
        day = int(group_dict[KEY_DAY])

        return SciDate(year, month, day)

    def sub(self, other: 'SciDate') -> int:
        """
        SciDate subtraction, self - other. The result is the seconds between the two SciDate.

        :param other: The other SciDate as subtrahend
        :return: The seconds between the two SciDate
        """
        return self.epoch - other.epoch


def days_diff(day1: SciDate, day2: SciDate, *, include_first: bool = False, include_last: bool = False):
    """
    Calculate the days difference between two given days. include_first and include_last
    can be specified to indicate whether include the first and the last day. If first and
    last days are considered partial days and should not be considered, just set both
    include_first and include_last as False (or ignore them as False are the default value).

    Note that this function returns the absolute difference value, the result is unsigned.

    :param day1: The first day
    :param day2: The last day
    :param include_first: Whether include the first day
    :param include_last: Whether include the last day
    :return: The absolute value of the day difference
    """

    # SciDate.sub includes the first day but not last, add last to the diff
    # to fulfil the specified include_first and include_last value
    diff_seconds = abs(day1.sub(day2)) + SECONDS_PER_DAY

    min_diff = 0
    if not include_first:
        min_diff += SECONDS_PER_DAY

    if not include_last:
        min_diff += SECONDS_PER_DAY

    if diff_seconds < min_diff:
        return 0

    return (diff_seconds - min_diff) // SECONDS_PER_DAY
