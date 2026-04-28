from .views import FAQListView
from django.urls import path

urlpatterns = [
    path('', FAQListView.as_view(), name='faq-list'),
]
