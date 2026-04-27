from .views import ContactMessageCreateView, ContactInfoView
from django.urls import path    

urlpatterns = [
    path('', ContactMessageCreateView.as_view(), name='contact-message-create'),
    path('info/', ContactInfoView.as_view(), name='contact-info'),
]