from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user


# User Model
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    objects = UserManager()


# Event Model
class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.available_tickets = self.total_tickets
        super().save(*args, **kwargs)


# Booking Model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    idempotency_key = models.UUIDField(default=uuid.uuid4, unique=True)

    class Meta:
        unique_together = ('user', 'event')
