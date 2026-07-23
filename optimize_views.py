import re

filepath = 'players/views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Optimize player_public_profile
old_public = 'profile = get_object_or_404(PlayerProfile, pk=pk)'
new_public = 'profile = get_object_or_404(PlayerProfile.objects.select_related("nationality").prefetch_related("previous_clubs", "stats", "files"), pk=pk)'
content = content.replace(old_public, new_public)

# Optimize profile_complete
old_complete = '''    profile, _ = PlayerProfile.objects.get_or_create(
        user=request.user,
        defaults={"first_name": request.user.first_name or "", "last_name": request.user.last_name or ""}
    )'''
new_complete = '''    # Fetch with select_related and prefetch_related for performance
    try:
        profile = PlayerProfile.objects.select_related('nationality').prefetch_related(
            'previous_clubs', 'stats', 'files'
        ).get(user=request.user)
    except PlayerProfile.DoesNotExist:
        profile = PlayerProfile.objects.create(
            user=request.user,
            first_name=request.user.first_name or "",
            last_name=request.user.last_name or ""
        )'''
content = content.replace(old_complete, new_complete)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
