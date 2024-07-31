from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Appointment, Message, MedicalRecord, Notification
from users.models import User
from .forms import AppointmentForm, MessageForm, MedicalRecordForm, SurvivorLoginForm, DoctorLoginForm, RegistrationForm
from django.contrib.auth import login

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'dashboard/home.html')

def survivor_login(request):
    if request.method == 'POST':
        form = SurvivorLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('survivor_dashboard')
    else:
        form = SurvivorLoginForm()
    return render(request, 'login.html', {'form': form, 'user_type': 'Survivor'})

def doctor_login(request):
    if request.method == 'POST':
        form = DoctorLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_doctor:
                login(request, user)
                return redirect('doctor_dashboard')
            else:
                form.add_error(None, "This account is not registered as a doctor.")
    else:
        form = DoctorLoginForm()
    return render(request, 'login.html', {'form': form, 'user_type': 'Doctor'})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_doctor:
                return redirect('doctor_dashboard')
            else:
                return redirect('survivor_dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

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

@login_required
def doctor_dashboard(request):
    try:
        appointments = Appointment.objects.filter(doctor=request.user).order_by('date_time')
    except:
        appointments = []
    return render(request, 'dashboard/doctor_dashboard.html', {'appointments': appointments})

@login_required
def view_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if appointment.patient != request.user and appointment.doctor != request.user:
        return redirect('dashboard')
    return render(request, 'dashboard/view_appointment.html', {'appointment': appointment})

@login_required
def messages(request):
    user_messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-timestamp')
    paginator = Paginator(user_messages, 10)  # Show 10 messages per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/messages.html', {'page_obj': page_obj})

@login_required
def medical_records(request):
    records = MedicalRecord.objects.filter(patient=request.user).order_by('-date')
    return render(request, 'dashboard/medical_records.html', {'records': records})

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/notifications.html', {'notifications': notifications})

def is_doctor(user):
    return user.is_authenticated and user.is_doctor

@login_required
def search_patients(request):
    query = request.GET.get('q')
    search_performed = False
    patients = []

    if query:
        search_performed = True
        patients = User.objects.filter(
            Q(is_patient=True) &
            (Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query))
        )

    return render(request, 'dashboard/search_patients.html', {
        'patients': patients,
        'search_performed': search_performed
    })

def doctor_register(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}. You can now log in.')
            return redirect('login')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = request.user
            appointment.save()
            messages.success(request, 'Appointment scheduled successfully.')
            return redirect('dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'dashboard/create_appointment.html', {'form': form})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment cancelled successfully.')
        return redirect('dashboard')
    return render(request, 'dashboard/cancel_appointment.html', {'appointment': appointment})

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
    else:
        form = MessageForm()
    return render(request, 'dashboard/send_message.html', {'form': form})

@login_required
def view_messages(request):
    messages_list = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    paginator = Paginator(messages_list, 10)  # Show 10 messages per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/view_messages.html', {'page_obj': page_obj})

@login_required
def medical_records(request):
    records = MedicalRecord.objects.filter(patient=request.user).order_by('-date')
    return render(request, 'dashboard/medical_records.html', {'records': records})

@login_required
def view_medical_records(request):
    if hasattr(request.user, 'is_doctor') and request.user.is_doctor:
        records = MedicalRecord.objects.filter(doctor=request.user).order_by('-date')
    else:
        records = MedicalRecord.objects.filter(patient=request.user).order_by('-date')

    paginator = Paginator(records, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/view_medical_records.html', {'page_obj': page_obj})


@login_required
def create_medical_record(request, patient_id):
    if not request.user.is_doctor:
        messages.error(request, "You don't have permission to create medical records.")
        return redirect('dashboard')

    patient = get_object_or_404(User, id=patient_id, is_patient=True)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = patient
            medical_record.doctor = request.user
            medical_record.save()
            messages.success(request, "Medical record created successfully.")
            return redirect('view_medical_records')
    else:
        form = MedicalRecordForm()

    return render(request, 'dashboard/create_medical_record.html', {'form': form, 'patient': patient})

@login_required
def view_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/view_notifications.html', {'notifications': notifications})


def survivor_login(request):
    if request.method == 'POST':
        form = SurvivorLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = SurvivorLoginForm()
    return render(request, 'dashboard/login.html', {'form': form, 'user_type': 'Survivor'})

def doctor_login(request):
    if request.method == 'POST':
        form = DoctorLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None and user.is_doctor:
                login(request, user)
                return redirect('dashboard')
    else:
        form = DoctorLoginForm()
    return render(request, 'dashboard/login.html', {'form': form, 'user_type': 'Doctor'})
    
