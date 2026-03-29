import json
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helper


class TestHelperFilePaths(unittest.TestCase):
    def test_get_skills_file(self):
        self.assertEqual(helper.get_skills_file(), "data/skills.json")

    def test_get_organizations_file(self):
        self.assertEqual(helper.get_organizations_file(), "data/organizations.json")

    def test_get_search_terms_file(self):
        self.assertEqual(helper.get_search_terms_file(), "data/search-terms.json")

    def test_get_badges_file(self):
        result = helper.get_badges_file("abc123")
        self.assertEqual(result, "data/badges/abc123.json")

    def test_get_badges_file_different_id(self):
        result = helper.get_badges_file("org-456")
        self.assertEqual(result, "data/badges/org-456.json")


class TestHelperFileOperations(unittest.TestCase):
    def test_get_items_from_file_missing(self):
        result = helper.get_items_from_file("/nonexistent/path/file.json")
        self.assertEqual(result, {})

    def test_get_items_from_file_existing(self):
        data = {"key": "value", "count": 42}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            tmp_path = f.name
        try:
            result = helper.get_items_from_file(tmp_path)
            self.assertEqual(result, data)
        finally:
            os.unlink(tmp_path)

    def test_set_items_from_file(self):
        data = {"org1": {"name": "Test Org"}, "org2": {"name": "Another Org"}}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            tmp_path = f.name
        try:
            helper.set_items_from_file(tmp_path, data)
            with open(tmp_path, "r") as f:
                result = json.load(f)
            self.assertEqual(result, data)
        finally:
            os.unlink(tmp_path)

    def test_roundtrip_file_operations(self):
        original = {"a": 1, "b": [1, 2, 3]}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            tmp_path = f.name
        try:
            helper.set_items_from_file(tmp_path, original)
            result = helper.get_items_from_file(tmp_path)
            self.assertEqual(result, original)
        finally:
            os.unlink(tmp_path)


class TestCrawlSearchTerms(unittest.TestCase):
    def test_crawl_search_terms_organization(self):
        items = [
            {
                "type": "Organization",
                "id": "org1",
                "name": "Test Org",
                "photo": {"url": "http://example.com/logo.png"},
                "url": "/orgs/test-org",
            }
        ]
        with (
            patch("helper.get_items_by_search_term", return_value=items),
            patch("helper.get_items_from_file", return_value={}),
            patch("helper.set_items_from_file") as mock_set,
        ):
            helper.crawl_search_terms(["test"])
            self.assertTrue(mock_set.called)

    def test_crawl_search_terms_skill(self):
        items = [
            {
                "type": "Skill",
                "id": "skill1",
                "name": "Python",
            }
        ]
        with (
            patch("helper.get_items_by_search_term", return_value=items),
            patch("helper.get_items_from_file", return_value={}),
            patch("helper.set_items_from_file") as mock_set,
        ):
            helper.crawl_search_terms(["python"])
            self.assertTrue(mock_set.called)


class TestGetBadges(unittest.TestCase):
    def test_get_badges_single_page(self):
        mock_response = {
            "data": [{"id": "badge1", "name": "Badge One"}],
            "metadata": {"next_page_url": None},
        }
        mock_get = MagicMock()
        mock_get.return_value.json.return_value = mock_response
        with patch("requests.get", mock_get):
            result = helper.get_badges({}, "http://example.com/badges.json")
        self.assertIn("badge1", result)
        self.assertEqual(result["badge1"]["name"], "Badge One")

    def test_get_badges_multiple_pages(self):
        responses = [
            {
                "data": [{"id": "badge1", "name": "Badge One"}],
                "metadata": {"next_page_url": "http://example.com/badges.json?page=2"},
            },
            {
                "data": [{"id": "badge2", "name": "Badge Two"}],
                "metadata": {"next_page_url": None},
            },
        ]
        call_count = [0]

        def mock_get(url):
            resp = MagicMock()
            resp.json.return_value = responses[call_count[0]]
            call_count[0] += 1
            return resp

        with patch("requests.get", mock_get):
            result = helper.get_badges({}, "http://example.com/badges.json")
        self.assertIn("badge1", result)
        self.assertIn("badge2", result)

    def test_get_badges_handles_error(self):
        mock_get = MagicMock(side_effect=Exception("Network error"))
        with patch("requests.get", mock_get):
            result = helper.get_badges({}, "http://example.com/badges.json")
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
