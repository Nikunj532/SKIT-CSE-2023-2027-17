import unittest
from pathlib import Path
from fastapi.testclient import TestClient

from backend.main import app
from backend.services.scheme_service import (
    load_schemes,
    search_schemes,
    get_scheme_by_id,
    get_all_schemes,
)


class TestSchemeSearchAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_search_schemes_default_returns_all(self):
        """GET /api/schemes/search without filters returns paginated scheme list."""
        response = self.client.get("/api/schemes/search")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("total", data)
        self.assertIn("page", data)
        self.assertIn("limit", data)
        self.assertIn("total_pages", data)
        self.assertIn("schemes", data)
        self.assertEqual(data["page"], 1)
        self.assertGreater(data["total"], 0)
        self.assertGreater(len(data["schemes"]), 0)

    def test_02_search_schemes_keyword_query(self):
        """GET /api/schemes/search?q=kisan searches in name and description."""
        response = self.client.get("/api/schemes/search?q=kisan")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertGreaterEqual(data["total"], 1)
        names = [s["name"] for s in data["schemes"]]
        self.assertTrue(any("Kisan" in name for name in names))

    def test_03_search_schemes_category_filter(self):
        """GET /api/schemes/search?category=Health filters by category."""
        response = self.client.get("/api/schemes/search?category=Health")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertGreaterEqual(data["total"], 1)
        for scheme in data["schemes"]:
            self.assertEqual(scheme["category"].lower(), "health")

    def test_04_search_schemes_state_filter(self):
        """GET /api/schemes/search?state=Rajasthan returns Rajasthan & Central schemes."""
        response = self.client.get("/api/schemes/search?state=Rajasthan")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertGreaterEqual(data["total"], 1)
        for scheme in data["schemes"]:
            self.assertIn(
                scheme["state"].lower(),
                ("rajasthan", "central", "all", "all india", "national")
            )

    def test_05_search_schemes_combined_filters(self):
        """GET /api/schemes/search with combined keyword, category, and state."""
        response = self.client.get("/api/schemes/search?q=scholarship&category=Education&state=Rajasthan")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertGreaterEqual(data["total"], 1)
        scheme = data["schemes"][0]
        self.assertIn("Scholarship", scheme["name"])
        self.assertEqual(scheme["category"], "Education")

    def test_06_search_schemes_no_results(self):
        """GET /api/schemes/search with unmatched query returns total=0 and empty list."""
        response = self.client.get("/api/schemes/search?q=completely_nonexistent_xyz_query")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["total"], 0)
        self.assertEqual(data["total_pages"], 0)
        self.assertEqual(data["schemes"], [])

    def test_07_search_schemes_pagination(self):
        """GET /api/schemes/search pagination parameters correctly slice results."""
        # Page 1 with limit 2
        res_p1 = self.client.get("/api/schemes/search?page=1&limit=2")
        self.assertEqual(res_p1.status_code, 200)
        data_p1 = res_p1.json()
        self.assertEqual(data_p1["page"], 1)
        self.assertEqual(data_p1["limit"], 2)
        self.assertEqual(len(data_p1["schemes"]), 2)

        # Page 2 with limit 2
        res_p2 = self.client.get("/api/schemes/search?page=2&limit=2")
        self.assertEqual(res_p2.status_code, 200)
        data_p2 = res_p2.json()
        self.assertEqual(data_p2["page"], 2)
        self.assertEqual(len(data_p2["schemes"]), 2)

        # Confirm distinct schemes between pages
        ids_p1 = [s["scheme_id"] for s in data_p1["schemes"]]
        ids_p2 = [s["scheme_id"] for s in data_p2["schemes"]]
        self.assertEqual(len(set(ids_p1).intersection(set(ids_p2))), 0)

    def test_08_search_schemes_validation_error(self):
        """Query validation errors: page < 1 and limit > 100 return 422."""
        # Invalid page=0
        res_invalid_page = self.client.get("/api/schemes/search?page=0")
        self.assertEqual(res_invalid_page.status_code, 422)

        # Invalid limit=150 (> 100)
        res_invalid_limit = self.client.get("/api/schemes/search?limit=150")
        self.assertEqual(res_invalid_limit.status_code, 422)

    def test_09_get_scheme_by_id_success(self):
        """GET /api/schemes/{scheme_id} returns the specific scheme."""
        response = self.client.get("/api/schemes/sch_pm_kisan")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["scheme_id"], "sch_pm_kisan")
        self.assertIn("Pradhan Mantri", data["name"])
        self.assertEqual(data["category"], "Agriculture")
        self.assertIsInstance(data["benefits"], list)
        self.assertIsInstance(data["eligibility"], list)

    def test_10_get_scheme_by_id_not_found(self):
        """GET /api/schemes/{scheme_id} returns 404 for unknown scheme."""
        response = self.client.get("/api/schemes/sch_nonexistent_999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])

    def test_11_get_all_schemes_backward_compatibility(self):
        """GET /api/schemes returns raw list of all schemes for backward compatibility."""
        response = self.client.get("/api/schemes")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_12_missing_dataset_graceful_handling(self):
        """Direct service test when dataset path does not exist."""
        nonexistent = Path("data/nonexistent_file_xyz.json")
        schemes = load_schemes(data_path=nonexistent)
        self.assertEqual(schemes, [])

        res = search_schemes(q="test", data_path=nonexistent)
        self.assertEqual(res.total, 0)
        self.assertEqual(res.schemes, [])

        scheme = get_scheme_by_id("sch_pm_kisan", data_path=nonexistent)
        self.assertIsNone(scheme)


if __name__ == "__main__":
    unittest.main()
