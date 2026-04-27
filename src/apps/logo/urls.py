from .views import LogoListView
from django.urls import path        

urlpatterns = [
    path('', LogoListView.as_view(), name='logo-list'),
]   