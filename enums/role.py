from enum import Enum

class role(str,Enum):
    SUBADMIN = "SUBADMIN"
    SUPERADMIN = "SUPERADMIN"
    USER = "USER"