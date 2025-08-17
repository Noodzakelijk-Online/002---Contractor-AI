import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

from ..main import app, get_db
from ..database import Base
from .. import models

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    # Drop the database tables after the test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    A fixture that provides a test client for the API.
    """
    yield TestClient(app)


def test_create_client(client):
    """
    Test creating a new client.
    """
    response = client.post(
        "/clients/",
        json={
            "full_name": "Test Client",
            "email": "test@example.com",
            "phone_number": "1234567890",
            "address": "123 Test St",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test Client"
    assert "id" in data


def test_read_clients(client, db_session):
    """
    Test reading a list of clients.
    """
    # Create a client first
    client.post(
        "/clients/",
        json={
            "full_name": "Test Client 1",
            "email": "test1@example.com",
        },
    )
    client.post(
        "/clients/",
        json={
            "full_name": "Test Client 2",
            "email": "test2@example.com",
        },
    )

    response = client.get("/clients/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["full_name"] == "Test Client 1"
    assert data[1]["full_name"] == "Test Client 2"


def test_create_job(client, db_session):
    """
    Test creating a new job.
    """
    # First, create a client to associate the job with
    client_response = client.post(
        "/clients/",
        json={"full_name": "Job Client", "email": "job_client@example.com"},
    )
    client_id = client_response.json()["id"]

    response = client.post(
        "/jobs/",
        json={
            "description": "Test job description",
            "client_id": client_id,
            "status": "new_request",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test job description"
    assert data["client_id"] == client_id
    assert "id" in data


def test_update_job_status_valid(client, db_session):
    """
    Test valid state transitions for a job.
    """
    client_res = client.post("/clients/", json={"full_name": "Status Client", "email": "status@example.com"})
    job_res = client.post("/jobs/", json={"description": "Status Test Job", "client_id": client_res.json()["id"]})
    job_id = job_res.json()["id"]

    # Test new_request -> approved
    response = client.patch(f"/jobs/{job_id}/status", json={"status": "approved"})
    assert response.status_code == 200
    assert response.json()["status"] == "approved"

    # Test approved -> scheduled
    response = client.patch(f"/jobs/{job_id}/status", json={"status": "scheduled"})
    assert response.status_code == 200
    assert response.json()["status"] == "scheduled"

    # Test scheduled -> in_progress
    response = client.patch(f"/jobs/{job_id}/status", json={"status": "in_progress"})
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

    # Test in_progress -> completed
    response = client.patch(f"/jobs/{job_id}/status", json={"status": "completed"})
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_update_job_status_invalid(client, db_session):
    """
    Test an invalid state transition for a job.
    """
    client_res = client.post("/clients/", json={"full_name": "Invalid Status Client", "email": "invalid@example.com"})
    job_res = client.post("/jobs/", json={"description": "Invalid Status Test Job", "client_id": client_res.json()["id"]})
    job_id = job_res.json()["id"]

    # Test new_request -> scheduled (invalid)
    response = client.patch(f"/jobs/{job_id}/status", json={"status": "scheduled"})
    assert response.status_code == 400
    assert "Invalid status transition" in response.json()["detail"]


def test_create_worker_availability_exception(client, db_session):
    """
    Test creating a worker availability exception.
    """
    # First, create a worker user
    # Note: User creation endpoint is not implemented yet, so we create it directly in the DB for this test.
    worker = models.User(
        full_name="Test Worker",
        email="worker@example.com",
        role="worker",
        hashed_password="fake_password",
    )
    db_session.add(worker)
    db_session.commit()
    db_session.refresh(worker)

    start_time = datetime.datetime.now(datetime.timezone.utc)
    end_time = start_time + datetime.timedelta(hours=2)

    response = client.post(
        "/worker_availability_exceptions/",
        json={
            "worker_id": worker.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "is_unavailable": True,
            "reason": "Doctor's appointment",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["worker_id"] == worker.id
    assert data["reason"] == "Doctor's appointment"
