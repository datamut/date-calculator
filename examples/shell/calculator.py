"""
A simple command-line tool to do the dedicated date calculation for the scientific experiment.
"""

import fire
from scidate.scidate import SciDate, days_diff


def calculator(first_day: str, last_day: str, fmt: str = '%d/%m/%Y'):
    day1 = SciDate.parse(first_day, fmt)
    day2 = SciDate.parse(last_day, fmt)
    days = days_diff(day1, day2, include_first=False, include_last=False)
    return f'{first_day} - {last_day} = {days} {"days" if days > 1 else "day"}'


if __name__ == '__main__':
    fire.Fire(calculator)
