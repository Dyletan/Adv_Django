from rest_framework import serializers
from .models import JobListing, Application, SkillTag

class SkillTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillTag
        fields = ['name']

class JobListingSerializer(serializers.ModelSerializer):
    required_skills = SkillTagSerializer(many=True)

    class Meta:
        model = JobListing
        fields = ['id', 'title', 'company_name', 'location', 'employment_type', 'required_experience', 'required_skills', 'description', 'created_at']

    def create(self, validated_data):
        skills_data = validated_data.pop('required_skills')
        job = JobListing.objects.create(**validated_data)
        for skill_data in skills_data:
            skill, _ = SkillTag.objects.get_or_create(name=skill_data['name'])
            job.required_skills.add(skill)
        return job

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'job_seeker', 'job_listing', 'resume_used', 'feedback_text', 'match_score', 'created_at']
        read_only_fields = ['feedback_text', 'match_score', 'created_at']