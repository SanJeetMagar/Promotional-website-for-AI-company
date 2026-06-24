from django.urls import path
from .views import (
    # Event Views
    EventListView, EventDetailView, EventCreateView,
    EventUpdateView, EventDeleteView,
    # Speaker Views
    SpeakerListView, SpeakerDetailView, SpeakerCreateView,
    SpeakerUpdateView, SpeakerDeleteView,
    # Tag Views
    EventTagListView, EventTagCreateView, EventTagUpdateView,
    EventTagDeleteView,
    # Registration Views
    EventRegistrationCreateView, EventRegistrationListView,
    EventRegistrationDetailView, EventRegistrationCancelView,
    EventRegistrationConfirmView,
    # Gallery Views
    EventGalleryCreateView, EventGalleryDeleteView,
)

app_name = 'events'

urlpatterns = [
    # Event URLs
    path('', EventListView.as_view(), name='event-list'),
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('<slug:slug>/', EventDetailView.as_view(), name='event-detail'),
    path('update/', EventUpdateView.as_view(), name='event-update'),
    path('delete/', EventDeleteView.as_view(), name='event-delete'),
    
    # Speaker URLs
    path('speakers/', SpeakerListView.as_view(), name='speaker-list'),
    path('speakers/create/', SpeakerCreateView.as_view(), name='speaker-create'),
    path('speakers/<int:pk>/', SpeakerDetailView.as_view(), name='speaker-detail'),
    path('speakers/<int:pk>/update/', SpeakerUpdateView.as_view(), name='speaker-update'),
    path('speakers/<int:pk>/delete/', SpeakerDeleteView.as_view(), name='speaker-delete'),
    
    # Tag URLs
    path('tags/', EventTagListView.as_view(), name='tag-list'),
    path('tags/create/', EventTagCreateView.as_view(), name='tag-create'),
    path('tags/<int:pk>/update/', EventTagUpdateView.as_view(), name='tag-update'),
    path('tags/<int:pk>/delete/', EventTagDeleteView.as_view(), name='tag-delete'),
    
    # Registration URLs
    path('registrations/', EventRegistrationListView.as_view(), name='registration-list'),
    path('registrations/create/', EventRegistrationCreateView.as_view(), name='registration-create'),
    path('registrations/<int:pk>/', EventRegistrationDetailView.as_view(), name='registration-detail'),
    path('registrations/<int:pk>/cancel/', EventRegistrationCancelView.as_view(), name='registration-cancel'),
    path('registrations/<int:pk>/confirm/', EventRegistrationConfirmView.as_view(), name='registration-confirm'),
    
    # Gallery URLs
    path('gallery/upload/', EventGalleryCreateView.as_view(), name='gallery-upload'),
    path('gallery/<int:pk>/delete/', EventGalleryDeleteView.as_view(), name='gallery-delete'),
]