# core/views.py

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Machine, Booking, Feedback, Query
from .forms import RegisterForm, PhoneLoginForm, BookingForm, FeedbackForm, QueryForm


# ════════════════════════════════════════════════
# HOME / LANDING PAGE
# ════════════════════════════════════════════════
def home(request):
    machines  = Machine.objects.filter(is_available=True)
    feedbacks = Feedback.objects.filter(is_public=True).select_related('user')[:6]
    context = {
        'machines':  machines,
        'feedbacks': feedbacks,
    }
    return render(request, 'core/home.html', context)


# ════════════════════════════════════════════════
# AUTHENTICATION VIEWS
# ════════════════════════════════════════════════
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Welcome, {user.name}! Your account has been created.")
        return redirect('home')

    return render(request, 'core/auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = PhoneLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        phone    = form.cleaned_data['phone']
        password = form.cleaned_data['password']
        user     = authenticate(request, username=phone, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.name}!")
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, "Invalid phone number or password.")

    return render(request, 'core/auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You've been logged out.")
    return redirect('home')


# ════════════════════════════════════════════════
# BOOKING VIEWS
# ════════════════════════════════════════════════
@login_required
def booking_view(request):
    form = BookingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        try:
            booking.save()
            messages.success(request, "✅ Booking confirmed! We'll contact you shortly.")
            return redirect('my_bookings')
        except Exception as e:
            messages.error(request, str(e))

    machines = Machine.objects.filter(is_available=True)
    return render(request, 'core/booking.html', {'form': form, 'machines': machines})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('machine')
    return render(request, 'core/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, "Booking cancelled.")
    return redirect('my_bookings')


# ─── API: Booked slots for FullCalendar ──────────────────
def booked_slots_api(request):
    """Returns all bookings as JSON for FullCalendar display."""
    machine_id = request.GET.get('machine_id')
    bookings = Booking.objects.filter(status__in=['pending', 'confirmed'])

    if machine_id:
        bookings = bookings.filter(machine_id=machine_id)

    events = []
    for b in bookings.select_related('machine', 'user'):
        events.append({
            'id':    b.pk,
            'title': f"{b.machine.name} — BOOKED",
            'start': f"{b.date}T{b.start_time}",
            'end':   f"{b.date}T{b.end_time}",
            'color': '#e74c3c',
            'extendedProps': {
                'machine': b.machine.name,
                'status':  b.status,
            }
        })

    return JsonResponse(events, safe=False)


# ════════════════════════════════════════════════
# FEEDBACK VIEW
# ════════════════════════════════════════════════
@login_required
def feedback_view(request):
    form = FeedbackForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        feedback = form.save(commit=False)
        feedback.user = request.user
        feedback.save()
        messages.success(request, "Thank you for your feedback!")
        return redirect('home')

    feedbacks = Feedback.objects.filter(is_public=True).select_related('user')
    return render(request, 'core/feedback.html', {'form': form, 'feedbacks': feedbacks})


# ════════════════════════════════════════════════
# QUERY / CONTACT VIEW
# ════════════════════════════════════════════════
def contact_view(request):
    form = QueryForm(request.POST or None)

    # Pre-fill if user is logged in
    if request.user.is_authenticated and not request.POST:
        form = QueryForm(initial={
            'name':  request.user.name,
            'phone': request.user.phone,
            'email': request.user.email or '',
        })

    if request.method == 'POST' and form.is_valid():
        query = form.save(commit=False)
        if request.user.is_authenticated:
            query.user = request.user
        query.save()
        messages.success(request, "✅ Your query has been submitted. We'll respond within 24 hours.")
        return redirect('contact')

    return render(request, 'core/contact.html', {'form': form})