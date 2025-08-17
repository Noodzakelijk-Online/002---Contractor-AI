from sqlalchemy.orm import Session
from datetime import datetime, time
from typing import List
from . import models, crud

def is_worker_available(
    db: Session, worker_id: int, start_time: datetime, end_time: datetime
) -> bool:
    """
    Check if a worker is available for a given time range.
    """
    worker = db.query(models.User).filter(models.User.id == worker_id).first()
    if not worker or worker.role != models.UserRole.worker:
        return False

    # Check against default schedule
    if worker.default_start_time and worker.default_end_time:
        if (
            start_time.time() < worker.default_start_time
            or end_time.time() > worker.default_end_time
        ):
            return False

    # Check for any unavailability exceptions that overlap with the requested time
    exceptions = crud.get_worker_availability_exceptions(
        db, worker_id=worker_id, start_time=start_time, end_time=end_time
    )

    for exc in exceptions:
        if exc.is_unavailable:
            return False

    # Note: This logic does not yet handle cases where an exception makes a worker *available*
    # outside their default hours. This can be added later.

    return True


def find_available_workers(
    db: Session, start_time: datetime, end_time: datetime
) -> List[models.User]:
    """
    Find all workers who are available for a given time range.
    """
    # Note: This is a simplified implementation. A real implementation would need
    # to handle pagination and be more efficient.
    all_workers = db.query(models.User).filter(models.User.role == models.UserRole.worker).all()

    available_workers = []
    for worker in all_workers:
        if is_worker_available(db, worker.id, start_time, end_time):
            available_workers.append(worker)

    return available_workers
