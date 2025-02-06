
# django-booking-api

Booking API code challenge




## Run Locally

Clone the project

```bash
  git clone https://github.com/CarlosLadd/django-booking-api.git
```

Go to the project directory

```bash
  cd django-booking-api
```

Create a Virtualenv

```bash
  python3 -m venv venv
  source venv/bin/activate
```

Install dependencies

```bash
  cd mytest
  pip3 install -r requirements.txt
```

Docker

```bash
  cd mytest
  docker-compose up --build
```

Run unit tests

```bash
  python3 manage.py test
```

Create an Event
```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Test Event",
           "date": "2025-02-10T18:00:00Z",
           "total_tickets": 100,
           "available_tickets": 100
         }'
```

Booking
```bash
curl -X POST http://127.0.0.1:8000/api/bookings/book/ \
     -H "Content-Type: application/json" \
     -d '{
          "email": "testuser@example.com",
          "event_id": 1,
          "idempotency_key": "123e4567-e89b-12d3-a456-426614174000"
         }'
```