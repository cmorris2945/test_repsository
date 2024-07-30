from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Appointment, Message, MedicalRecord, Notification
from users.models import User
from .forms import AppointmentForm, MessageForm, MedicalRecordForm

def register(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'dashboard/home.html')

@login_required
def dashboard(request):
    if request.user.is_patient:
        return patient_dashboard(request)
    elif request.user.is_doctor:
        return doctor_dashboard(request)
    else:
        return redirect('home')

@login_required
def patient_dashboard(request):
    appointments = Appointment.objects.filter(patient=request.user).order_by('date_time')
    medical_records = MedicalRecord.objects.filter(patient=request.user).order_by('-date')
    recent_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')[:5]

    context = {
        'appointments': appointments,
        'medical_records': medical_records,
        'recent_messages': recent_messages,
        'appointment_form': AppointmentForm(),
    }
    return render(request, 'dashboard/patient_dashboard.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Appointment, Message

@login_required
def doctor_dashboard(request):
    try:
        appointments = Appointment.objects.filter(doctor=request.user).order_by('date_time')
    except:
        appointments = []

    try:
        recent_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')[:5]
    except:
        recent_messages = []

    context = {
        'appointments': appointments,
        'recent_messages': recent_messages,
    }
    return render(request, 'dashboard/doctor_dashboard.html', context)

@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, 'Appointment created successfully.')
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'dashboard/create_appointment.html', {'form': form})
    
@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('dashboard')
    return redirect('dashboard')

@login_required
def view_medical_records(request):
    if request.user.is_patient:
        medical_records = MedicalRecord.objects.filter(patient=request.user).order_by('-date')
    elif request.user.is_doctor:
        medical_records = MedicalRecord.objects.filter(doctor=request.user).order_by('-date')
    else:
        return redirect('home')

    context = {
        'medical_records': medical_records,
    }
    return render(request, 'dashboard/medical_records.html', context)

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment cancelled successfully.')
        return redirect('dashboard')
    return render(request, 'dashboard/cancel_appointment.html', {'appointment': appointment})

@login_required
def view_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    received_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    context = {
        'sent_messages': sent_messages,
        'received_messages': received_messages,
    }
    return render(request, 'dashboard/view_messages.html', context)

@login_required
def create_medical_record(request, patient_id):
    if not request.user.is_doctor:
        messages.error(request, "You don't have permission to create medical records.")
        return redirect('dashboard')

    patient = get_object_or_404(User, id=patient_id, is_patient=True)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.doctor = request.user
            record.save()
            messages.success(request, "Medical record created successfully.")
            return redirect('view_medical_records')
    else:
        form = MedicalRecordForm()

    return render(request, 'dashboard/create_medical_record.html', {'form': form, 'patient': patient})

@login_required
def view_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/notifications.html', {'notifications': notifications})

def is_doctor(user):
    return user.is_authenticated and user.is_doctor

@user_passes_test(is_doctor)
def search_patients(request):
    query = request.GET.get('q')
    if query:
        patients = User.objects.filter(
            Q(is_patient=True) &
            (Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
        )
    else:
        patients = User.objects.filter(is_patient=True)

    return render(request, 'dashboard/search_patients.html', {'patients': patients, 'query': query})

def doctor_register(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Here you might want to create a Doctor profile associated with this user
            # For example: Doctor.objects.create(user=user, specialty=form.cleaned_data['specialty'], license_number=form.cleaned_data['license_number'])
            messages.success(request, f'Account created for {user.username}. You can now log in.')
            return redirect('login')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'register.html', {'form': form})