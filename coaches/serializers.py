from rest_framework import serializers
from .models import CoachProfile, CoachPreviousClub, CoachFile


class CoachPreviousClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachPreviousClub
        fields = ['id', 'club_name', 'country', 'division', 'start_date', 'end_date']


class CoachFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachFile
        fields = ['id', 'file_type', 'file', 'title', 'created_at']


class CoachProfileSerializer(serializers.ModelSerializer):
    nationality_name = serializers.CharField(source='nationality.name', read_only=True)
    age = serializers.SerializerMethodField()
    previous_clubs = CoachPreviousClubSerializer(many=True, read_only=True)
    files = CoachFileSerializer(many=True, read_only=True)

    class Meta:
        model = CoachProfile
        fields = [
            'id', 'first_name', 'last_name', 'birth_date', 'birth_place',
            'gender', 'nationality', 'nationality_name', 'age',
            'diplomas_certificates', 'status', 'achievements',
            'salary_min', 'salary_max',
            'current_club_name', 'current_club_country', 'current_club_division',
            'current_club_start', 'current_club_end', 'contract_end_date',
            'has_agent_contract', 'agent_full_name',
            'search_objective', 'target_club_notes', 'visibility_mode',
            'is_active', 'created_at', 'updated_at',
            'previous_clubs', 'files',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'age']

    def get_age(self, obj):
        return obj.age()
