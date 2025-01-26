def test_create_merged_analysis(client):
    response = client.post(
        "/api/merged-analysis/",
        json={
            "analysis_ids": "1,2",
            "user_id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["analysis_ids"] == "1,2"

def test_get_merged_analyses(client):
    response = client.get("/api/merged-analysis/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0