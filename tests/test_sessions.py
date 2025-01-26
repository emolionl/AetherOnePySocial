def test_create_session(client):
    response = client.post(
        "/api/sessions/",
        json={
            "intention": "Session Intention",
            "description": "Session description.",
            "case_id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["intention"] == "Session Intention"

def test_get_sessions(client):
    response = client.get("/api/sessions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0