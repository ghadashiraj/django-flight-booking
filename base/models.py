# from django.db import models
# from django.contrib.auth.models import User
# # Create your models here.
# class Flight_company_model(models.Model):
#     flight_company=models.CharField(max_length=100)

#     def __str__(self):
#         return self.flight_company

# class FlightDetails_new(models.Model):
#     flight_company=models.ForeignKey(Flight_company_model,on_delete=models.CASCADE)
#     flight_name=models.CharField(max_length=100)
#     flight_number=models.CharField(default=0)
#     flight_from=models.CharField(max_length=100)
#     flight_to=models.CharField(max_length=100)
#     flight_departure_time=models.TimeField()
#     flight_date=models.DateField(max_length=100)
#     flight_ticket_price=models.IntegerField(default=0)

#     def __str__(self):
#         return self.flight_name



# class Bookings2(models.Model):
#     flight_company=models.CharField(max_length=100)
#     flight_name=models.CharField(max_length=100)
#     flight_number=models.CharField(default=0)
#     flight_from=models.CharField(max_length=100)
#     flight_to=models.CharField(max_length=100)
#     flight_departure_time=models.CharField(max_length=100)
#     flight_date=models.CharField(max_length=100)
#     flight_ticket_price=models.IntegerField(default=0)
#     pname=models.CharField(max_length=100)
#     ano=models.CharField(max_length=100)
#     phno=models.CharField(max_length=100)
#     email=models.CharField(max_length=100)
#     sno=models.CharField(max_length=100)
#     host=models.ForeignKey(User,on_delete=models.CASCADE)


# class History(models.Model):
#     flight_company=models.CharField(max_length=100)
#     flight_name=models.CharField(max_length=100)
#     flight_number=models.CharField(default=0)
#     flight_from=models.CharField(max_length=100)
#     flight_to=models.CharField(max_length=100)
#     flight_departure_time=models.CharField(max_length=100)
#     flight_date=models.CharField(max_length=100)
#     flight_ticket_price=models.IntegerField(default=0)
#     pname=models.CharField(max_length=100)
#     ano=models.CharField(max_length=100)
#     phno=models.CharField(max_length=100)
#     email=models.CharField(max_length=100)
#     sno=models.CharField(max_length=100)
#     host=models.ForeignKey(User,on_delete=models.CASCADE)


from django.db import models
from django.contrib.auth.models import User


class Flight_company_model(models.Model):
    flight_company = models.CharField(max_length=100)

    def __str__(self):
        return self.flight_company


class FlightDetails_new(models.Model):
    flight_company = models.ForeignKey(Flight_company_model, on_delete=models.CASCADE)
    flight_name = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20)
    flight_from = models.CharField(max_length=100)
    flight_to = models.CharField(max_length=100)
    flight_departure_time = models.TimeField()
    flight_date = models.DateField()
    flight_ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.PositiveIntegerField(default=180)

    def __str__(self):
        return self.flight_name


class Bookings2(models.Model):
    flight_company = models.CharField(max_length=100)
    flight_name = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20)
    flight_from = models.CharField(max_length=100)
    flight_to = models.CharField(max_length=100)
    flight_departure_time = models.CharField(max_length=50)
    flight_date = models.CharField(max_length=50)
    flight_ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    pname = models.CharField(max_length=100)
    ano = models.CharField(max_length=50, blank=True)
    phno = models.CharField(max_length=15, blank=True)
    email = models.EmailField()
    sno = models.CharField(max_length=100)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(FlightDetails_new, on_delete=models.CASCADE)

    def __str__(self):
        return self.pname


class SeatReservation(models.Model):
    booking = models.ForeignKey(
        Bookings2,
        on_delete=models.CASCADE,
        related_name="seat_reservations"
    )
    flight = models.ForeignKey(FlightDetails_new, on_delete=models.CASCADE)

    # Passenger details
    seat_number = models.CharField(max_length=10)
    pname = models.CharField(max_length=100)
    ano = models.CharField(max_length=50, blank=True)
    phno = models.CharField(max_length=15, blank=True)
    email = models.EmailField()
    host = models.ForeignKey(User, on_delete=models.CASCADE)

    # Flight details
    flight_company = models.CharField(max_length=100)
    flight_name = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20)
    flight_from = models.CharField(max_length=100)
    flight_to = models.CharField(max_length=100)
    flight_departure_time = models.CharField(max_length=50)
    flight_date = models.CharField(max_length=50)
    flight_ticket_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['flight', 'seat_number'],
                name='unique_seat_per_flight'
            )
        ]

    def __str__(self):
        return f"{self.pname} - {self.seat_number}"


class History(models.Model):
    flight_company = models.CharField(max_length=100)
    flight_name = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20)
    flight_from = models.CharField(max_length=100)
    flight_to = models.CharField(max_length=100)
    flight_departure_time = models.CharField(max_length=50)
    flight_date = models.CharField(max_length=50)
    flight_ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    pname = models.CharField(max_length=100)
    ano = models.CharField(max_length=50, blank=True)
    phno = models.CharField(max_length=15, blank=True)
    email = models.EmailField()
    sno = models.CharField(max_length=10)
    host = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.pname
