from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Prefetch
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import (
    Event, EventTag, Speaker, EventGallery, EventRegistration,
    EventStatus, EventType
)
from .serializers import (
    EventListSerializer, EventDetailSerializer,
    EventCreateUpdateSerializer, EventTagSerializer,
    SpeakerSerializer, EventGallerySerializer,
    EventRegistrationSerializer, EventRegistrationListSerializer
)
from .permissions import IsAdminOrReadOnly


# ============== Event Views ==============

@extend_schema(
    tags=['Events'],
    summary="List and search events",
    parameters=[
        OpenApiParameter('search', OpenApiTypes.STR, description='Search in title and description'),
        OpenApiParameter('status', OpenApiTypes.STR, description='Filter by status'),
        OpenApiParameter('event_type', OpenApiTypes.STR, description='Filter by event type'),
        OpenApiParameter('tag', OpenApiTypes.STR, description='Filter by tag slug'),
        OpenApiParameter('featured', OpenApiTypes.BOOL, description='Filter featured events'),
        OpenApiParameter('upcoming', OpenApiTypes.BOOL, description='Show only upcoming events'),
    ]
)
class EventListView(generics.ListAPIView):
    serializer_class = EventListSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['event_date', 'view_count', 'title']
    ordering = ['event_date']

    def get_queryset(self):
        queryset = Event.objects.select_related().prefetch_related(
            'tags',
            'event_speakers__speaker',
            Prefetch('registrations', queryset=EventRegistration.objects.filter(status='confirmed'))
        ).annotate(
            registered_count=Count('registrations', filter=Q(registrations__status='confirmed'))
        )

        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(venue_name__icontains=search)
            )

        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by event type
        event_type = self.request.query_params.get('event_type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)

        # Filter by tag
        tag_slug = self.request.query_params.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        # Filter featured
        featured = self.request.query_params.get('featured')
        if featured is not None:
            is_featured = featured.lower() == 'true'
            queryset = queryset.filter(is_featured=is_featured)

        # Show only upcoming
        upcoming = self.request.query_params.get('upcoming')
        if upcoming and upcoming.lower() == 'true':
            queryset = queryset.filter(
                event_date__gte=timezone.now().date(),
                status=EventStatus.UPCOMING
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Group by status for homepage
        if not request.query_params:
            upcoming = queryset.filter(
                status=EventStatus.UPCOMING,
                event_date__gte=timezone.now().date()
            ).order_by('event_date')[:6]

            past = queryset.filter(
                status=EventStatus.COMPLETED
            ).order_by('-event_date')[:6]

            return Response({
                'upcoming': self.get_serializer(upcoming, many=True).data,
                'past': self.get_serializer(past, many=True).data
            })

        return super().list(request, *args, **kwargs)


@extend_schema(tags=['Events'], summary="Get event details")
class EventDetailView(generics.RetrieveAPIView):
    serializer_class = EventDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return Event.objects.select_related().prefetch_related(
            'tags',
            'event_speakers__speaker',
            'agenda_items__speaker',
            'gallery_images',
            Prefetch('registrations', queryset=EventRegistration.objects.filter(status='confirmed'))
        ).annotate(
            registered_count=Count('registrations', filter=Q(registrations__status='confirmed'))
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(tags=['Events'], summary="Create a new event")
class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]


@extend_schema(tags=['Events'], summary="Update an event")
class EventUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'
    parser_classes = [MultiPartParser, FormParser]


@extend_schema(tags=['Events'], summary="Delete an event")
class EventDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'


# ============== Speaker Views ==============

@extend_schema(tags=['Speakers'], summary="List all speakers")
class SpeakerListView(generics.ListAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'title', 'company']
    ordering_fields = ['name']


@extend_schema(tags=['Speakers'], summary="Get speaker details")
class SpeakerDetailView(generics.RetrieveAPIView):
    queryset = Speaker.objects.prefetch_related('speaker_events__event')
    serializer_class = SpeakerSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


@extend_schema(tags=['Speakers'], summary="Create a new speaker")
class SpeakerCreateView(generics.CreateAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]


@extend_schema(tags=['Speakers'], summary="Update a speaker")
class SpeakerUpdateView(generics.UpdateAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'
    parser_classes = [MultiPartParser, FormParser]


@extend_schema(tags=['Speakers'], summary="Delete a speaker")
class SpeakerDeleteView(generics.DestroyAPIView):
    queryset = Speaker.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'


# ============== Tag Views ==============

@extend_schema(tags=['Event Tags'], summary="List all event tags")
class EventTagListView(generics.ListAPIView):
    queryset = EventTag.objects.annotate(
        event_count=Count('events')
    )
    serializer_class = EventTagSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['Event Tags'], summary="Create a new tag")
class EventTagCreateView(generics.CreateAPIView):
    queryset = EventTag.objects.all()
    serializer_class = EventTagSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


@extend_schema(tags=['Event Tags'], summary="Update a tag")
class EventTagUpdateView(generics.UpdateAPIView):
    queryset = EventTag.objects.all()
    serializer_class = EventTagSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'


@extend_schema(tags=['Event Tags'], summary="Delete a tag")
class EventTagDeleteView(generics.DestroyAPIView):
    queryset = EventTag.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'slug'


# ============== Registration Views ==============

@extend_schema(tags=['Event Registrations'], summary="Register for an event")
class EventRegistrationCreateView(generics.CreateAPIView):
    serializer_class = EventRegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        registration = serializer.save()
        # Here you can send confirmation email
        # send_registration_confirmation_email(registration)


@extend_schema(tags=['Event Registrations'], summary="List registrations (Admin only)")
class EventRegistrationListView(generics.ListAPIView):
    serializer_class = EventRegistrationListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'email', 'confirmation_code']
    ordering = ['-registration_date']

    def get_queryset(self):
        queryset = EventRegistration.objects.select_related('event')
        
        event_slug = self.request.query_params.get('event')
        if event_slug:
            queryset = queryset.filter(event__slug=event_slug)
        
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset


@extend_schema(tags=['Event Registrations'], summary="Get registration details")
class EventRegistrationDetailView(generics.RetrieveAPIView):
    serializer_class = EventRegistrationListSerializer
    permission_classes = [AllowAny]
    lookup_field = 'confirmation_code'

    def get_queryset(self):
        return EventRegistration.objects.select_related('event')


@extend_schema(tags=['Event Registrations'], summary="Cancel registration")
class EventRegistrationCancelView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, confirmation_code):
        registration = get_object_or_404(
            EventRegistration,
            confirmation_code=confirmation_code
        )
        registration.cancel()
        serializer = EventRegistrationListSerializer(registration)
        return Response(serializer.data)


@extend_schema(tags=['Event Registrations'], summary="Confirm registration (Admin)")
class EventRegistrationConfirmView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def post(self, request, pk):
        registration = get_object_or_404(EventRegistration, pk=pk)
        registration.confirm()
        serializer = EventRegistrationListSerializer(registration)
        return Response(serializer.data)


# ============== Gallery Views ==============

@extend_schema(tags=['Event Gallery'], summary="Upload event gallery images")
class EventGalleryCreateView(generics.CreateAPIView):
    queryset = EventGallery.objects.all()
    serializer_class = EventGallerySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        slug = self.kwargs['slug']
        event = get_object_or_404(Event, slug=slug)
        serializer.save(event=event)


@extend_schema(tags=['Event Gallery'], summary="Delete gallery image")
class EventGalleryDeleteView(generics.DestroyAPIView):
    queryset = EventGallery.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]