"""
Test cases for testing functionalities in scidate.
"""

import datetime

import pytest

from ..scidate import (
    Month,
    SciDate,
    is_leap_year,
    num_leap_years,
    days_diff
)
from ..exceptions import InvalidDateException, InvalidDateFormatException


def test_is_leap_year():
    # not divisible by 4
    assert is_leap_year(1999) is False

    # divisible by 4 but not 100
    assert is_leap_year(1896) is True

    # divisible by 4 and 100 but not 400
    assert is_leap_year(1900) is False

    # divisible by 4, 100, and also 400
    assert is_leap_year(2000) is True


def test_num_leap_years():
    # number of leap year include the start year
    assert num_leap_years(1988, 1989) == 1

    # number of lear years exclude the end year
    assert num_leap_years(1999, 2000) == 0

    # number of leap years include the start year but exclude the end year
    assert num_leap_years(2000, 2000) == 0

    # number of leap years across a period contain a year divisible by 100 but not 400
    assert num_leap_years(1896, 1905) == 2

    # verify number of leap years across a long period of time
    assert num_leap_years(1900, 3000) == 267

    # when it is negative, it is counting down, it won't include Feb of the start year
    assert num_leap_years(2000, 1986) == -3


def test_month_enum():
    # simple verify converting month value to Month Enum
    assert Month.of(1).month == 1
    assert Month(2).days == 28


def test_month_enum_invalid():
    # invalid month smaller than 1
    with pytest.raises(ValueError):
        Month.of(0)

    # invalid month bigger than 12
    with pytest.raises(ValueError):
        Month(13)


def test_sci_date_invalid():
    # invalid month
    with pytest.raises(InvalidDateException):
        SciDate(2021, 0, 13)

    # invalid day
    with pytest.raises(InvalidDateException):
        SciDate(2020, 1, 32)

    # invalid 29 Feb for non-leap year
    with pytest.raises(InvalidDateException):
        SciDate(2023, 2, 29)


def test_sci_date():
    # verify basic properties
    date = SciDate(2021, 6, 23)
    assert date.year == 2021
    assert date.month == 6
    assert date.day == 23

    # verify the epoch with help of datetime library (they have different relative Epoch, 1970 for
    # standard library and 1900 in SciDate)
    base_date = datetime.datetime(1900, 1, 1, 0, 0, 0, 0)
    base_offset = abs(base_date.timestamp())
    assert date.epoch == base_offset + datetime.datetime(2021, 6, 23).timestamp()


def test_sci_date_parse():
    # parsing from the standard format
    date = SciDate.parse('23/06/2021')
    assert date.year == 2021
    assert date.month == 6
    assert date.day == 23

    # parsing from the standard format with optional leading 0 on month
    date = SciDate.parse('23/6/2021')
    assert date.year == 2021
    assert date.month == 6
    assert date.day == 23

    # parsing from the standard format with optional leading 0 on day
    date = SciDate.parse('3/6/2021')
    assert date.year == 2021
    assert date.month == 6
    assert date.day == 3

    # test parsing from the customised format
    date = SciDate.parse('2020-02-29', '%Y-%m-%d')
    assert date.year == 2020
    assert date.month == 2
    assert date.day == 29


def test_sci_date_parse_errors():
    # unexpected format with extra unknown %s
    with pytest.raises(InvalidDateFormatException):
        SciDate.parse('2020-02-29', '%Y-%m-%d %s')

    # no day specified in the format
    with pytest.raises(InvalidDateFormatException):
        SciDate.parse('2020-02', '%Y-%m')

    # no month and day specified in the format
    with pytest.raises(InvalidDateFormatException):
        SciDate.parse('2021', '%Y')

    # no year and month specified in the format
    with pytest.raises(InvalidDateFormatException):
        SciDate.parse('3', '%d')

    # date doesn't match the format
    with pytest.raises(InvalidDateFormatException):
        SciDate.parse('2021-02-abc', '%Y-%m-%d')


def test_sci_date_sub():
    d1 = SciDate(2021, 7, 16)
    d2 = SciDate(2021, 7, 17)

    # date subtraction, bigger - smaller
    assert d2.sub(d1) == 86400

    # date subtraction, smaller - bigger
    assert d1.sub(d2) == -86400

    # date subtraction, two equal days
    d3 = SciDate(2021, 7, 16)
    assert d3.sub(d1) == 0


def test_days_diff():
    # diff for the same day
    assert days_diff(SciDate(2012, 6, 2), SciDate(2012, 6, 2)) == 0

    # diff for the consecutive two days
    assert days_diff(SciDate(2012, 12, 31), SciDate(2013, 1, 1)) == 0

    # diff for the consecutive two days with first and last days included
    assert days_diff(SciDate(2012, 12, 31), SciDate(2013, 1, 1), include_first=True, include_last=True) == 2

    # diff for the consecutive two days with only first included
    assert days_diff(SciDate(2012, 12, 31), SciDate(2013, 1, 1), include_first=True, include_last=False) == 1

    # diff for the consecutive two days with only first included
    assert days_diff(SciDate(2013, 1, 1), SciDate(2012, 12, 31), include_first=False, include_last=True) == 1

    # diff of alternative two days
    assert days_diff(SciDate(2000, 2, 28), SciDate(2000, 3, 1)) == 1

    # the given test cases
    assert days_diff(SciDate(1983, 6, 2), SciDate(1983, 6, 22)) == 19
    assert days_diff(SciDate(1984, 7, 4), SciDate(1984, 12, 25)) == 173
    assert days_diff(SciDate(1989, 1, 3), SciDate(1983, 8, 3)) == 1979
