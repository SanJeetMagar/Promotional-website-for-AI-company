from .views import TeamMemberListView, CEOMessageView
from django.urls import path

urlpatterns = [
    path('team-members/', TeamMemberListView.as_view(), name='team-member-list'),
    path('ceo-messages/', CEOMessageView.as_view(), name='ceo-message-list'),
]