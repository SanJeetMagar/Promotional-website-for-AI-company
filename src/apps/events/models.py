from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from src.apps.common.slug import generate_unique_slug
from src.apps.common.models import BaseModel


class EventType(models.TextChoices):
    WORKSHOP = 'workshop', 'Workshop'
    SEMINAR = 'seminar', 'Seminar'
    MEETUP = 'meetup', 'Meetup'
    CONFERENCE = 'conference', 'Conference'
    WEBINAR = 'webinar', 'Webinar'
    NETWORKING = 'networking', 'Networking'


class EventStatus(models.TextChoices):
    UPCOMING = 'upcoming', 'Upcoming'
    ONGOING = 'ongoing', 'Ongoing'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'


class Event(BaseModel):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField()
    short_description = models.CharField(
        max_length=200,
        help_text="Brief description for event cards"
    )
    
    # Event Details
    event_type = models.CharField(
        max_length=20,
        choices=EventType.choices,
        default=EventType.WORKSHOP,
        db_index=True
    )
    status = models.CharField(
        max_length=20,
        choices=EventStatus.choices,
        default=EventStatus.UPCOMING,
        db_index=True
    )
    
    # Date & Time
    event_date = models.DateField(db_index=True)
    event_time = models.TimeField()
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Event duration in minutes"
    )
    
    # Location
    venue_name = models.CharField(max_length=255)
    venue_address = models.TextField(blank=True)
    is_virtual = models.BooleanField(default=False)
    virtual_link = models.URLField(blank=True, help_text="Meeting/Stream link for virtual events")
    map_embed_url = models.URLField(blank=True, help_text="Google Maps embed URL")
    
    # Media
    banner_image = models.ImageField(upload_to='events/banners/')
    thumbnail_image = models.ImageField(
        upload_to='events/thumbnails/',
        null=True,
        blank=True
    )
    
    # Registration
    max_participants = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )
    registration_deadline = models.DateTimeField(null=True, blank=True)
    registration_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    is_free = models.BooleanField(default=True)
    external_registration_url = models.URLField(
        blank=True,
        help_text="External registration link (e.g., Eventbrite)"
    )
    
    # Additional Info
    tags = models.ManyToManyField('EventTag', related_name='events', blank=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    view_count = models.PositiveIntegerField(default=0)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-event_date', '-event_time']
        indexes = [
            models.Index(fields=['-event_date', 'status']),
            models.Index(fields=['is_featured', 'status']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Event, self.title)
        
        # Auto-set thumbnail from banner if not provided
        if not self.thumbnail_image and self.banner_image:
            self.thumbnail_image = self.banner_image
        
        # Auto-update status based on dates
        self.update_status()
        
        super().save(*args, **kwargs)

    def update_status(self):
        """Automatically update event status based on dates"""
        now = timezone.now()
        event_datetime = timezone.datetime.combine(
            self.event_date,
            self.event_time
        )
        event_datetime = timezone.make_aware(event_datetime)
        
        if self.status != EventStatus.CANCELLED:
            if event_datetime > now:
                self.status = EventStatus.UPCOMING
            elif self.end_date:
                end_datetime = timezone.datetime.combine(
                    self.end_date,
                    self.end_time or self.event_time
                )
                end_datetime = timezone.make_aware(end_datetime)
                if now < end_datetime:
                    self.status = EventStatus.ONGOING
                else:
                    self.status = EventStatus.COMPLETED
            else:
                self.status = EventStatus.COMPLETED

    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    @property
    def is_registration_open(self):
        """Check if registration is still open"""
        if self.status == EventStatus.CANCELLED:
            return False
        
        now = timezone.now()
        
        if self.registration_deadline:
            if now > self.registration_deadline:
                return False
        
        event_datetime = timezone.datetime.combine(
            self.event_date,
            self.event_time
        )
        event_datetime = timezone.make_aware(event_datetime)
        
        return event_datetime > now

    @property
    def is_full(self):
        """Check if event is at max capacity"""
        if not self.max_participants:
            return False
        return self.registrations.filter(status='confirmed').count() >= self.max_participants

    @property
    def available_seats(self):
        """Get number of available seats"""
        if not self.max_participants:
            return None
        confirmed = self.registrations.filter(status='confirmed').count()
        return max(0, self.max_participants - confirmed)

    @property
    def registered_count(self):
        """Get count of confirmed registrations"""
        return self.registrations.filter(status='confirmed').count()


class EventTag(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    color = models.CharField(
        max_length=7,
        default='#3B82F6',
        help_text="Hex color code for tag"
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(EventTag, self.name)
        super().save(*args, **kwargs)


class Speaker(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=255, help_text="Job title or designation")
    company = models.CharField(max_length=255, blank=True)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='events/speakers/')
    
    # Social Links
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Speaker, self.name)
        super().save(*args, **kwargs)


class EventSpeaker(BaseModel):
    """Through model for Event-Speaker relationship"""
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_speakers'
    )
    speaker = models.ForeignKey(
        Speaker,
        on_delete=models.CASCADE,
        related_name='speaker_events'
    )
    topic = models.CharField(
        max_length=255,
        blank=True,
        help_text="Specific topic this speaker will cover"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        unique_together = ['event', 'speaker']

    def __str__(self):
        return f"{self.speaker.name} at {self.event.title}"


class EventAgenda(BaseModel):
    """Event schedule/agenda items"""
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='agenda_items'
    )
    time = models.TimeField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    speaker = models.ForeignKey(
        Speaker,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='agenda_items'
    )
    duration_minutes = models.PositiveIntegerField(default=30)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'time']

    def __str__(self):
        return f"{self.event.title} - {self.title}"


class EventGallery(BaseModel):
    """Gallery images for events"""
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(upload_to='events/gallery/')
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name_plural = 'Event Galleries'

    def __str__(self):
        return f"Gallery image for {self.event.title}"


class RegistrationStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    CANCELLED = 'cancelled', 'Cancelled'
    ATTENDED = 'attended', 'Attended'


class EventRegistration(BaseModel):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    
    # Participant Info
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    
    # Registration Details
    status = models.CharField(
        max_length=20,
        choices=RegistrationStatus.choices,
        default=RegistrationStatus.PENDING,
        db_index=True
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    confirmation_code = models.CharField(max_length=20, unique=True, blank=True)
    
    # Additional
    notes = models.TextField(blank=True, help_text="Special requests or notes")
    attended = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MinValueValidator(5)]
    )

    class Meta:
        ordering = ['-registration_date']
        unique_together = ['event', 'email']

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"

    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            import uuid
            self.confirmation_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def confirm(self):
        """Confirm the registration"""
        self.status = RegistrationStatus.CONFIRMED
        self.save()

    def cancel(self):
        """Cancel the registration"""
        self.status = RegistrationStatus.CANCELLED
        self.save()
