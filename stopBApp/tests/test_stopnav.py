from django.test import TestCase, Client
from django.urls import reverse
from stopBApp.models import Location
import json

class StopNavTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('stopnearby')

    def test_get_navigation_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'navigation.html')

    def test_post_location_valid(self):
        data = {
            "latitude": 43.0389,
            "longitude": -87.9065
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(Location.objects.count(), 1)

        location = Location.objects.first()
        self.assertEqual(location.latitude, data["latitude"])
        self.assertEqual(location.longitude, data["longitude"])

    def test_post_location_invalid_json(self):
        response = self.client.post(
            self.url,
            data="not-json",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["status"], "error")




