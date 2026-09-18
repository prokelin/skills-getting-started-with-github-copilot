from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_participant_removes_email():
    activity = activities["Chess Club"]
    original_participants = activity["participants"][:]

    try:
        new_email = "teststudent@mergington.edu"
        activity["participants"].append(new_email)

        response = client.delete("/activities/Chess Club/signup", params={"email": new_email})

        assert response.status_code == 200
        assert new_email not in activity["participants"]
        assert response.json()["message"] == f"Unregistered {new_email} from Chess Club"
    finally:
        activity["participants"] = original_participants
