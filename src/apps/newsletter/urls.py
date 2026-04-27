from .views import NewsletterCreateView
from django.urls import path    

urlpatterns = [
    path('', NewsletterCreateView.as_view(), name='newsletter-create'),
]