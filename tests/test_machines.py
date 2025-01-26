def test_create_machine(client):
    response = client.post(
        "/api/machines/",
        json={
            "machine_name": "Machine1",
            "description": "Test machine",
            "api_key": "1234"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["machine_name"] == "Machine1"
    assert data["description"] == "Test machine"

def test_get_machines(client):
    client.post(
        "/api/machines/",
        json={
            "machine_name": "Machine2",
            "description": "Another test machine",
            "api_key": "5678"
        }
    )
    response = client.get("/api/machines/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["machine_name"] == "Machine1"