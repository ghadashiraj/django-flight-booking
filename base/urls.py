from django.urls import path
from . import views

urlpatterns=[
    path('home',views.home,name='home'),
    path('history',views.history,name='history'),
    path('bookings',views.bookings,name='bookings'),
    path('about',views.about,name='about'),
    path('support',views.support,name='support'),
    path('bookNow/<int:bpk>',views.bookNow,name='bookNow'),
    path('update/<int:upk>',views.update,name='update'),
    path('delBook/<int:dpk>',views.delBook,name='delBook'),
]