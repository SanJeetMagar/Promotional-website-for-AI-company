from django.urls import path
from .views import (
    TeamMemberListView, AdminTeamMemberListView, TeamMemberDetailView, 
    TeamMemberCreateView, TeamMemberUpdateView, TeamMemberDeleteView,
    
    CEOMessageView, AdminCEOMessageListView, CEOMessageDetailView, 
    CEOMessageCreateView, CEOMessageUpdateView, CEOMessageDeleteView
)

urlpatterns = [
    # --- Public Team ---
    path('members/', TeamMemberListView.as_view(), name='team-member-list'),
    path('members/<int:pk>/', TeamMemberDetailView.as_view(), name='team-member-detail'),
    
    # --- Admin Team ---
    path('members/admin/all/', AdminTeamMemberListView.as_view(), name='admin-team-member-list'),
    path('members/admin/create/', TeamMemberCreateView.as_view(), name='team-member-create'),
    path('members/admin/<int:pk>/update/', TeamMemberUpdateView.as_view(), name='team-member-update'),
    path('members/admin/<int:pk>/delete/', TeamMemberDeleteView.as_view(), name='team-member-delete'),

    # --- Public CEO Message ---
    path('ceo-message/active/', CEOMessageView.as_view(), name='ceo-message-active'),
    
    # --- Admin CEO Messages ---
    path('ceo-messages/admin/all/', AdminCEOMessageListView.as_view(), name='admin-ceo-message-list'),
    path('ceo-messages/admin/create/', CEOMessageCreateView.as_view(), name='ceo-message-create'),
    path('ceo-messages/admin/<int:pk>/', CEOMessageDetailView.as_view(), name='ceo-message-detail'),
    path('ceo-messages/admin/<int:pk>/update/', CEOMessageUpdateView.as_view(), name='ceo-message-update'),
    path('ceo-messages/admin/<int:pk>/delete/', CEOMessageDeleteView.as_view(), name='ceo-message-delete'),
]