from rest_framework import serializers
from .models import (
    Event, EventTag, Speaker, EventSpeaker, EventAgenda,
    EventGallery, EventRegistration, EventType, EventStatus
)


class EventTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTag
        fields = ['id', 'name', 'slug', 'color']
        read_only_fields = ['slug']


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = [
            'id', 'name', 'slug', 'title', 'company', 'bio',
            'profile_image', 'email', 'website', 'linkedin_url',
            'twitter_url', 'github_url'
        ]
        read_only_fields = ['slug']


class EventSpeakerSerializer(serializers.ModelSerializer):
    speaker = SpeakerSerializer(read_only=True)
    speaker_id = serializers.PrimaryKeyRelatedField(
        queryset=Speaker.objects.all(),
        source='speaker',
        write_only=True
    )

    class Meta:
        model = EventSpeaker
        fields = ['id', 'speaker', 'speaker_id', 'topic', 'order']


class EventAgendaSerializer(serializers.ModelSerializer):
    speaker = SpeakerSerializer(read_only=True)
    speaker_id = serializers.PrimaryKeyRelatedField(
        queryset=Speaker.objects.all(),
        source='speaker',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = EventAgenda
        fields = [
            'id', 'time', 'title', 'description', 'speaker',
            'speaker_id', 'duration_minutes', 'order'
        ]


class EventGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventGallery
        fields = ['id', 'image', 'caption', 'order']


class EventListSerializer(serializers.ModelSerializer):
    tags = EventTagSerializer(many=True, read_only=True)
    speakers = serializers.SerializerMethodField()
    registered_count = serializers.IntegerField(read_only=True)
    is_registration_open = serializers.BooleanField(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'short_description', 'event_type',
            'status', 'event_date', 'event_time', 'venue_name',
            'is_virtual', 'thumbnail_image', 'is_featured',
            'tags', 'speakers', 'registered_count',
            'is_registration_open', 'available_seats', 'is_free',
            'registration_fee'
        ]

    def get_speakers(self, obj):
        event_speakers = obj.event_speakers.select_related('speaker')[:3]
        return SpeakerSerializer([es.speaker for es in event_speakers], many=True).data


class EventDetailSerializer(serializers.ModelSerializer):
    tags = EventTagSerializer(many=True, read_only=True)
    speakers = EventSpeakerSerializer(source='event_speakers', many=True, read_only=True)
    agenda_items = EventAgendaSerializer(many=True, read_only=True)
    gallery_images = EventGallerySerializer(many=True, read_only=True)
    registered_count = serializers.IntegerField(read_only=True)
    is_registration_open = serializers.BooleanField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)
    related_events = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'event_type', 'status', 'event_date', 'event_time',
            'end_date', 'end_time', 'duration_minutes', 'venue_name',
            'venue_address', 'is_virtual', 'virtual_link', 'map_embed_url',
            'banner_image', 'tags', 'speakers', 'agenda_items',
            'gallery_images', 'max_participants', 'registration_deadline',
            'registration_fee', 'is_free', 'external_registration_url',
            'registered_count', 'is_registration_open', 'is_full',
            'available_seats', 'view_count', 'related_events'
        ]

    def get_related_events(self, obj):
        related = Event.objects.filter(
            tags__in=obj.tags.all(),
            status=EventStatus.UPCOMING
        ).exclude(id=obj.id).distinct()[:3]
        return EventListSerializer(related, many=True).data


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=EventTag.objects.all(),
        required=False
    )
    speakers = EventSpeakerSerializer(source='event_speakers', many=True, required=False)
    agenda_items = EventAgendaSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'event_type', 'status', 'event_date', 'event_time',
            'end_date', 'end_time', 'duration_minutes', 'venue_name',
            'venue_address', 'is_virtual', 'virtual_link', 'map_embed_url',
            'banner_image', 'thumbnail_image', 'tags', 'speakers',
            'agenda_items', 'max_participants', 'registration_deadline',
            'registration_fee', 'is_free', 'external_registration_url',
            'is_featured', 'meta_description', 'meta_keywords'
        ]
        read_only_fields = ['slug']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        speakers_data = validated_data.pop('event_speakers', [])
        agenda_data = validated_data.pop('agenda_items', [])

        event = Event.objects.create(**validated_data)

        if tags_data:
            event.tags.set(tags_data)

        for speaker_data in speakers_data:
            EventSpeaker.objects.create(event=event, **speaker_data)

        for agenda_item in agenda_data:
            EventAgenda.objects.create(event=event, **agenda_item)

        return event

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        speakers_data = validated_data.pop('event_speakers', None)
        agenda_data = validated_data.pop('agenda_items', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data is not None:
            instance.tags.set(tags_data)

        if speakers_data is not None:
            instance.event_speakers.all().delete()
            for speaker_data in speakers_data:
                EventSpeaker.objects.create(event=instance, **speaker_data)

        if agenda_data is not None:
            instance.agenda_items.all().delete()
            for agenda_item in agenda_data:
                EventAgenda.objects.create(event=instance, **agenda_item)

        return instance


class EventRegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_date = serializers.DateField(source='event.event_date', read_only=True)

    class Meta:
        model = EventRegistration
        fields = [
            'id', 'event', 'event_title', 'event_date', 'full_name',
            'email', 'phone', 'company', 'job_title', 'status',
            'registration_date', 'confirmation_code', 'notes'
        ]
        read_only_fields = ['status', 'registration_date', 'confirmation_code']

    
    def validate(self, data):
        # FIXED: Safely grab the event during a partial PATCH request
        event = data.get('event', getattr(self.instance, 'event', None))
        
        if not event:
            return data
            
        # Check if event registration is open
        if not event.is_registration_open:
            raise serializers.ValidationError("Registration is closed for this event.")
        
        # Check if event is full
        if event.is_full:
            raise serializers.ValidationError("This event has reached maximum capacity.")
        
        # Check if email already registered (only check if email is in data)
        email = data.get('email')
        if email and EventRegistration.objects.filter(event=event, email=email).exclude(id=getattr(self.instance, 'id', None)).exists():
            raise serializers.ValidationError("This email is already registered for this event.")
        
        return data

class EventRegistrationListSerializer(serializers.ModelSerializer):
    event = EventListSerializer(read_only=True)

    class Meta:
        model = EventRegistration
        fields = [
            'id', 'event', 'full_name', 'email', 'phone',
            'company', 'job_title', 'status', 'registration_date',
            'confirmation_code', 'attended'
        ]
