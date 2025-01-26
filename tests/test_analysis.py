def test_create_analysis(client):
    response = client.post(
        "/api/analysis/",
        json={
            "note": "Analysis note.",
            "target_gv": 50,
            "session_id": 1,
            "catalog_id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["note"] == "Analysis note."

def test_get_analyses(client):
    response = client.get("/api/analysis/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0