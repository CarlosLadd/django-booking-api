from django.core.cache import cache
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from .models import Event, Booking, User
from .serializers import EventSerializer, BookingSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        date = self.request.query_params.get('date')
        if name:
            queryset = queryset.filter(name__icontains=name)
        if date:
            queryset = queryset.filter(date=date)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class BookingViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @transaction.atomic
    @action(detail=False, methods=['post'])
    def book(self, request):
        user_email = request.data.get('email')
        event_id = request.data.get('event_id')
        idempotency_key = request.data.get('idempotency_key')

        if cache.get(idempotency_key):
            return Response({"message": "Duplicate booking attempt detected."}, status=400)

        cache.set(idempotency_key, True, timeout=60)

        user, _ = User.objects.get_or_create(email=user_email)
        event = Event.objects.select_for_update().get(id=event_id)

        if event.available_tickets <= 0:
            return Response({"message": "No tickets available."}, status=400)

        event.available_tickets -= 1
        event.save()
        Booking.objects.create(user=user, event=event, idempotency_key=idempotency_key)

        return Response({"message": "Booking confirmed."})
