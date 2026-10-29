import unittest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from backend.main import app
from Nimisha.services.profile_service import ProfileService
from Nimisha.schemas.profile import (
    ProfileBase,
    ProfileCreate,
    ProfileInDB,
    ProfileResponse,
    ProfileUpdate,
    PROFILES_COLLECTION,
    PROFILES_COLLECTION_VALIDATOR,
    PROFILES_INDEXES,
)
from database.mongodb import check_mongodb_connection, get_mongodb_uri, get_database_name


class TestNimishaProfileAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.service = ProfileService()

    def setUp(self):
        self.service.clear_all()

    def test_01_create_profile_success(self):
        payload = {
            "name": "Nimisha Mangal",
            "age": 21,
            "gender": "Female",
            "state": "Rajasthan",
            "district": "Jaipur",
            "income": 250000.0,
            "occupation": "Student",
            "category": "General",
            "disability_status": "No",
            "qualification": "B.Tech Data Science"
        }
        response = self.client.post("/api/profile", json=payload)
        self.assertEqual(response.status_code, 201)

        data = response.json()
        self.assertIn("profile_id", data)
        self.assertTrue(data["profile_id"].startswith("prof_"))
        self.assertEqual(data["name"], "Nimisha Mangal")
        self.assertEqual(data["age"], 21)
        self.assertEqual(data["state"], "Rajasthan")
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)

    def test_02_create_profile_validation_error_invalid_age(self):
        payload = {
            "name": "Invalid User",
            "age": -5,  # Invalid negative age
            "gender": "Male",
            "state": "Rajasthan",
            "district": "Jaipur",
            "income": 100000.0,
            "occupation": "Farmer",
            "category": "OBC"
        }
        response = self.client.post("/api/profile", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_03_create_profile_validation_error_missing_field(self):
        payload = {
            "name": "Incomplete User",
            "age": 30
            # missing gender, state, district, income, occupation, category
        }
        response = self.client.post("/api/profile", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_04_get_profile_success(self):
        payload = {
            "name": "Rohan Sharma",
            "age": 28,
            "gender": "Male",
            "state": "Delhi",
            "district": "North Delhi",
            "income": 180000.0,
            "occupation": "Artisan",
            "category": "OBC",
            "disability_status": "No"
        }
        create_res = self.client.post("/api/profile", json=payload)
        profile_id = create_res.json()["profile_id"]

        get_res = self.client.get(f"/api/profile/{profile_id}")
        self.assertEqual(get_res.status_code, 200)

        data = get_res.json()
        self.assertEqual(data["profile_id"], profile_id)
        self.assertEqual(data["name"], "Rohan Sharma")
        self.assertEqual(data["district"], "North Delhi")

    def test_05_get_profile_not_found(self):
        response = self.client.get("/api/profile/prof_nonexistent")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])

    def test_06_update_profile_success(self):
        payload = {
            "name": "Priya Verma",
            "age": 24,
            "gender": "Female",
            "state": "Madhya Pradesh",
            "district": "Bhopal",
            "income": 120000.0,
            "occupation": "Teacher",
            "category": "SC",
            "disability_status": "No"
        }
        create_res = self.client.post("/api/profile", json=payload)
        profile_id = create_res.json()["profile_id"]

        update_payload = {
            "income": 150000.0,
            "occupation": "Senior Teacher",
            "qualification": "M.Sc B.Ed"
        }
        update_res = self.client.put(f"/api/profile/{profile_id}", json=update_payload)
        self.assertEqual(update_res.status_code, 200)

        data = update_res.json()
        self.assertEqual(data["profile_id"], profile_id)
        self.assertEqual(data["income"], 150000.0)
        self.assertEqual(data["occupation"], "Senior Teacher")
        self.assertEqual(data["qualification"], "M.Sc B.Ed")
        self.assertEqual(data["name"], "Priya Verma")  # Unchanged field preserved

    def test_07_update_profile_not_found(self):
        update_payload = {"income": 300000.0}
        response = self.client.put("/api/profile/prof_nonexistent", json=update_payload)
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])

    def test_08_update_profile_validation_error_invalid_age(self):
        payload = {
            "name": "Test User",
            "age": 30,
            "gender": "Female",
            "state": "Rajasthan",
            "district": "Kota",
            "income": 200000.0,
            "occupation": "Engineer",
            "category": "General",
            "disability_status": "No"
        }
        create_res = self.client.post("/api/profile", json=payload)
        profile_id = create_res.json()["profile_id"]

        # Attempt to update with invalid negative age
        invalid_update = {"age": -1}
        response = self.client.put(f"/api/profile/{profile_id}", json=invalid_update)
        self.assertEqual(response.status_code, 422)

    def test_09_list_profiles_success(self):
        for i in range(3):
            self.client.post("/api/profile", json={
                "name": f"Citizen {i}",
                "age": 20 + i,
                "gender": "Female",
                "state": "Rajasthan",
                "district": "Jaipur",
                "income": 100000.0 * (i + 1),
                "occupation": "Worker",
                "category": "General",
                "disability_status": "No"
            })

        response = self.client.get("/api/profile?skip=0&limit=10")
        self.assertEqual(response.status_code, 200)
        profiles = response.json()
        self.assertGreaterEqual(len(profiles), 3)

    def test_10_mongodb_profile_entity_schema_and_indexes(self):
        """Verifies MongoDB entity definition, aliases, and indexing specifications."""
        entity = ProfileInDB(
            _id="670678e5f1a23b4c5d6e7f80",
            profile_id="prof_test1234",
            name="Nimisha Mangal",
            age=21,
            gender="Female",
            state="Rajasthan",
            district="Jaipur",
            income=250000.0,
            occupation="Student",
            category="General",
            disability_status="No",
            qualification="B.Tech Data Science",
            created_at="2026-10-09T18:00:00Z",
            updated_at="2026-10-09T18:00:00Z"
        )
        self.assertEqual(entity.id, "670678e5f1a23b4c5d6e7f80")
        self.assertEqual(entity.profile_id, "prof_test1234")

        # Check collection metadata
        self.assertEqual(PROFILES_COLLECTION, "profiles")
        self.assertIn("$jsonSchema", PROFILES_COLLECTION_VALIDATOR)
        self.assertIn("profile_id", PROFILES_COLLECTION_VALIDATOR["$jsonSchema"]["required"])

        # Check index specifications
        index_names = [idx["name"] for idx in PROFILES_INDEXES]
        self.assertIn("idx_profile_id_unique", index_names)
        self.assertIn("idx_profile_state", index_names)

        # Check environment configuration helpers
        self.assertTrue(len(get_mongodb_uri()) > 0)
        self.assertTrue(len(get_database_name()) > 0)

    def test_11_profile_service_with_mock_mongodb(self):
        """Verifies that ProfileService operates correctly with MongoDB collections."""
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        # Mock insert_one
        mock_insert_result = MagicMock()
        mock_insert_result.inserted_id = "mock_object_id_123"
        mock_collection.insert_one.return_value = mock_insert_result

        service = ProfileService(mongo_db=mock_db)
        self.assertEqual(service.backend_type, "mongodb")

        # Test creation with MongoDB
        create_payload = ProfileCreate(
            name="MongoDB User",
            age=25,
            gender="Male",
            state="Rajasthan",
            district="Ajmer",
            income=200000.0,
            occupation="Technician",
            category="OBC",
            disability_status="No"
        )
        created = service.create_profile(create_payload)
        self.assertTrue(mock_collection.insert_one.called)
        self.assertEqual(created.name, "MongoDB User")

        # Test retrieval with MongoDB
        mock_collection.find_one.return_value = {
            "_id": "mock_object_id_123",
            "profile_id": created.profile_id,
            "name": "MongoDB User",
            "age": 25,
            "gender": "Male",
            "state": "Rajasthan",
            "district": "Ajmer",
            "income": 200000.0,
            "occupation": "Technician",
            "category": "OBC",
            "disability_status": "No",
            "qualification": None,
            "created_at": created.created_at,
            "updated_at": created.updated_at
        }
        retrieved = service.get_profile(created.profile_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.profile_id, created.profile_id)


if __name__ == "__main__":
    unittest.main()
