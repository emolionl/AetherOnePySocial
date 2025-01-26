def test_create_rate(client):
    response = client.post(
        "/api/rates/",
        json={
            "signature": "Rate Signature",
            "description": "Rate description.",
            "catalog_id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["signature"] == "Rate Signature"
    assert data["description"] == "Rate description."

def test_get_rates(client):
    response = client.get("/api/rates/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0