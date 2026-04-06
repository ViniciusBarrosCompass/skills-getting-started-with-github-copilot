import copy
from urllib.parse import quote

from src.app import activities


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity = copy.deepcopy(activities["Chess Club"])

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    json_data = response.json()
    assert "Chess Club" in json_data
    assert json_data["Chess Club"] == expected_activity
    assert isinstance(json_data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/signup"
    previous_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert len(activities[activity_name]["participants"]) == previous_count + 1
    assert activities[activity_name]["participants"][-1] == email


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/signup"

    # Act
    first_response = client.post(endpoint, params={"email": email})
    second_response = client.post(endpoint, params={"email": email})

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_participant(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/signup"
    assert email in activities[activity_name]["participants"]

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]


def test_unregister_nonexistent_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.signed@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
