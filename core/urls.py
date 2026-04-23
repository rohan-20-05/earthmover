# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # ── Home ──────────────────────────────────
    path('',              views.home,          name='home'),

    # ── Auth ──────────────────────────────────
    path('register/',     views.register_view, name='register'),
    path('login/',        views.login_view,    name='login'),
    path('logout/',       views.logout_view,   name='logout'),

    # ── Booking ───────────────────────────────
    path('book/',         views.booking_view,  name='booking'),
    path('my-bookings/',  views.my_bookings,   name='my_bookings'),
    path('cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),

    # ── API ───────────────────────────────────
    path('api/booked-slots/', views.booked_slots_api, name='booked_slots_api'),

    # ── Feedback ──────────────────────────────
    path('feedback/',     views.feedback_view, name='feedback'),

    # ── Contact ───────────────────────────────
    path('contact/',      views.contact_view,  name='contact'),

    path('setup-admin/',      views.create_super,  name='create_super'),
]