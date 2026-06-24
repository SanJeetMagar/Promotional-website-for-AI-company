from django.urls import path
from .views import (
    ProductDropdownListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

urlpatterns = [
    path('', ProductDropdownListView.as_view(), name='product-dropdown-list'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('<slug:slug>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<slug:slug>/delete/', ProductDeleteView.as_view(), name='product-delete'),
]