from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional, Literal
from datetime import datetime,date
from enums.requestStatus import ReqStatus
from enums.role import role

class Ticket(BaseModel):
    username: str
    email: EmailStr
    mobileno: constr(strip_whitespace=True)
    user_id: str
    eventdescription: constr(strip_whitespace=True)
    date: date
    clubname: Optional[str] = None
    requestType: Literal["club", "teacher"]
    status: Literal[ReqStatus.PENDING, ReqStatus.FORWARD, ReqStatus.BOOKED, ReqStatus.DECLINED] = ReqStatus.PENDING
    approvedBy: Optional[str] = None
    file: Optional[str] = None
    startTime: str
    endTime: str
