from django.db import models
from src.apps.common.models import BaseModel
from django.utils import timezone
from src.apps.common.slug import generate_unique_slug
class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
class EmploymentType(models.TextChoices):
    FULL_TIME = 'Full-time', 'Full-time'
    PART_TIME = 'Part-time', 'Part-time'
    CONTRACT = 'Contract', 'Contract'
    TEMPORARY = 'Temporary', 'Temporary'
    INTERN = 'Intern', 'Intern'

class JobStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    CLOSED = 'closed', 'Closed'

class WorkArrangement(models.TextChoices):
    ON_SITE = 'On-site', 'On-site'
    REMOTE = 'Remote', 'Remote'
    HYBRID = 'Hybrid', 'Hybrid'
class JobPosting(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    seat_openings = models.PositiveIntegerField(default=1)
    required_skills = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    how_to_apply = models.TextField(blank=True)
    employment_type = models.CharField(max_length=50, blank=True, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    work_arrangement = models.CharField(max_length=50, blank=True, choices=WorkArrangement.choices, default=WorkArrangement.ON_SITE)
    status = models.CharField(max_length=50, choices=JobStatus.choices, default=JobStatus.DRAFT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(JobPosting, self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class CV(BaseModel):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=False)
    phone_number = models.CharField(max_length=20, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    portfolio_link = models.URLField(blank=True)
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    short_note = models.TextField(blank=True)
    job = models.ForeignKey(
        JobPosting, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,  # optional - can submit without specific job
        related_name='applications'
    )
        
    def __str__(self):
        return self.full_name
    