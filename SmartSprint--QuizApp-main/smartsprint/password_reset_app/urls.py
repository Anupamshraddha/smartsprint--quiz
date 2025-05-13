from django.urls import path
from . import views

urlpatterns = [
    path('reset/', views.request_reset, name='request_reset'),
    path('reset/otp/', views.display_otp, name='display_otp'),
    path('reset/verify/', views.verify_otp, name='verify_otp'),
    path('reset/password/', views.reset_password, name='reset_password'),
    path('reset/success/', views.reset_success, name='reset_success'),
]