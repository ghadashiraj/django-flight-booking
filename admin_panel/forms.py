from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from base.models import FlightDetails_new, SeatReservation


class AdminRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150, required=True)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, strip=False)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput, strip=False)
    invite_code = forms.CharField(label="Admin invitation code", widget=forms.PasswordInput, strip=False)

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        User = get_user_model()
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        User = get_user_model()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get('password1')
        password2 = cleaned.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')
        if password1:
            User = get_user_model()
            candidate = User(
                username=cleaned.get('username', ''),
                email=cleaned.get('email', ''),
                first_name=cleaned.get('first_name', ''),
                last_name=cleaned.get('last_name', ''),
            )
            try:
                validate_password(password1, user=candidate)
            except ValidationError as exc:
                self.add_error('password1', exc)
        return cleaned


class FlightForm(forms.ModelForm):
    class Meta:
        model = FlightDetails_new
        fields = '__all__'


class SeatReservationForm(forms.ModelForm):
    class Meta:
        model = SeatReservation
        fields = ['pname', 'ano', 'phno', 'email', 'seat_number']
