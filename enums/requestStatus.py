from enum import Enum

class ReqStatus(str, Enum):
    PENDING = "PENDING"
    DECLINED = "DECLINED"
    FORWARD = "FORWARD"
    BOOKED = "BOOKED"