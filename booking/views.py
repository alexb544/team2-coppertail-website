from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingCreateForm
from .models import Booking, TimeSlot, BookingService
from .pricing import estimate_total
from services.models import Service
from accounts.models import Dog

@login_required
def booking_create(request):
    if request.method == "POST":
        form = BookingCreateForm(request.POST, user=request.user)
        if form.is_valid():
            slot = form.cleaned_data["slot"]
            dog = form.cleaned_data["dog"]
            services = form.cleaned_data["services"]

            subtotal, total = estimate_total(dog, services)

            request.session["booking_draft"] = {
                "slot_id": slot.id,
                "dog_id": dog.id,
                "service_ids": [service.id for service in services],
                "subtotal": subtotal,
                "total": total,
            }
            return redirect("booking_confirm")
    else:
        form = BookingCreateForm(user=request.user)

    return render(request, "booking/booking_create.html", {"form": form})


@login_required
def booking_confirm(request):
    draft = request.session.get("booking_draft")
    if not draft:
        return redirect("booking_create")

    slot = get_object_or_404(TimeSlot, id=draft["slot_id"], is_open=True)
    dog = get_object_or_404(Dog, id=draft["dog_id"], owner__user=request.user)

    services = Service.objects.filter(id__in=draft["service_ids"])

    if request.method == "POST":
        # Prevent race conditions
        with transaction.atomic():
            slot = TimeSlot.objects.select_for_update().get(id=slot.id) # type: ignore

            if not slot.is_open:
                # someone else took it
                return render(request, "booking/booking_confirm.html", {
                    "draft": draft,
                    "slot": slot,
                    "dog": dog,
                    "services": services,
                    "error": "Sorry — that slot was just booked. Please choose another time.",
                })

            booking = Booking.objects.create(
                user=request.user,
                dog=dog,
                slot=slot,
                status=Booking.Status.CONFIRMED,
                subtotal=draft["subtotal"],
                total=draft["total"],
            )

            for service in services:
                BookingService.objects.create(
                    booking=booking,
                    service=service,
                    price=service.base_price,
                )

            slot.is_open = False
            slot.save()

        request.session.pop("booking_draft", None)
        
        return redirect("booking_success", booking_id=booking.id) # type: ignore

    return render(request, "booking/booking_confirm.html", {
        "draft": draft,
        "slot": slot,
        "dog": dog,
        "services": services,
    })