from django.urls import path
from .views import (
    EventListView, EventDetailView, EventCreateView,
    EventUpdateView, EventDeleteView,
    SpeakerListView, SpeakerDetailView, SpeakerCreateView,
    SpeakerUpdateView, SpeakerDeleteView,
    EventTagListView, EventTagCreateView, EventTagUpdateView,
    EventTagDeleteView,
    EventRegistrationCreateView, EventRegistrationListView,
    EventRegistrationDetailView, EventRegistrationCancelView,
    EventRegistrationConfirmView,
    EventGalleryCreateView, EventGalleryDeleteView,
)

app_name = 'events'

urlpatterns = [
    # Event URLs
    path('', EventListView.as_view(), name='event-list'),
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('<slug:slug>/', EventDetailView.as_view(), name='event-detail'),
    path('<slug:slug>/update/', EventUpdateView.as_view(), name='event-update'),       # Bug 1
    path('<slug:slug>/delete/', EventDeleteView.as_view(), name='event-delete'),       # Bug 1

    # Speaker URLs
    path('speakers/', SpeakerListView.as_view(), name='speaker-list'),
    path('speakers/create/', SpeakerCreateView.as_view(), name='speaker-create'),
    path('speakers/<slug:slug>/', SpeakerDetailView.as_view(), name='speaker-detail'),         # Bug 2
    path('speakers/<slug:slug>/update/', SpeakerUpdateView.as_view(), name='speaker-update'),  # Bug 2
    path('speakers/<slug:slug>/delete/', SpeakerDeleteView.as_view(), name='speaker-delete'),  # Bug 2

    # Tag URLs
    path('tags/', EventTagListView.as_view(), name='tag-list'),
    path('tags/create/', EventTagCreateView.as_view(), name='tag-create'),
    path('tags/<slug:slug>/update/', EventTagUpdateView.as_view(), name='tag-update'),  # Bug 3
    path('tags/<slug:slug>/delete/', EventTagDeleteView.as_view(), name='tag-delete'),  # Bug 3

    # Registration URLs
    path('registrations/', EventRegistrationListView.as_view(), name='registration-list'),
    path('registrations/create/', EventRegistrationCreateView.as_view(), name='registration-create'),
    path('registrations/<str:confirmation_code>/', EventRegistrationDetailView.as_view(), name='registration-detail'),         # Bug 4
    path('registrations/<str:confirmation_code>/cancel/', EventRegistrationCancelView.as_view(), name='registration-cancel'),  # Bug 4
    path('registrations/<int:pk>/confirm/', EventRegistrationConfirmView.as_view(), name='registration-confirm'),

    # Gallery URLs
    path('<slug:slug>/gallery/upload/', EventGalleryCreateView.as_view(), name='gallery-upload'),  # Bug 5
    path('gallery/<int:pk>/delete/', EventGalleryDeleteView.as_view(), name='gallery-delete'),
]