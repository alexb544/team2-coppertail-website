from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from services.models import Service
from booking.models import TimeSlot, Booking
from .forms import ServiceForm, TimeSlotForm, BookingForm

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
    service_price_min = request.GET.get('service_price_min')
    service_price_max = request.GET.get('service_price_max')
    service_sort = request.GET.get('service_sort', 'service_name')
    if service_price_min:
        services = services.filter(base_price__gte=service_price_min)
    if service_price_max:
        services = services.filter(base_price__lte=service_price_max)
    valid_service_sorts = ['service_name', '-service_name', 'base_price', '-base_price']
    if service_sort in valid_service_sorts:
        services = services.order_by(service_sort)
    timeslots = TimeSlot.objects.all()
    slot_status = request.GET.get('slot_status', '')
    slot_sort = request.GET.get('slot_sort', 'start_time')
    if slot_status == 'open':
        timeslots = timeslots.filter(is_open=True)
    elif slot_status == 'closed':
        timeslots = timeslots.filter(is_open=False)
    valid_slot_sorts = ['start_time', '-start_time', 'end_time', '-end_time']
    if slot_sort in valid_slot_sorts:
        timeslots = timeslots.order_by(slot_sort)
    bookings = Booking.objects.select_related('user', 'dog', 'slot')
    booking_customer = request.GET.get('booking_customer', '').strip()
    booking_status = request.GET.get('booking_status', '')
    booking_sort = request.GET.get('booking_sort', 'created_at')
    if booking_customer:
        bookings = bookings.filter(user__username__icontains=booking_customer)
    if booking_status:
        bookings = bookings.filter(status=booking_status)
    valid_booking_sorts = ['user__username', '-user__username', 'total', '-total', 'created_at', '-created_at', 'slot__start_time', '-slot__start_time']
    if booking_sort in valid_booking_sorts:
        bookings = bookings.order_by(booking_sort)
    return render(request, 'dashboard/dashboard.html', {
        'services': services,
        'timeslots': timeslots,
        'recent_bookings': bookings,
        # pass filter values back so form fields stay filled
        'service_price_min': service_price_min or '',
        'service_price_max': service_price_max or '',
        'service_sort': service_sort,
        'slot_status': slot_status,
        'slot_sort': slot_sort,
        'booking_customer': booking_customer,
        'booking_status': booking_status,
        'booking_sort': booking_sort,
    })

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
        'form_title': f'Edit - {service.service_name}',
        'submit_label': 'Save Changes',
    })

@admin_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, f'"{service.service_name}" deleted.')
    return redirect('dashboard:dashboard')

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

@admin_required
def edit_booking(request, pk):
    booking = get_object_or_404(
        Booking.objects.select_related('user', 'dog', 'slot'), pk=pk
    )
    form = BookingForm(request.POST or None, instance=booking)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Booking #{booking.pk} updated!')
        return redirect('dashboard:dashboard')
    return render(request, 'dashboard/booking_form.html', {
        'form': form,
        'booking': booking,
        'form_title': f'Edit Booking #{booking.pk}',
        'submit_label': 'Save Changes',
    })

@admin_required
def delete_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, f'Booking #{pk} deleted.')
    return redirect('dashboard:dashboard')

@admin_required
def update_booking_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in Booking.Status.values:
            booking.status = new_status
            booking.save()
            messages.success(request, f'Booking #{pk} marked as {new_status}.')
    return redirect('dashboard:dashboard')