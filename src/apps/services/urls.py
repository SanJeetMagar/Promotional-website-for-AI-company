from .views import ExpertiseListView
from django.urls import path    


urlpatterns = [
    path('', ExpertiseListView.as_view(), name='expertise-list'),
]