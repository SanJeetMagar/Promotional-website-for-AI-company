from .views import TeamMemberListCreateView, CEOMessageListCreateView
from django.urls import path

urlpatterns = [
    path('team/members/', TeamMemberListCreateView.as_view(), name='team-member-list'),
    path('ceo/messages/', CEOMessageListCreateView.as_view(), name='ceo-message-list'),
]