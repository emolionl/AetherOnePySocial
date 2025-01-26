def test_create_catalog(client):
    response = client.post(
        "/api/catalog/",
        json={
            "name": "Test Catalog",
            "description": "This is a test catalog.",
            "author": "Test Author"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Catalog"
    assert data["author"] == "Test Author"

def test_get_catalog(client):
    client.post(
        "/api/catalog/",
        json={
            "name": "Another Catalog",
            "description": "Another test catalog.",
            "author": "Author Name"
        }
    )
    response = client.get("/api/catalog/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Test Catalog"