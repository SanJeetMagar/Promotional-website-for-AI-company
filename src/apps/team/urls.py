from .views import TeamMemberListView, CEOMessageListView
from django.urls import path

urlpatterns = [
    path('team/members/', TeamMemberListView.as_view(), name='team-member-list'),
    path('ceo/messages/', CEOMessageListView.as_view(), name='ceo-message-list'),
]