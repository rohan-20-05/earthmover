# core/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Booking, Feedback, Query


# ─── Registration Form ───────────────────────────────────
class RegisterForm(forms.ModelForm):
    password  = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Create Password'
    }))
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm Password'
    }))

    class Meta:
        model  = CustomUser
        fields = ['name', 'phone', 'email']
        widgets = {
            'name':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (optional)'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


# ─── Login Form ──────────────────────────────────────────
class PhoneLoginForm(forms.Form):
    phone    = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Phone Number'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))


# ─── Booking Form ────────────────────────────────────────
class BookingForm(forms.ModelForm):
    class Meta:
        model  = Booking
        fields = ['machine', 'date', 'start_time', 'end_time', 'location', 'notes']
        widgets = {
            'machine':    forms.Select(attrs={'class': 'form-select'}),
            'date':       forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time':   forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'location':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Site Location'}),
            'notes':      forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                 'placeholder': 'Any special requirements?'}),
        }


# ─── Feedback Form ───────────────────────────────────────
class FeedbackForm(forms.ModelForm):
    class Meta:
        model  = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'rating':  forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                             'placeholder': 'Share your experience...'}),
        }


# ─── Query / Contact Form ────────────────────────────────
class QueryForm(forms.ModelForm):
    class Meta:
        model  = Query
        fields = ['name', 'phone', 'email', 'subject', 'message']
        widgets = {
            'name':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'phone':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email':   forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (optional)'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                             'placeholder': 'Describe your query...'}),
        }