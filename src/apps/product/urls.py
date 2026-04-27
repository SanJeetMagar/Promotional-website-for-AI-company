from .views import ProductDropdownListView, ProductDetailView
from django.urls import path

urlpatterns = [
    path('', ProductDropdownListView.as_view(), name='product-dropdown-list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
]