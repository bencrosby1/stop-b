from django.test import TestCase, Client
from django.urls import reverse
import xml.etree.ElementTree as ET

class BusTimesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_bus_time_view_status_code(self):
        response = self.client.get(reverse('bus_times'))
        self.assertEqual(response.status_code, 200)

    def test_bus_times_view_valid(self):
        valid_stop_id = 1718
        response = self.client.get(reverse('bus_times', args={'stop_id': valid_stop_id}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, dict)

    def test_bus_times_view_invalid_stop(self):
        invalid_stop_id = -1
        response = self.client.get(reverse('bus_times', args={'stop_id': invalid_stop_id}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(isinstance(response.content, dict))

    def test_bus_times_view_coordinates_valid(self):
        stop_lat = 43.0166003
        stop_lon = -88.0382036
        response = self.client.get(reverse('bus_times', args={'lat': stop_lat, 'lon': stop_lon}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, dict)

    def test_bus_times_view_coordinates_invalid(self):
        stop_lat = 1234567890
        stop_lon = 1234567890
        response = self.client.get(reverse('bus_times', args={'lat': stop_lat, 'lon': stop_lon}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(isinstance(response.content, dict))