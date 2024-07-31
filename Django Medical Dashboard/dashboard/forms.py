from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Appointment, Message, MedicalRecord
from users.models import User

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'treatment', 'notes']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time', 'reason']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['receiver', 'content']

class SurvivorLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')

class DoctorLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_doctor = forms.BooleanField(required=False, label='Register as a Doctor')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_doctor']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_doctor = self.cleaned_data['is_doctor']
        if commit:
            user.save()
        return user

class SurvivorLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class DoctorLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)