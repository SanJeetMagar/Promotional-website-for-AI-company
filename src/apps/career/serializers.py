from .models import CV, JobPosting
from rest_framework import serializers


class CVSerializer(serializers.ModelSerializer):
    job = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CV
        fields = ['id', 'full_name', 'email', 'phone_number', 'years_of_experience', 'linkedin_profile', 'github_profile', 'portfolio_link', 'resume_file', 'short_note', 'job']  # add job here
        extra_kwargs = {
            'job': {'read_only': True}
        }
    def validate(self, data):
        slug = self.context['view'].kwargs.get('slug')
        
        if slug:  # applying to specific job
            job = JobPosting.objects.filter(slug=slug, status='published').first()
            if job and CV.objects.filter(email=data['email'], job=job).exists():
                raise serializers.ValidationError(
                    "You have already applied to this job."
                )
        else:  # general CV
            if CV.objects.filter(email=data['email'], job=None).exists():
                raise serializers.ValidationError(
                    "You have already submitted a general CV."
                )
        
        return data
class JobPostingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ['id', 'title', 'slug', 'location', 'tags', 'employment_type', 'work_arrangement', 'status']
class JobPostingDetailSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    class Meta:
        model = JobPosting
        fields = ['id', 'title', 'slug', 'location', 'tags', 'description', 'deadline', 'seat_openings', 'required_skills', 'benefits', 'how_to_apply', 'employment_type', 'work_arrangement', 'status']
