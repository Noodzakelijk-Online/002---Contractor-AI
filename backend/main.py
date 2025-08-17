from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine

# This line creates the database tables if they don't exist.
# In a production environment, this should be handled by Alembic migrations.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Manus AI Brain API")

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Project": "Manus AI Brain"}

# Clients Endpoints
@app.post("/clients/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_email(db, email=client.email)
    if db_client:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_client(db=db, client=client)

@app.get("/clients/", response_model=List[schemas.Client])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = crud.get_clients(db, skip=skip, limit=limit)
    return clients

@app.get("/clients/{client_id}", response_model=schemas.Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

# Jobs Endpoints
@app.post("/jobs/", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db=db, job=job)

@app.get("/jobs/", response_model=List[schemas.Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs

@app.get("/jobs/{job_id}", response_model=schemas.Job)
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@app.patch("/jobs/{job_id}/status", response_model=schemas.Job)
def update_job_status(
    job_id: int,
    status_update: schemas.JobUpdateStatus,
    db: Session = Depends(get_db),
):
    job = crud.get_job(db, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    new_status = status_update.status
    current_status = job.status

    # State machine transition validation
    valid_transitions = {
        models.JobStatus.new_request: [models.JobStatus.approved, models.JobStatus.cancelled],
        models.JobStatus.approved: [models.JobStatus.scheduled, models.JobStatus.cancelled],
        models.JobStatus.scheduled: [models.JobStatus.in_progress, models.JobStatus.cancelled],
        models.JobStatus.in_progress: [models.JobStatus.completed, models.JobStatus.cancelled],
    }

    if new_status not in valid_transitions.get(current_status, []):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from {current_status.value} to {new_status.value}",
        )

    return crud.update_job_status(db=db, job=job, status=new_status)


# Worker Availability Endpoints
@app.post("/worker_availability_exceptions/", response_model=schemas.WorkerAvailabilityException)
def create_worker_availability_exception(
    exception: schemas.WorkerAvailabilityExceptionCreate, db: Session = Depends(get_db)
):
    return crud.create_worker_availability_exception(db=db, exception=exception)
