# test session keys
# pytest tests/test_session_keys.py -v --local_session_id=123
# machine_id is not needed for this test, because we need to check at 
# /api/shared-analysis endpoint if there is session that is already shared
# with this key, because someone could share also same with user_id and session_id
# but machine ID could be different if someone is working different raspberry pies of different machines
# with out warnings pytest tests/test_session_keys.py -v -p no:warnings
# THIS SHOULD BE RUNNING pytest tests/test_session_keys.py -v -p no:warnings -s

import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base, engine, SessionLocal
from app.models.user import User
import uuid  # Add this import at the top

class TestAuth:
    client = TestClient(app)
    local_url = "http://localhost:8000"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    username = f"testuser_{timestamp}"
    email = f"test_{timestamp}@example.com"
    password = "testpass"
    token = None
    user_id = None
    local_session_id = 123
    session_key = None

    @pytest.mark.order(1)
    def test_ping(self):
        response = self.client.get(f"{self.local_url}/ping")
        assert response.status_code == 200
        assert response.json() == {"message": "pong"}
    @pytest.mark.order(2)
    def test_register(self):
        response = self.client.post(
            f"{self.local_url}/api/auth/register",
            json={
                "username": self.username,
                "email": self.email,
                "password": self.password
            }
        )
        #print(f"Response: {response.json()}")
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        TestAuth.user_id = data["user_id"]
        assert data["username"] == self.username
        assert data["email"] == self.email
    @pytest.mark.order(3)
    def test_get_token(self):
        response = self.client.post(
            f"{self.local_url}/api/auth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "username": self.email,
                "password": self.password
            }

        )
        #print(f"Response: {response.json()}")
        assert response.status_code == 200
        assert response.json()["email"] == self.email
        assert response.json()["username"] == self.username
        assert response.json()["user_id"] == self.user_id
        TestAuth.token = response.json().get("access_token")
        assert self.token is not None
    @pytest.mark.order(4)
    def test_create_session_key(self):
        token = self.token
        response = self.client.post(
            "/api/session-keys/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "user_id": self.user_id,
                "local_session_id": self.local_session_id
            }
        )
        assert response.status_code == 200
        assert response.json()["status"] == "created"
        assert "key" in response.json()
        assert response.json()["user_id"] == self.user_id
        assert response.json()["local_session_id"] == self.local_session_id
        TestAuth.session_key = response.json()["key"]
    @pytest.mark.order(5)
    def test_create_duplicate_user_key(self):
        token = self.token
        # Create first key
        response = self.client.post(
            "/api/session-keys/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "user_id": self.user_id,
                "local_session_id": self.local_session_id
            }
        )
        #print(f"Response: {response.json()}")
        assert response.status_code == 200
        assert response.json()["status"] == "exists"
        assert response.json()["message"] == "Session key already exists for this user in combination with local_session_id"
        assert "key" in response.json()
    @pytest.mark.order(6)
    def test_create_with_existing_combination(self):
        token = self.token
        test_key = self.session_key
        # Create first key
        response = self.client.post(
            "/api/session-keys/",
            headers={"Authorization": f"Bearer {token}"},

            json={
                "user_id": self.user_id,
                "local_session_id": self.local_session_id,
                "key": test_key
            }
        )
    
        assert response.status_code == 200
        assert response.json()["status"] == "error"
        assert "This combination of user_id" in response.json()["message"]
    @pytest.mark.order(7)
    def test_unauthorized_access(self):
        response = self.client.post(
            "/api/session-keys/",
            json={
                "user_id": self.user_id,
                "local_session_id": self.local_session_id
            }
        )
        #print(f"Response: {response.json()}")
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]
    @pytest.mark.order(8)
    def test_wrong_user_id(self):
        token = self.token
        response = self.client.post(
            "/api/session-keys/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "user_id": self.user_id + 1,
                "local_session_id": self.local_session_id
            }
        )
        #print(f"Response: {response.json()}")
        assert response.status_code == 403
        assert "Not authorized to create/update session keys for other users" in response.json()["detail"]
    @pytest.mark.order(9)
    def test_create_key_different_session_id(self):
        token = self.token
        # Create first key
        response1 = self.client.post(
            f"{self.local_url}/api/session-keys/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "user_id": self.user_id,
                "local_session_id": self.local_session_id + 1
            }
        )
        #print(f"First Response: {response1.json()}")
        assert response1.status_code == 200
        assert response1.json()["status"] == "created"
        
        # Create second key with different local_session_id
        response2 = self.client.post(
            f"{self.local_url}/api/session-keys/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "user_id": self.user_id,
                "local_session_id": self.local_session_id + 2  # Different local_session_id
            }
        )
        #print(f"Second Response: {response2.json()}")
        
        # Assert success response
        assert response2.status_code == 200
        data = response2.json()
        assert data["status"] == "created"
        assert "key" in data
        assert data["user_id"] == self.user_id
        assert data["local_session_id"] == self.local_session_id + 2
    @pytest.mark.order(10)
    def test_upload_shared_analysis(self):
        # Prepare the analysis data
        analysis_data = {
            "data": {
                "analyses": {
                    "analyses": [
                        {
                            "analysis": {
                                "catalog_id": 2,
                                "created": "2025-01-27T14:11:40",
                                "id": 9,
                                "name": None,
                                "session_id": 7,
                                "target_gv": 699
                            },
                            "catalog": {
                                "description": "radionics-rates",
                                "id": 2,
                                "name": "emotions"
                            },
                            "rate_analysis": [
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 1002,
                                "gv": 962,
                                "id": 1,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "8989",
                                "signature": "wary"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 948,
                                "gv": 870,
                                "id": 2,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "jkjkjkjk",
                                "signature": "crazy"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 939,
                                "gv": 798,
                                "id": 3,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "dsdsds",
                                "signature": "tranquil"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 933,
                                "gv": 726,
                                "id": 4,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "dsdsd",
                                "signature": "scared"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 922,
                                "gv": 851,
                                "id": 5,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "dsdsds",
                                "signature": "tense"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 898,
                                "gv": 893,
                                "id": 6,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "dsdsdsdsds",
                                "signature": "mad"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 893,
                                "gv": 305,
                                "id": 7,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "fdfdfd",
                                "signature": "sunny"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 892,
                                "gv": 670,
                                "id": 8,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "fdfdfd",
                                "signature": "lively"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 889,
                                "gv": 580,
                                "id": 9,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "gfgffg",
                                "signature": "afraid"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 887,
                                "gv": 477,
                                "id": 10,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "",
                                "signature": "angry"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 886,
                                "gv": 541,
                                "id": 11,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "",
                                "signature": "upbeat"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 866,
                                "gv": 582,
                                "id": 12,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "",
                                "signature": "icy"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 865,
                                "gv": 1086,
                                "id": 13,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "",
                                "signature": "cross"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 865,
                                "gv": 639,
                                "id": 14,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "",
                                "signature": "ornery"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 857,
                                "gv": 898,
                                "id": 15,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "",
                                "signature": "crabby"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 852,
                                "gv": 877,
                                "id": 16,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "",
                                "signature": "sad"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 848,
                                "gv": 591,
                                "id": 17,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "",
                                "signature": "glum"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 844,
                                "gv": 853,
                                "id": 18,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "",
                                "signature": "happy"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 841,
                                "gv": 916,
                                "id": 19,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "",
                                "signature": "shy"
                            },
                            {
                                "analysis_id": 9,
                                "catalog_id": 2,
                                "description": None,
                                "energetic_value": 824,
                                "gv": 817,
                                "id": 20,
                                "level": 0,
                                "note": "",
                                "potency": 0,
                                "potencyType": "",
                                "signature": "frigid"
                            }
                        ],
                            "rates": [
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 13,
                                    "signature": "afraid"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 14,
                                    "signature": "angry"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 15,
                                    "signature": "calm"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 16,
                                    "signature": "cheerful"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 17,
                                    "signature": "cold"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 18,
                                    "signature": "crabby"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 19,
                                    "signature": "crazy"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 20,
                                    "signature": "cross"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 21,
                                    "signature": "excited"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 22,
                                    "signature": "frigid"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 23,
                                    "signature": "furious"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 24,
                                    "signature": "glad"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 25,
                                    "signature": "glum"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 26,
                                    "signature": "happy"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 27,
                                    "signature": "icy"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 28,
                                    "signature": "jolly"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 29,
                                    "signature": "jovial"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 30,
                                    "signature": "kind"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 31,
                                    "signature": "lively"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 32,
                                    "signature": "livid"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 33,
                                    "signature": "mad"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 34,
                                    "signature": "ornery"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 35,
                                    "signature": "rosy"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 36,
                                    "signature": "sad"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 37,
                                    "signature": "scared"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 38,
                                    "signature": "seething"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 39,
                                    "signature": "shy"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 40,
                                    "signature": "sunny"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 41,
                                    "signature": "tense"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 42,
                                    "signature": "tranquil"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 43,
                                    "signature": "upbeat"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 44,
                                    "signature": "wary"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 45,
                                    "signature": "weary"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 46,
                                    "signature": "worried"
                                }
                            ]
                        }
                    ],
                    "case": {
                        "color": "#303de8",
                        "created": "2025-01-27T14:10:50",
                        "description": "test6",
                        "email": "test6@test.com",
                        "id": 6,
                        "last_change": "Mon, 27 Jan 2025 14:10:50 GMT",
                        "name": "test6"
                    },
                    "session": {
                        "case_id": 6,
                        "created": "2025-01-27T14:11:18",
                        "description": "test6",
                        "id": 7,
                        "intention": "test6"
                    }
                },
                "key": self.session_key,
                "machine_id": "machine_id",
                "session_id": 7,
                "user_id": self.user_id  # Use the registered user_id
            },
            "message": "Found 3 analyses with their related data",
            "status": "success"
        }

        # Upload the analysis
        response = self.client.post(
            f"{self.local_url}/api/shared-analysis",
            headers={"Authorization": f"Bearer {self.token}"},
            json=analysis_data
        )
        
        print(f"Upload Response: {response.json()}")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
    @pytest.mark.order(11)
    def test_get_shared_analysis_by_key(self):
        # Use the session_key that was created in earlier tests
        valid_key = self.session_key  # This should already be a valid UUID from earlier tests
        print(f"Valid Key: {valid_key}")
        print(f"Token: {self.token}")
        # Now test getting the analysis by key
        response = self.client.get(
            f"{self.local_url}/api/shared-analysis/by-key/{valid_key}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["status_code"] == 200
        assert data["message"] == "Sessions retrieved successfully"
        assert "data" in data
        
        # Test non-existent key (using a random UUID)
        non_existent_uuid = str(uuid.uuid4())
        response = self.client.get(
            f"{self.local_url}/api/shared-analysis/by-key/{non_existent_uuid}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 404
        
        # Test unauthorized access (using a different user)
        # First create a new user
        new_user_response = self.client.post(
            f"{self.local_url}/api/auth/register",
            json={
                "username": f"{self.username}_2",
                "email": f"test2_{self.timestamp}@example.com",
                "password": self.password
            }
        )
        assert new_user_response.status_code == 200
        new_user_token = new_user_response.json()["access_token"]
        
        # Try to access the original user's shared analysis
        response = self.client.get(
            f"{self.local_url}/api/shared-analysis/by-key/{valid_key}",
            headers={"Authorization": f"Bearer {new_user_token}"}
        )
        assert response.status_code == 403

    @pytest.mark.order(12)
    def test_get_shared_analysis_by_key_add_session_other_user(self):
        # Use the session_key that was created in earlier tests
        valid_key = self.session_key

        # Create a new user first
        new_user_response = self.client.post(
            f"{self.local_url}/api/auth/register",
            json={
                "username": f"{self.username}_3",
                "email": f"test3_{self.timestamp}@example.com",
                "password": self.password
            }
        )
        assert new_user_response.status_code == 200
        new_user_token = new_user_response.json()["access_token"]
        new_user_id = new_user_response.json()["user_id"]

        # Prepare the analysis data for the new user
        analysis_data = {
            "data": {
                "analyses": {
                    "analyses": [
                        {
                            "analysis": {
                                "catalog_id": 2,
                                "created": "2025-01-27T14:11:40",
                                "id": 10,  # Different ID
                                "name": None,
                                "session_id": 8,  # Different session_id
                                "target_gv": 699
                            },
                            "catalog": {
                                "description": "radionics-rates",
                                "id": 2,
                                "name": "emotions"
                            },
                            "rate_analysis": [
                                {
                                    "analysis_id": 10,  # Match with new analysis id
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 1002,
                                    "gv": 962,
                                    "id": 21,  # Different ID
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "8989",
                                    "signature": "wary"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 1002,
                                    "gv": 962,
                                    "id": 1,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "8989",
                                    "signature": "wary"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 948,
                                    "gv": 870,
                                    "id": 2,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "jkjkjkjk",
                                    "signature": "crazy"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 939,
                                    "gv": 798,
                                    "id": 3,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "dsdsds",
                                    "signature": "tranquil"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 933,
                                    "gv": 726,
                                    "id": 4,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "dsdsd",
                                    "signature": "scared"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 922,
                                    "gv": 851,
                                    "id": 5,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "dsdsds",
                                    "signature": "tense"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 898,
                                    "gv": 893,
                                    "id": 6,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "dsdsdsdsds",
                                    "signature": "mad"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 893,
                                    "gv": 305,
                                    "id": 7,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "fdfdfd",
                                    "signature": "sunny"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 892,
                                    "gv": 670,
                                    "id": 8,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "fdfdfd",
                                    "signature": "lively"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 889,
                                    "gv": 580,
                                    "id": 9,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "gfgffg",
                                    "signature": "afraid"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 887,
                                    "gv": 477,
                                    "id": 10,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "",
                                    "signature": "angry"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 886,
                                    "gv": 541,
                                    "id": 11,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "",
                                    "signature": "upbeat"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 866,
                                    "gv": 582,
                                    "id": 12,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "",
                                    "signature": "icy"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 865,
                                    "gv": 1086,
                                    "id": 13,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "",
                                    "signature": "cross"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 865,
                                    "gv": 639,
                                    "id": 14,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "",
                                    "signature": "ornery"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 857,
                                    "gv": 898,
                                    "id": 15,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "",
                                    "signature": "crabby"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 852,
                                    "gv": 877,
                                    "id": 16,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "",
                                    "signature": "sad"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 848,
                                    "gv": 591,
                                    "id": 17,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "",
                                    "signature": "glum"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 844,
                                    "gv": 853,
                                    "id": 18,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "",
                                    "signature": "happy"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 841,
                                    "gv": 916,
                                    "id": 19,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "",
                                    "signature": "shy"
                                },
                                {
                                    "analysis_id": 9,
                                    "catalog_id": 2,
                                    "description": None,
                                    "energetic_value": 824,
                                    "gv": 817,
                                    "id": 20,
                                    "level": 0,
                                    "note": "",
                                    "potency": 0,
                                    "potencyType": "",
                                    "signature": "frigid"
                                }
                            ],
                            "rates": [
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 13,
                                    "signature": "afraid"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 14,
                                    "signature": "angry"

                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 15,
                                    "signature": "calm"

                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 16,
                                    "signature": "cheerful"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 17,
                                    "signature": "cold"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 18,
                                    "signature": "crabby"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 19,
                                    "signature": "crazy"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 20,
                                    "signature": "cross"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 21,
                                    "signature": "excited"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 22,
                                    "signature": "frigid"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 23,
                                    "signature": "furious"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 24,
                                    "signature": "glad"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 25,
                                    "signature": "glum"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 26,
                                    "signature": "happy"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 27,
                                    "signature": "icy"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 28,
                                    "signature": "jolly"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 29,
                                    "signature": "jovial"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 30,
                                    "signature": "kind"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 31,
                                    "signature": "lively"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 32,
                                    "signature": "livid"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 33,
                                    "signature": "mad"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 34,
                                    "signature": "ornery"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 35,
                                    "signature": "rosy"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 36,
                                    "signature": "sad"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 37,
                                    "signature": "scared"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 38,
                                    "signature": "seething"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 39,
                                    "signature": "shy"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 40,
                                    "signature": "sunny"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 41,
                                    "signature": "tense"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 42,
                                    "signature": "tranquil"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 43,
                                    "signature": "upbeat"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 44,
                                    "signature": "wary"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 45,
                                    "signature": "weary"
                                },
                                {
                                    "catalog_id": 2,
                                    "description": None,
                                    "id": 46,
                                    "signature": "worried"
                                }
                            ]
                        }
                    ],
                    "case": {
                        "color": "#303de8",
                        "created": "2025-01-27T14:10:50",
                        "description": "test7",
                        "email": "test7@test.com",
                        "id": 7,
                        "last_change": "Mon, 27 Jan 2025 14:10:50 GMT",
                        "name": "test7"
                    },
                    "session": {
                        "case_id": 7,
                        "created": "2025-01-27T14:11:18",
                        "description": "test7",
                        "id": 8,
                        "intention": "test7"
                    }
                },
                "key": valid_key,  # Use the same key as before
                "machine_id": "machine_id_2",  # Different machine_id
                "session_id": 8,
                "user_id": new_user_id  # Use the new user's ID
            },
            "message": "Found 1 analysis with related data",
            "status": "success"
        }
        #print(f"Analysis Data: some")
        #return "data some"
        # Upload the analysis with the new user's token
        response = self.client.post(
            f"{self.local_url}/api/shared-analysis",
            headers={"Authorization": f"Bearer {new_user_token}"},
            json=analysis_data
        )
        
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        return "data some"
        # Now verify we can get both users' analyses using the key
        response = self.client.get(
            f"{self.local_url}/api/shared-analysis/by-key/{valid_key}",
            headers={"Authorization": f"Bearer {new_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) >= 2  # Should have at least 2 sessions (one from each user)
        
        # Verify we can find both user IDs in the response
        user_ids = {session["user_id"] for session in data["data"]}
        assert self.user_id in user_ids
        assert new_user_id in user_ids