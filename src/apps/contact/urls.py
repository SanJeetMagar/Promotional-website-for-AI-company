from .views import ContactMessageCreateView
from django.urls import path    

urlpatterns = [
    path('', ContactMessageCreateView.as_view(), name='contact-message-create')
#     path('info/', ContactInfoView.as_view(), name='contact-info'),
]