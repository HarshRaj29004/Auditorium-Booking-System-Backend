from pydantic import BaseModel, EmailStr, constr, Field
from typing import List, Optional
from datetime import datetime
from enums.role import role

class Token(BaseModel):
    token: str
    createdAt: Optional[datetime] = Field(default_factory=datetime.utcnow)

class User(BaseModel):
    email: EmailStr
    username: Optional[constr(strip_whitespace=True, min_length=3, max_length=50)] = None
    password: constr(min_length=8)
    role: Optional[str] = Field(default=role.USER, pattern=f"^({role.SUPERADMIN}|{role.SUBADMIN}|{role.USER})$")
    tokens: Optional[List[Token]] = []
    lastLogin: Optional[datetime] = None
    isActive: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
