from rest_framework import serializers
from .models import PlayerProfile, PlayerPreviousClub, PlayerStat, PlayerFile, Nationality


class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = ['id', 'name']


class PlayerPreviousClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerPreviousClub
        fields = ['id', 'club_name', 'country', 'division', 'start_date', 'end_date']


class PlayerStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStat
        fields = ['id', 'season', 'matches', 'goals', 'assists', 'minutes']


class PlayerFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerFile
        fields = ['id', 'file_type', 'file', 'title', 'created_at']


class PlayerProfileSerializer(serializers.ModelSerializer):
    nationality_name = serializers.CharField(source='nationality.name', read_only=True)
    age = serializers.SerializerMethodField()
    previous_clubs = PlayerPreviousClubSerializer(many=True, read_only=True)
    stats = PlayerStatSerializer(many=True, read_only=True)
    files = PlayerFileSerializer(many=True, read_only=True)

    class Meta:
        model = PlayerProfile
        fields = [
            'id', 'first_name', 'last_name', 'birth_date', 'birth_place',
            'gender', 'nationality', 'nationality_name', 'age',
            'is_minor', 'status', 'position', 'foot',
            'height_cm', 'weight_kg',
            'salary_min', 'salary_max', 'player_value',
            'current_club_name', 'current_club_country', 'current_club_division',
            'current_club_start', 'current_club_end', 'contract_end_date',
            'search_objective', 'has_agent_contract', 'agent_full_name',
            'target_club_notes', 'visibility_mode',
            'is_active', 'created_at', 'updated_at',
            'previous_clubs', 'stats', 'files',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'age']

    def get_age(self, obj):
        return obj.age()


class PlayerListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for search lists."""
    nationality_name = serializers.CharField(source='nationality.name', read_only=True)
    age = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = PlayerProfile
        fields = [
            'id', 'first_name', 'last_name', 'age', 'position',
            'nationality_name', 'current_club_name', 'status', 'is_active',
            'profile_photo',
        ]

    def get_age(self, obj):
        return obj.age()

    def get_profile_photo(self, obj):
        photo = obj.files.filter(file_type='PHOTO').first()
        if photo:
            request = self.context.get('request')
            return request.build_absolute_uri(photo.file.url) if request else photo.file.url
        return None
