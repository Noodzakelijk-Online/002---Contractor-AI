import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app, get_db
from ..database import Base

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
