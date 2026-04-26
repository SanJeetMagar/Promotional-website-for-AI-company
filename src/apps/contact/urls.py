from .views import ContactMessageCreateView
from django.urls import path    

urlpatterns = [
    path('contact/messages/', ContactMessageCreateView.as_view(), name='contact-message-create'),
]