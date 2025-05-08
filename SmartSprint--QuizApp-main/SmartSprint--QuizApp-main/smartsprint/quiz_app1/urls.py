from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.reviews, name='reviews'),
    path('external-reviews/', views.flask_reviews_view, name='external_reviews'),
]
