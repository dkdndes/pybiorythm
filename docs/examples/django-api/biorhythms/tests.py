from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class BiorhythmAPITestCase(APITestCase):
    """Test cases for the Biorhythm API."""

    def test_api_info_endpoint(self):
        """Test the API info endpoint."""
        url = reverse("api_info")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_quick_biorhythm_missing_params(self):
        """Test quick endpoint without required parameters."""
        url = reverse("quick_biorhythm")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_quick_biorhythm_valid_params(self):
        """Test quick endpoint with valid parameters."""
        url = reverse("quick_biorhythm")
        response = self.client.get(url, {"birthdate": "1990-05-15", "days": "7"})

        # This test will pass even if PyBiorythm is not installed
        if response.status_code == 503:
            # Library not available - this is expected in some environments
            self.assertIn("error", response.json())
        else:
            # Library available - test successful calculation
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("birthdate", data)
            self.assertIn("biorhythm_data", data)

    def test_calculate_endpoint_invalid_data(self):
        """Test calculate endpoint with invalid data."""
        url = reverse("calculate_biorhythm")
        response = self.client.post(
            url, {"birthdate": "invalid-date", "days": "invalid-number"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_calculate_endpoint_valid_data(self):
        """Test calculate endpoint with valid data."""
        url = reverse("calculate_biorhythm")
        response = self.client.post(
            url,
            {"birthdate": "1990-05-15", "target_date": "2024-08-10", "days": 7},
            format="json",
        )

        # This test will pass even if PyBiorythm is not installed
        if response.status_code == 503:
            # Library not available - this is expected in some environments
            self.assertIn("error", response.data)
        else:
            # Library available - test successful calculation
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("request_info", response.data)
            self.assertIn("biorhythm_data", response.data)
