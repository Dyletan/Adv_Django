from rest_framework import serializers
from .models import JobListing, Application, SkillTag
from accounts.models import User

class SkillTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillTag
        fields = ['id', 'name']

class JobListingSerializer(serializers.ModelSerializer):
    required_skills = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True
    )
    required_skills_data = SkillTagSerializer(many=True, read_only=True, source='required_skills')

    class Meta:
        model = JobListing
        fields = ['id', 'recruiter', 'title', 'company_name', 'location', 'employment_type', 
                  'required_experience', 'required_skills', 'required_skills_data', 'description', 'created_at']
        read_only_fields = ['id', 'recruiter', 'created_at', 'required_skills_data']

    def validate_required_skills(self, value):
        if not value:
            raise serializers.ValidationError("At least one skill is required.")
        if len(set(value)) != len(value):
            raise serializers.ValidationError("Duplicate skills are not allowed.")
        for skill in value:
            if len(skill.strip()) == 0:
                raise serializers.ValidationError("Skills cannot be empty.")
        return value

    def create(self, validated_data):
        skills_data = validated_data.pop('required_skills')
        job = JobListing.objects.create(**validated_data)
        for skill_name in skills_data:
            skill_name = skill_name.strip()
            skill, _ = SkillTag.objects.get_or_create(name=skill_name[:50])
            job.required_skills.add(skill)
        return job

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'job_seeker', 'job_listing', 'resume_used', 'feedback_text', 'match_score', 'created_at']
        read_only_fields = ['feedback_text', 'match_score', 'created_at']