"""
Tests for the calculator.
"""

from fire import testutils
from scidate.exceptions import InvalidDateException, InvalidDateFormatException

from calculator import calculator


class CalculatorTest(testutils.BaseTestCase):

    def test_calculator(self):
        # the given tests cases
        self.assertEqual(calculator('02/06/1983', '22/6/1983'), '02/06/1983 - 22/6/1983 = 19 days')
        self.assertEqual(calculator('4/07/1984', '25/12/1984'), '4/07/1984 - 25/12/1984 = 173 days')
        self.assertEqual(calculator('03/1/1989', '3/8/1983'), '03/1/1989 - 3/8/1983 = 1979 days')

        # extra test cases with customised date format
        self.assertEqual(calculator('2000-02-28', '2000-03-01', '%Y-%m-%d'), '2000-02-28 - 2000-03-01 = 1 day')

    def test_calculator_invalid_date(self):
        # test invalid date exception
        with self.assertRaises(InvalidDateException):
            calculator('32/06/1983', '22/6/1983')

    def test_calculator_invalid_format(self):
        # test invalid date format exception
        with self.assertRaises(InvalidDateFormatException):
            calculator('1983-06-02', '22/6/1983')


if __name__ == '__main__':
    testutils.main()
