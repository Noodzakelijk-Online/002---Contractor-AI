from pydantic import BaseModel
from typing import Optional
import datetime
from .models import JobStatus, UserRole

# Base schemas
class ClientBase(BaseModel):
    full_name: str
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None

class JobBase(BaseModel):
    description: str
    client_id: int
    worker_id: Optional[int] = None
    status: JobStatus = JobStatus.new_request

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None

class ToolBase(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int = 1


# Schemas for creation (request body)
class ClientCreate(ClientBase):
    pass

class JobCreate(JobBase):
    pass

class UserCreate(UserBase):
    password: str
    role: UserRole

class ToolCreate(ToolBase):
    pass


# Schemas for reading (response body)
class Client(ClientBase):
    id: int

    class Config:
        orm_mode = True

class Job(JobBase):
    id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    scheduled_start_time: Optional[datetime.datetime] = None
    scheduled_end_time: Optional[datetime.datetime] = None
    actual_start_time: Optional[datetime.datetime] = None
    actual_end_time: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    is_active: bool
    role: UserRole

    class Config:
        orm_mode = True

class Tool(ToolBase):
    id: int

    class Config:
        orm_mode = True
