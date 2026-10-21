# from django.shortcuts import render,redirect
# from django.contrib.auth.decorators import login_required
# from base.models import FlightDetails_new,Bookings2,History
# from django.db.models import Q
 
# #  ! Flight booking

# @login_required(login_url='login')
# def home(request):
#     # od=FlightDetails_new.objects.all()

#     if 'from' in request.GET:
#         from_data=request.GET['from']
#         to_data=request.GET['to']
#         # ^SEARCH OPERATION <<<<<<<<<<--------------------
#         od=FlightDetails_new.objects.filter(Q(flight_from__icontains=from_data) & Q(flight_to__icontains=to_data))

#         return render(request,'home.html',{'od':od,'flight_search':True})
#     else:
#         od=FlightDetails_new.objects.all().order_by('flight_date')
#     return render(request,'home.html',{'od':od})

# @login_required(login_url='login')
# def history(request):
#     hData=History.objects.filter(host=request.user)
#     return render(request,'history.html',{'hData':hData})

# @login_required(login_url='login')
# def bookings(request):
#     all_bookings=Bookings2.objects.filter(host=request.user)
#     return render(request,'bookings.html',{'all_bookings':all_bookings})

# def about(request):
#     return render(request,'about.html')

# def support(request):
#     return render(request,'support.html')
# @login_required(login_url='login')
# def bookNow(request,bpk):
#     flight=FlightDetails_new.objects.get(id=bpk)

#     if request.method == 'POST':
#         flight_company=request.POST['cname']
#         flight_name=request.POST['fname']
#         flight_number=request.POST['fno']
#         flight_from=request.POST['fromloc']
#         flight_to=request.POST['to']
#         flight_departure_time=request.POST['time']
#         flight_date=request.POST['date']
#         flight_ticket_price=request.POST['price']
#         pname=request.POST['pname']
#         ano=request.POST['ano']
#         phno=request.POST['phno']
#         email=request.POST['email']
#         sno=request.POST['sno']

#         Bookings2.objects.create(flight_company=flight_company,flight_name=flight_name,flight_number=flight_number,flight_from=flight_from,flight_to=flight_to,flight_departure_time=flight_departure_time,flight_date=flight_date,flight_ticket_price=flight_ticket_price,pname=pname,ano=ano,phno=phno,email=email,sno=sno,host=request.user)

#         return redirect('bookings')
#     return render(request,'bookNow.html',{'flight':flight})


# def update(request,upk):
#     us=Bookings2.objects.get(id=upk)

#     if request.method == 'POST':
#         pname=request.POST['pname']
#         ano=request.POST['ano']
#         phno=request.POST['phno']
#         email=request.POST['email']
#         us.pname=pname
#         us.ano=ano
#         us.phno=phno
#         us.email=email
#         us.save()
#         return redirect('bookings')
#     return render(request,'update.html',{'us':us})


# def delBook(request,dpk):
#     ddata=Bookings2.objects.get(id=dpk)
#     History.objects.create(flight_company=ddata.flight_company,
#                            flight_name=ddata.flight_name,
#                            flight_number=ddata.flight_number,
#                            flight_from=ddata.flight_from,
#                            flight_to=ddata.flight_to,
#                            flight_departure_time=ddata.flight_departure_time,
#                            flight_date=ddata.flight_date,
#                            flight_ticket_price=ddata.flight_ticket_price,
#                            pname=ddata.pname,
#                            ano=ddata.ano,
#                            phno=ddata.phno,
#                            email=ddata.email,
#                            sno=ddata.sno,
#                            host=ddata.host)
#     ddata.delete()
#     return redirect('history')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.models import FlightDetails_new, Bookings2, History, SeatReservation
from django.db.models import Q
from django.db import transaction


@login_required(login_url='login')
def home(request):

    if 'from' in request.GET:
        from_data = request.GET['from']
        to_data = request.GET['to']

        od = FlightDetails_new.objects.filter(
            Q(flight_from__icontains=from_data) &
            Q(flight_to__icontains=to_data)
        )

        return render(request, 'home.html', {
            'od': od,
            'flight_search': True
        })

    else:
        od = FlightDetails_new.objects.all().order_by('flight_date')

    return render(request, 'home.html', {'od': od})


@login_required(login_url='login')
def history(request):

    hData = History.objects.filter(host=request.user)

    return render(request, 'history.html', {'hData': hData})


@login_required(login_url='login')
def bookings(request):

    all_bookings = SeatReservation.objects.filter(host=request.user)

    return render(request, 'bookings.html', {
        'all_bookings': all_bookings
    })


def about(request):

    return render(request, 'about.html')


def support(request):

    return render(request, 'support.html')


@login_required(login_url='login')
def bookNow(request, bpk):

    flight = FlightDetails_new.objects.get(id=bpk)
    all_seats = [f"S{i}" for i in range(1, flight.total_seats + 1)]

    booked_seats = set(
        SeatReservation.objects.filter(
            flight=flight  
        ).values_list('seat_number', flat=True))  

    available_seats = [seat for seat in all_seats if seat not in booked_seats]

    if request.method == 'POST':

        passengers = []

        for i in range(1, 6):

            pname = request.POST.get(f'pname_{i}', '').strip()
            ano = request.POST.get(f'ano_{i}', '').strip()
            phno = request.POST.get(f'phno_{i}', '').strip()
            email = request.POST.get(f'email_{i}', '').strip()
            seat = request.POST.get(f'sno_{i}', '').strip()

            if not any([pname, ano, phno, email, seat]):  
                continue

            if not pname or not email or not seat:
                return render(request, 'bookNow.html', {
                    'flight': flight,
                    'available_seats': available_seats,
                    'error': (
                        f'Please enter the name, email and seat '
                        f'for Passenger {i}.'
                    )
                })

            passengers.append({
                'pname': pname,
                'ano': ano,
                'phno': phno,
                'email': email,
                'seat': seat
            })

        if not passengers:
            return render(request, 'bookNow.html', {
                'flight': flight,
                'available_seats': available_seats,
                'error': 'Please enter details for at least one passenger.'
            })

        seat_numbers = [p['seat'] for p in passengers]  

        if len(seat_numbers) != len(set(seat_numbers)):
            return render(request, 'bookNow.html', {
                'flight': flight,
                'available_seats': available_seats,
                'error': 'Each passenger must have a different seat.'
            })

        if not set(seat_numbers).issubset(set(available_seats)):
            return render(request, 'bookNow.html', {
                'flight': flight,
                'available_seats': available_seats,
                'error': (
                    'One or more seats are unavailable. '
                    'Please select again.'
                )
            })

        with transaction.atomic():

            first_passenger = passengers[0]

            booking = Bookings2.objects.create(
                flight_company=flight.flight_company.flight_company,
                flight_name=flight.flight_name,
                flight_number=flight.flight_number,
                flight_from=flight.flight_from,
                flight_to=flight.flight_to,
                flight_departure_time=str(
                    flight.flight_departure_time
                ),
                flight_date=str(flight.flight_date),
                flight_ticket_price=flight.flight_ticket_price,
                pname=first_passenger['pname'],
                ano=first_passenger['ano'],
                phno=first_passenger['phno'],
                email=first_passenger['email'],
                sno=', '.join(seat_numbers),
                host=request.user,
                flight=flight
            )

            for passenger in passengers:
                SeatReservation.objects.create(
                    booking=booking,
                    flight=flight,
                    seat_number=passenger['seat'],
                    pname=passenger['pname'],
                    ano=passenger['ano'],
                    phno=passenger['phno'],
                    email=passenger['email'],
                    host=request.user,

                    flight_company=booking.flight_company,
                    flight_name=booking.flight_name,
                    flight_number=booking.flight_number,
                    flight_from=booking.flight_from,
                    flight_to=booking.flight_to,
                    flight_departure_time=booking.flight_departure_time,
                    flight_date=booking.flight_date,
                    flight_ticket_price=booking.flight_ticket_price
                )

        return redirect('bookings')

    return render(request, 'bookNow.html', {
        'flight': flight,
        'available_seats': available_seats
    })


@login_required(login_url='login')
def update(request, upk):

    us = SeatReservation.objects.get(id=upk, host=request.user)

    if request.method == 'POST':

        pname = request.POST['pname']
        ano = request.POST['ano']
        phno = request.POST['phno']
        email = request.POST['email']

        us.pname = pname
        us.ano = ano
        us.phno = phno
        us.email = email

        us.save()

        return redirect('bookings')

    return render(request, 'update.html', {'us': us})


@login_required(login_url='login')
def delBook(request, dpk):

    ddata = SeatReservation.objects.get(id=dpk, host=request.user)

    History.objects.create(
                flight_company=ddata.flight_company,
                flight_name=ddata.flight_name,
                flight_number=ddata.flight_number,
                flight_from=ddata.flight_from,
                flight_to=ddata.flight_to,
                flight_departure_time=ddata.flight_departure_time,
                flight_date=ddata.flight_date,
                flight_ticket_price=ddata.flight_ticket_price,
                pname=ddata.pname,
                ano=ddata.ano,
                phno=ddata.phno,
                email=ddata.email,
                sno=ddata.seat_number,
                host=ddata.host
            )

    # # Get individual passenger reservations
    # reservations = list(ddata.seat_reservations.all())

    # if reservations:

    #     # Save each passenger separately in history
    #     for passenger in reservations:
    #         History.objects.create(
    #             flight_company=ddata.flight_company,
    #             flight_name=ddata.flight_name,
    #             flight_number=ddata.flight_number,
    #             flight_from=ddata.flight_from,
    #             flight_to=ddata.flight_to,
    #             flight_departure_time=ddata.flight_departure_time,
    #             flight_date=ddata.flight_date,
    #             flight_ticket_price=ddata.flight_ticket_price,
    #             pname=passenger.pname,
    #             ano=passenger.ano,
    #             phno=passenger.phno,
    #             email=passenger.email,
    #             sno=passenger.seat_number,
    #             host=ddata.host
    #         )

    # else:
    #     # Preserve history for older bookings
    #     # that do not have individual seat reservations
    #     History.objects.create(
    #         flight_company=ddata.flight_company,
    #         flight_name=ddata.flight_name,
    #         flight_number=ddata.flight_number,
    #         flight_from=ddata.flight_from,
    #         flight_to=ddata.flight_to,
    #         flight_departure_time=ddata.flight_departure_time,
    #         flight_date=ddata.flight_date,
    #         flight_ticket_price=ddata.flight_ticket_price,
    #         pname=ddata.pname,
    #         ano=ddata.ano,
    #         phno=ddata.phno,
    #         email=ddata.email,
    #         sno=ddata.sno,
    #         host=ddata.host
    #     )

    ddata.delete()

    return redirect('history')
