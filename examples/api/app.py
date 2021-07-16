"""
A simple API to do the dedicated date calculation for the scientific experiment.
"""

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from scidate.scidate import SciDate, days_diff
from scidate.exceptions import InvalidDateException, InvalidDateFormatException

app = FastAPI()


class CalculatorRequest(BaseModel):
    """
    The calculator request model
    """
    first_day: str
    last_day: str
    fmt: Optional[str] = '%d/%m/%Y'


class CalculatorResponse(BaseModel):
    """
    The calculator response model
    """
    first_day: str
    last_day: str
    days: int


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def home():
    """
    Redirect home page to API docs
    """
    return '/docs'


@app.post('/calculator', response_model=CalculatorResponse)
async def calculator(req: CalculatorRequest):
    """
    The endpoint to do the date calculation.

    :param req: The request object
    :return: The response object
    """
    try:
        day1 = SciDate.parse(req.first_day, req.fmt)
        day2 = SciDate.parse(req.last_day, req.fmt)
        days = days_diff(day1, day2, include_first=False, include_last=False)
    except (InvalidDateException, InvalidDateFormatException) as ex:
        raise HTTPException(status_code=500, detail=f'Failed to parse date {req}, error: {str(ex)}')
    else:
        return CalculatorResponse(first_day=req.first_day, last_day=req.last_day, days=days)
