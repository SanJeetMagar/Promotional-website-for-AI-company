from .models import CV, JobPosting
from rest_framework import serializers


class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = ['id', 'full_name', 'email', 'phone_number', 'years_of_experience', 'linkedin_profile', 'github_profile', 'portfolio_link', 'resume_file', 'short_note', 'job']  # add job here
        extra_kwargs = {
            'job': {'read_only': True}
        }
    def validate(self, data):
        if data.get('job') is None:
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