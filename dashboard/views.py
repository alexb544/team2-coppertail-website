from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from services.models import Service
from booking.models import TimeSlot, Booking
from .forms import ServiceForm, TimeSlotForm

def is_admin(user):
    return user.is_staff or user.is_superuser

def admin_required(view_func):
    decorated = login_required(login_url='accounts:login')(
        user_passes_test(is_admin, login_url='accounts:login')(view_func)
    )
    return decorated

@admin_required
def dashboard(request):
    services = Service.objects.all()
    timeslots = TimeSlot.objects.all().order_by('start_time')
    recent_bookings = Booking.objects.select_related('user', 'dog', 'slot') \
                                     .order_by('-created_at')[:10]
    return render(request, 'dashboard/dashboard.html', {
        'services': services,
        'timeslots': timeslots,
        'recent_bookings': recent_bookings,
    })

# --- Services ---

@admin_required
def add_service(request):
    form = ServiceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Service added successfully!')
        return redirect('dashboard:dashboard')
    return render(request, 'dashboard/service_form.html', {
        'form': form,
        'form_title': 'Add Service',
        'submit_label': 'Add Service',
    })

@admin_required
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None, instance=service)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Service updated!')
        return redirect('dashboard:dashboard')
    return render(request, 'dashboard/service_form.html', {
        'form': form,
        'form_title': f'Edit — {service.service_name}',
        'submit_label': 'Save Changes',
    })

@admin_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, f'"{service.service_name}" deleted.')
    return redirect('dashboard:dashboard')

# --- Time Slots ---

@admin_required
def add_timeslot(request):
    form = TimeSlotForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Time slot added!')
        return redirect('dashboard:dashboard')
    return render(request, 'dashboard/timeslot_form.html', {
        'form': form,
        'form_title': 'Add Time Slot',
        'submit_label': 'Add Slot',
    })

@admin_required
def edit_timeslot(request, pk):
    slot = get_object_or_404(TimeSlot, pk=pk)
    form = TimeSlotForm(request.POST or None, instance=slot)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Time slot updated!')
        return redirect('dashboard:dashboard')
    return render(request, 'dashboard/timeslot_form.html', {
        'form': form,
        'form_title': f'Edit Slot — {slot.start_time.strftime("%b %d, %Y %H:%M")}',
        'submit_label': 'Save Changes',
    })

@admin_required
def delete_timeslot(request, pk):
    slot = get_object_or_404(TimeSlot, pk=pk)
    if request.method == 'POST':
        slot.delete()
        messages.success(request, 'Time slot deleted.')
    return redirect('dashboard:dashboard')

@admin_required
def toggle_timeslot(request, pk):
    slot = get_object_or_404(TimeSlot, pk=pk)
    if request.method == 'POST':
        slot.is_open = not slot.is_open
        slot.save()
        state = 'opened' if slot.is_open else 'closed'
        messages.success(request, f'Slot {state}.')
    return redirect('dashboard:dashboard')
