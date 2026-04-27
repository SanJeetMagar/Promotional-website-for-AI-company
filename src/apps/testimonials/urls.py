from .views import TestimonialListView
from django.urls import path

urlpatterns = [
    path('', TestimonialListView.as_view(), name='testimonial-list'),
]   