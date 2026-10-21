from django.urls import path
from . import views

urlpatterns=[
    path('',views.login_,name='login'),
    path('logout',views.logout_,name='logout'),
    path('register',views.register,name='register'),
    path('profile',views.profile,name='profile'),
    path('upProf',views.upProf,name='upProf'),
    path('resPass',views.resPass,name='resPass'),
]