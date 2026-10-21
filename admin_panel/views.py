
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from base.models import (
    Flight_company_model,
    FlightDetails_new,
    Bookings2,
    SeatReservation,
)

from .forms import AdminRegistrationForm


# Admin access
staff_required = user_passes_test(
    lambda user: user.is_authenticated and user.is_staff,
    login_url='admin_login'
)


# Admin registration
def admin_register(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)

        if form.is_valid():
            cleaned = form.cleaned_data
            User = get_user_model()

            user = User.objects.create_user(
                username=cleaned['username'],
                email=cleaned['email'],
                password=cleaned['password1'],
                first_name=cleaned['first_name'],
                last_name=cleaned['last_name'],
            )

            user.is_staff = True
            user.save()

            messages.success(
                request, 'Admin account created successfully.'
            )
            return redirect('admin_login')

    else:
        form = AdminRegistrationForm()

    return render(request, 'adRegister.html', {'form': form})


# Admin login
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard')

    error = False

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')

        error = True

    return render(request, 'adlogin.html', {'error': error})


# Admin logout
@staff_required
def admin_logout(request):
    if request.method == 'POST':
        logout(request)

    return redirect('admin_login')


# Dashboard
@staff_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'flight_count': FlightDetails_new.objects.count(),
        'company_count': Flight_company_model.objects.count(),
        'booking_count': Bookings2.objects.count(),
        'seat_count': SeatReservation.objects.count(),
    })


# Flight company CRUD
@staff_required
def companies(request):
    all_companies = Flight_company_model.objects.all()

    return render(request, 'companies.html', {
        'all_companies': all_companies,
    })


@staff_required
def company_add(request):
    if request.method == 'POST':
        company_name = request.POST.get('flight_company', '')

        Flight_company_model.objects.create(
            flight_company=company_name
        )

        return redirect('compList')

    return render(request, 'company_form.html', {
        'heading': 'Add Flight Company',
        'company_name': '',
    })


@staff_required
def company_edit(request, company_id):
    company = get_object_or_404(
        Flight_company_model, id=company_id
    )

    if request.method == 'POST':
        company.flight_company = request.POST.get(
            'flight_company', ''
        )
        company.save()

        return redirect('compList')

    return render(request, 'company_form.html', {
        'heading': 'Edit Flight Company',
        'company_name': company.flight_company,
        'company': company,
    })


@staff_required
def company_delete(request, company_id):
    company = get_object_or_404(
        Flight_company_model, id=company_id
    )

    if request.method == 'POST':
        company.delete()
        return redirect('compList')

    return render(request, 'confirm_delete.html', {
        'item': company,
        'heading': 'Delete Flight Company',
        'cancel_url_name': 'compList',
        'warning': 'Delete this flight company?',
    })


# Flight CRUD
@staff_required
def flights(request):
    all_flights = FlightDetails_new.objects.all()

    return render(request, 'flights.html', {
        'all_flights': all_flights,
    })


@staff_required
def flight_add(request):
    if request.method == 'POST':
        company = get_object_or_404(
            Flight_company_model,
            id=request.POST.get('flight_company')
        )

        FlightDetails_new.objects.create(
            flight_company=company,
            flight_name=request.POST.get('flight_name'),
            flight_number=request.POST.get('flight_number'),
            flight_from=request.POST.get('flight_from'),
            flight_to=request.POST.get('flight_to'),
            flight_departure_time=request.POST.get(
                'flight_departure_time'
            ),
            flight_date=request.POST.get('flight_date'),
            flight_ticket_price=request.POST.get(
                'flight_ticket_price'
            ),
            total_seats=request.POST.get('total_seats', 180),
        )

        return redirect('flightList')

    companies = Flight_company_model.objects.all()

    return render(request, 'flight_form.html', {
        'heading': 'Add Flight',
        'companies': companies,
        'values': {},
    })


@staff_required
def flight_edit(request, flight_id):
    flight = get_object_or_404(
        FlightDetails_new, id=flight_id
    )

    if request.method == 'POST':
        flight.flight_company = get_object_or_404(
            Flight_company_model,
            id=request.POST.get('flight_company')
        )

        flight.flight_name = request.POST.get('flight_name')
        flight.flight_number = request.POST.get('flight_number')
        flight.flight_from = request.POST.get('flight_from')
        flight.flight_to = request.POST.get('flight_to')
        flight.flight_departure_time = request.POST.get(
            'flight_departure_time'
        )
        flight.flight_date = request.POST.get('flight_date')
        flight.flight_ticket_price = request.POST.get(
            'flight_ticket_price'
        )
        flight.total_seats = request.POST.get('total_seats')

        flight.save()
        return redirect('flightList')

    companies = Flight_company_model.objects.all()

    values = {
        'flight_company': str(flight.flight_company_id),
        'flight_name': flight.flight_name,
        'flight_number': flight.flight_number,
        'flight_from': flight.flight_from,
        'flight_to': flight.flight_to,
        'flight_departure_time': flight.flight_departure_time.strftime('%H:%M'),
        'flight_date': flight.flight_date.isoformat(),
        'flight_ticket_price': str(flight.flight_ticket_price),
        'total_seats': str(flight.total_seats),
    }

    return render(request, 'flight_form.html', {
        'heading': 'Edit Flight',
        'flight': flight,
        'companies': companies,
        'values': values,
    })


@staff_required
def flight_delete(request, flight_id):
    flight = get_object_or_404(
        FlightDetails_new, id=flight_id
    )

    if request.method == 'POST':
        flight.delete()
        return redirect('flightList')

    return render(request, 'confirm_delete.html', {
        'item': flight,
        'heading': 'Delete Flight',
        'cancel_url_name': 'flightList',
        'warning': 'Delete this flight?',
    })


# Booking management
@staff_required
def adBookings(request):
    all_bookings = Bookings2.objects.all()

    return render(request, 'adBookings.html', {
        'all_bookings': all_bookings,
    })


@staff_required
def booking_delete(request, booking_id):
    booking = get_object_or_404(
        Bookings2, id=booking_id
    )

    if request.method == 'POST':
        booking.delete()
        return redirect('admin_bookings')

    return render(request, 'confirm_delete.html', {
        'item': booking,
        'heading': 'Delete Booking',
        'cancel_url_name': 'admin_bookings',
        'warning': 'Delete this booking?',
    })


# Seat reservation management
@staff_required
def seats(request):
    all_seats = SeatReservation.objects.all()

    return render(request, 'seats.html', {
        'all_seats': all_seats,
    })


@staff_required
def seat_edit(request, seat_id):
    seat = get_object_or_404(
        SeatReservation, id=seat_id
    )

    if request.method == 'POST':
        seat.seat_number = request.POST.get('seat_number')
        seat.save()

        return redirect('admin_seats')

    return render(request, 'seat_form.html', {
        'seat': seat,
        'heading': 'Edit Seat Reservation',
    })


@staff_required
def seat_delete(request, seat_id):
    seat = get_object_or_404(
        SeatReservation, id=seat_id
    )

    if request.method == 'POST':
        seat.delete()
        return redirect('admin_seats')

    return render(request, 'confirm_delete.html', {
        'item': seat,
        'heading': 'Delete Seat Reservation',
        'cancel_url_name': 'admin_seats',
        'warning': 'Delete this seat reservation?',
    })
