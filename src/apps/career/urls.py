from .views import CareerListView
from django.urls import path

urlpatterns = [
    path('', CareerListView.as_view(), name='career-list'),
]