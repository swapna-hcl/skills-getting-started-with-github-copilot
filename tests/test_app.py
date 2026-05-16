import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
from copy import deepcopy

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Save and restore the original activities for test isolation
    original = deepcopy(activities)
    yield
    activities.clear()
    activities.update(deepcopy(original))

def test_get_activities():
    # Arrange
    client = TestClient(app)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    # Arrange
    test_email = "newstudent@mergington.edu"
    activity = "Chess Club"
    client = TestClient(app)
    # Act
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 200
    assert test_email in activities[activity]["participants"]

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    client = TestClient(app)
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()

def test_signup_activity_not_found():
    # Arrange
    client = TestClient(app)
    # Act
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_unregister_success():
    # Arrange
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    client = TestClient(app)
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]

def test_unregister_not_found():
    # Arrange
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    client = TestClient(app)
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
