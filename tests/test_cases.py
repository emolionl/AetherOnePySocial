def test_create_case(client):
    response = client.post(
        "/api/cases/",
        json={
            "name": "Test Case",
            "email": "testcase@example.com",
            "color": "red",
            "description": "Test case description."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Case"
    assert data["email"] == "testcase@example.com"

def test_get_cases(client):
    response = client.get("/api/cases/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0