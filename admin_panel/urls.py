
from django.urls import path
from . import views

urlpatterns = [
    # Admin authentication
    path('admin_register', views.admin_register, name='admin_register'),
    path('', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard', views.dashboard, name='dashboard'),

    # Flight company CRUD
    path('companies/', views.companies, name='compList'),
    path('compAdd', views.company_add, name='compAdd'),
    path('compEdit/<int:company_id>', views.company_edit, name='compEdit'),
    path('compDelete/<int:company_id>', views.company_delete, name='compDelete'),

    # Flight CRUD
    path('flights/', views.flights, name='flightList'),
    path('flightAdd', views.flight_add, name='flightAdd'),
    path('flightEdit/<int:flight_id>', views.flight_edit, name='flightEdit'),
    path('flightDelete/<int:flight_id>', views.flight_delete, name='flightDelete'),

    # Booking management
    path('adBookings/', views.adBookings, name='admin_bookings'),
    path(
        'bookings/<int:booking_id>/delete/',
        views.booking_delete,
        name='admin_booking_delete'
    ),

    # Seat management
    path('seats/', views.seats, name='admin_seats'),
    path(
        'seats/<int:seat_id>/edit/',
        views.seat_edit,
        name='admin_seat_edit'
    ),
    path(
        'seats/<int:seat_id>/delete/',
        views.seat_delete,
        name='admin_seat_delete'
    ),
]
