from sqlalchemy.orm import Session
from . import models, schemas

# Client CRUD
def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()

def get_client_by_email(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email == email).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()

def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(
        full_name=client.full_name,
        email=client.email,
        phone_number=client.phone_number,
        address=client.address,
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# Job CRUD
def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job).offset(skip).limit(limit).all()

def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def update_job_status(db: Session, job: models.Job, status: schemas.JobStatus):
    job.status = status
    db.commit()
    db.refresh(job)
    return job

# Worker Availability CRUD
def create_worker_availability_exception(
    db: Session, exception: schemas.WorkerAvailabilityExceptionCreate
):
    db_exception = models.WorkerAvailabilityException(**exception.dict())
    db.add(db_exception)
    db.commit()
    db.refresh(db_exception)
    return db_exception

def get_worker_availability_exceptions(
    db: Session, worker_id: int, start_time: schemas.datetime, end_time: schemas.datetime
):
    return (
        db.query(models.WorkerAvailabilityException)
        .filter(
            models.WorkerAvailabilityException.worker_id == worker_id,
            models.WorkerAvailabilityException.start_time < end_time,
            models.WorkerAvailabilityException.end_time > start_time,
        )
        .all()
    )
