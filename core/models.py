# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils import timezone


# ════════════════════════════════════════════════
# CUSTOM USER MANAGER
# ════════════════════════════════════════════════
class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Phone number is required')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(phone, password, **extra_fields)


# ════════════════════════════════════════════════
# CUSTOM USER MODEL (Phone-based auth)
# ════════════════════════════════════════════════
class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone       = models.CharField(max_length=15, unique=True)
    name        = models.CharField(max_length=100)
    email       = models.EmailField(blank=True, null=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD  = 'phone'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.name} ({self.phone})"


# ════════════════════════════════════════════════
# MACHINE / EQUIPMENT
# ════════════════════════════════════════════════
class Machine(models.Model):
    name        = models.CharField(max_length=200)
    description = models.TextField()
    image       = models.ImageField(upload_to='machines/', blank=True, null=True)
    capacity    = models.CharField(max_length=100, help_text="e.g. 20 Ton, 5 CY")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ════════════════════════════════════════════════
# BOOKING
# ════════════════════════════════════════════════
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user        = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    machine     = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='bookings')
    date        = models.DateField()
    start_time  = models.TimeField()
    end_time    = models.TimeField()
    location    = models.CharField(max_length=300)
    notes       = models.TextField(blank=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-start_time']

    def clean(self):
        """Prevent double booking for the same machine on the same date/time slot."""
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("Start time must be before end time.")

            # Check for overlapping bookings
            overlapping = Booking.objects.filter(
                machine=self.machine,
                date=self.date,
                status__in=['pending', 'confirmed']
            ).exclude(pk=self.pk)

            for booking in overlapping:
                if not (self.end_time <= booking.start_time or
                        self.start_time >= booking.end_time):
                    raise ValidationError(
                        f"This machine is already booked from "
                        f"{booking.start_time.strftime('%I:%M %p')} to "
                        f"{booking.end_time.strftime('%I:%M %p')} on this date."
                    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.machine.name} | {self.date} | {self.user.name}"


# ════════════════════════════════════════════════
# FEEDBACK / REVIEW
# ════════════════════════════════════════════════
class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user      = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='feedbacks')
    booking   = models.OneToOneField(Booking, on_delete=models.CASCADE,
                                     related_name='feedback', null=True, blank=True)
    rating    = models.IntegerField(choices=RATING_CHOICES)
    comment   = models.TextField()
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.name} — {self.rating}★"


# ════════════════════════════════════════════════
# QUERY / SUPPORT TICKET
# ════════════════════════════════════════════════
class Query(models.Model):
    STATUS_CHOICES = [
        ('open',     'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed',   'Closed'),
    ]

    name       = models.CharField(max_length=100)
    phone      = models.CharField(max_length=15)
    email      = models.EmailField(blank=True)
    subject    = models.CharField(max_length=200)
    message    = models.TextField()
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    user       = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='queries')

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Queries'

    def __str__(self):
        return f"[{self.status.upper()}] {self.subject} — {self.name}"