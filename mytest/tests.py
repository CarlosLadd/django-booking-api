from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from api.models import Event
import uuid


class BookingAPITest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(name="Test Event", date=timezone.now(), total_tickets=10,
                                          available_tickets=10)
        self.user_email = "testuser@example.com"
        self.idempotency_key = str(uuid.uuid4())

    def test_create_event(self):
        response = self.client.post(reverse('event-list'), {
            "name": "New Event",
            "date": timezone.now().isoformat(),
            "total_tickets": 50,
            "available_tickets": 50
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "New Event")

    def test_list_events(self):
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)

    def test_create_booking(self):
        response = self.client.post(reverse('booking-book'), {
            "email": self.user_email,
            "event_id": self.event.id,
            "idempotency_key": self.idempotency_key
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Booking confirmed.")

    def test_duplicate_booking(self):
        data = {
            "email": self.user_email,
            "event_id": self.event.id,
            "idempotency_key": self.idempotency_key
        }

        response1 = self.client.post(reverse('booking-book'), data, content_type='application/json')
        response2 = self.client.post(reverse('booking-book'), data, content_type='application/json')

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.json()["message"], "Booking confirmed.")
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response2.json()["message"], "Duplicate booking attempt detected.")
