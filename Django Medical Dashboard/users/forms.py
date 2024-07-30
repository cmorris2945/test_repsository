from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, PatientProfile, DoctorProfile

class PatientSignUpForm(UserCreationForm):
    date_of_birth = forms.DateField(required=False)
    medical_history = forms.CharField(widget=forms.Textarea, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.save()
        PatientProfile.objects.create(
            user=user,
            date_of_birth=self.cleaned_data.get('date_of_birth'),
            medical_history=self.cleaned_data.get('medical_history')
        )
        return user

class DoctorSignUpForm(UserCreationForm):
    specialty = forms.CharField(max_length=100, required=True)
    license_number = forms.CharField(max_length=50, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'specialty', 'license_number', 'password1', 'password2')

    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        user.save()
        DoctorProfile.objects.create(
            user=user,
            specialty=self.cleaned_data.get('specialty'),
            license_number=self.cleaned_data.get('license_number')
        )
        return user

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# You can keep the DoctorRegistrationForm if you need it for a different purpose
class DoctorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    specialty = forms.CharField(max_length=100, required=True)
    license_number = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'specialty', 'license_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_doctor = True
        if commit:
            user.save()
            DoctorProfile.objects.create(
                user=user,
                specialty=self.cleaned_data['specialty'],
                license_number=self.cleaned_data['license_number']
            )
        return user