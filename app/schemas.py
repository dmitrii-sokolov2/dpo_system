from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class ProgramBase(BaseModel):
    name: str
    code: Optional[str] = None
    hours: Optional[int] = None
    form: Optional[str] = None


class ProgramCreate(ProgramBase):
    pass


class ProgramOut(ProgramBase):
    id: int

    class Config:
        from_attributes = True


class ListenerBase(BaseModel):
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    snils: Optional[str] = None
    organization: Optional[str] = None


class ListenerCreate(ListenerBase):
    pass


class ListenerOut(ListenerBase):
    id: int

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    listener_id: int
    program_id: int
    comment: Optional[str] = None


class ApplicationOut(BaseModel):
    id: int
    listener_id: int
    program_id: int
    status: str
    created_at: Optional[date]
    comment: Optional[str]

    class Config:
        from_attributes = True