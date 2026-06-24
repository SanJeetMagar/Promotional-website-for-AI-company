from django.urls import path
from .views import FAQListView, FAQDetailView, FAQCreateView, FAQUpdateView, FAQDeleteView

urlpatterns = [
    path('', FAQListView.as_view(), name='faq-list'),
    path('create/', FAQCreateView.as_view(), name='faq-create'),
    path('<int:pk>/', FAQDetailView.as_view(), name='faq-detail'),
    path('<int:pk>/update/', FAQUpdateView.as_view(), name='faq-update'),
    path('<int:pk>/delete/', FAQDeleteView.as_view(), name='faq-delete'),
]