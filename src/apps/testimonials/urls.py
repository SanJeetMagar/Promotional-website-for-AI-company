from .views import TestimonialListView
from django.urls import path

urlpatterns = [
    path('testimonials/', TestimonialListView.as_view(), name='testimonial-list'),
]   