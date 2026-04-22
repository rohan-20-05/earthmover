# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Machine, Booking, Feedback, Query


# ─── Custom User Admin ───────────────────────────────────
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display  = ['phone', 'name', 'email', 'is_staff', 'is_active', 'date_joined']
    list_filter   = ['is_staff', 'is_active']
    search_fields = ['phone', 'name', 'email']
    ordering      = ['-date_joined']

    fieldsets = (
        (None,           {'fields': ('phone', 'password')}),
        ('Personal Info', {'fields': ('name', 'email')}),
        ('Permissions',  {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates',        {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':  ('phone', 'name', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


# ─── Machine Admin ───────────────────────────────────────
@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display  = ['name', 'capacity', 'hourly_rate', 'is_available', 'created_at']
    list_filter   = ['is_available']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'hourly_rate']


# ─── Booking Admin ───────────────────────────────────────
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ['machine', 'user', 'date', 'start_time', 'end_time', 'status', 'created_at']
    list_filter   = ['status', 'date', 'machine']
    search_fields = ['user__name', 'user__phone', 'machine__name', 'location']
    list_editable = ['status']
    date_hierarchy = 'date'
    raw_id_fields = ['user', 'machine']


# ─── Feedback Admin ──────────────────────────────────────
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display  = ['user', 'rating', 'is_public', 'created_at']
    list_filter   = ['rating', 'is_public']
    list_editable = ['is_public']
    search_fields = ['user__name', 'comment']


# ─── Query Admin ─────────────────────────────────────────
@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display  = ['subject', 'name', 'phone', 'status', 'created_at']
    list_filter   = ['status']
    list_editable = ['status']
    search_fields = ['name', 'phone', 'subject', 'message']
    date_hierarchy = 'created_at'