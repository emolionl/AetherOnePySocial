def test_create_comparison(client):
    response = client.post(
        "/api/comparison/",
        json={
            "merged_analysis_id": 1,
            "comparison_notes": "Comparison notes."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["comparison_notes"] == "Comparison notes."

def test_get_comparisons(client):
    response = client.get("/api/comparison/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0