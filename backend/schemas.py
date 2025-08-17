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
    default_start_time: Optional[datetime.time] = None
    default_end_time: Optional[datetime.time] = None

class ToolBase(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int = 1


# Schemas for creation (request body)
class ClientCreate(ClientBase):
    pass

class JobCreate(JobBase):
    pass

class JobUpdateStatus(BaseModel):
    status: JobStatus

class UserCreate(UserBase):
    password: str
    role: UserRole

class ToolCreate(ToolBase):
    pass


# Schemas for Worker Availability
class WorkerAvailabilityExceptionBase(BaseModel):
    start_time: datetime.datetime
    end_time: datetime.datetime
    is_unavailable: bool = True
    reason: Optional[str] = None

class WorkerAvailabilityExceptionCreate(WorkerAvailabilityExceptionBase):
    worker_id: int

class WorkerAvailabilityException(WorkerAvailabilityExceptionBase):
    id: int
    worker_id: int

    class Config:
        orm_mode = True


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
