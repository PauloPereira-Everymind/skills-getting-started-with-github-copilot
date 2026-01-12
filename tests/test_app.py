import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity():
    response = client.post("/activities/Chess Club/signup", params={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up test@example.com for Chess Club"}

def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Programming Class/signup", params={"email": "test2@example.com"})
    # Try again
    response = client.post("/activities/Programming Class/signup", params={"email": "test2@example.com"})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "test@example.com"})
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister():
    # Signup first
    client.post("/activities/Gym Class/signup", params={"email": "test3@example.com"})
    # Unregister
    response = client.post("/activities/Gym Class/unregister", params={"email": "test3@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "Unregistered test3@example.com from Gym Class"}

def test_unregister_not_signed_up():
    response = client.post("/activities/Gym Class/unregister", params={"email": "notsigned@example.com"})
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]

def test_unregister_activity_not_found():
    response = client.post("/activities/Nonexistent/unregister", params={"email": "test@example.com"})
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]