# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from .models import CustomUser, Machine, Booking, Feedback, Query


# ─── Custom Admin Forms ──────────────────────────────────
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone', 'name', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('phone', 'name', 'email')


# ─── Custom User Admin ───────────────────────────────────
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form    = CustomUserCreationForm
    form        = CustomUserChangeForm

    list_display  = ['phone', 'name', 'email', 'is_staff', 'is_active']
    list_filter   = ['is_staff', 'is_active']
    search_fields = ['phone', 'name', 'email']
    ordering      = ['-date_joined']

    # ── What shows on the EDIT user page ──
    fieldsets = (
        (None,            {'fields': ('phone', 'password')}),
        ('Personal Info', {'fields': ('name', 'email')}),
        ('Permissions',   {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        ('Dates',         {'fields': ('date_joined', 'last_login')}),
    )

    # ── What shows on the ADD user page ──
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':  ('phone', 'name', 'email',
                        'password1', 'password2',
                        'is_staff', 'is_active'),
        }),
    )

    readonly_fields = ['date_joined', 'last_login']


# ─── Machine Admin ───────────────────────────────────────
@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display  = ['name', 'capacity', 'hourly_rate', 'is_available']
    list_filter   = ['is_available']
    search_fields = ['name']
    list_editable = ['is_available', 'hourly_rate']


# ─── Booking Admin ───────────────────────────────────────
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ['machine', 'user', 'date', 'start_time', 'end_time', 'status']
    list_filter   = ['status', 'date', 'machine']
    search_fields = ['user__name', 'user__phone', 'machine__name']
    list_editable = ['status']
    date_hierarchy = 'date'


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
    search_fields = ['name', 'phone', 'subject']