from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import PlayerProfile
from .forms import PlayerProfileForm, PreviousClubFormSet, SeasonStatFormSet, FileFormSet

@login_required
def player_profile_edit(request):
    profile, _ = PlayerProfile.objects.get_or_create(
        user=request.user,
        defaults={"first_name": request.user.first_name or "", "last_name": request.user.last_name or ""}
    )

    if request.method == "POST":
        form = PlayerProfileForm(request.POST, request.FILES, instance=profile)
        clubs_fs = PreviousClubFormSet(request.POST, instance=profile)
        files_fs = FileFormSet(request.POST, request.FILES, instance=profile)

        if form.is_valid() and clubs_fs.is_valid() and files_fs.is_valid():
            form.save()
            clubs_fs.save()  # saves all clubs, giving new ones their PKs
            # After save, clubs_fs.forms[i].instance.pk is available for all
            for i, club_form in enumerate(clubs_fs.forms):
                if club_form.cleaned_data.get('DELETE'):
                    continue
                club_instance = club_form.instance
                if not club_instance.pk:
                    continue
                prefix = f"seasons_form_{i}"
                season_fs = SeasonStatFormSet(request.POST, instance=club_instance, prefix=prefix)
                if season_fs.is_valid():
                    seasons = season_fs.save(commit=False)
                    for s in seasons:
                        s.player = profile
                        s.club = club_instance
                        s.save()
                    for obj in season_fs.deleted_objects:
                        obj.delete()
            files_fs.save()
            step = request.POST.get('_current_step', '1')
            messages.success(request, "Profil joueur mis à jour ✅")
            from django.http import HttpResponseRedirect
            from django.urls import reverse
            return HttpResponseRedirect(reverse("players:profile_edit") + f"?step={step}")
    else:
        form = PlayerProfileForm(instance=profile)
        clubs_fs = PreviousClubFormSet(instance=profile)
        files_fs = FileFormSet(instance=profile)

    # Build season formsets for ALL clubs (saved AND new), using index as prefix
    clubs_with_seasons = []
    for i, club_form in enumerate(clubs_fs.forms):
        club_instance = club_form.instance
        prefix = f"seasons_form_{i}"
        if club_instance.pk:
            season_fs = SeasonStatFormSet(instance=club_instance, prefix=prefix)
        else:
            # New club: show an empty season formset so user can fill it now
            season_fs = SeasonStatFormSet(prefix=prefix)
        clubs_with_seasons.append((club_form, season_fs))

    return render(request, "players/profile_edit.html", {
        "form": form,
        "clubs_fs": clubs_fs,
        "clubs_with_seasons": clubs_with_seasons,
        "files_fs": files_fs,
        "profile": profile
    })

@login_required
def player_activate_ad(request):
    profile = get_object_or_404(PlayerProfile, user=request.user)
    if not profile.is_complete_for_activation():
        messages.error(request, "Complète les champs obligatoires avant d’activer l’annonce.")
        return redirect("players:profile_edit")
    if profile.files.count() == 0:
        messages.error(request, "Ajoute au moins un fichier (CV/Photo/Vidéo) avant activation.")
        return redirect("players:profile_edit")

    profile.is_active = True
    profile.save(update_fields=["is_active"])
    messages.success(request, "Annonce activée ✅")
    return redirect("players:profile_edit")

@login_required
def player_deactivate_ad(request):
    profile = get_object_or_404(PlayerProfile, user=request.user)
    profile.is_active = False
    profile.save(update_fields=["is_active"])
    messages.info(request, "Annonce désactivée.")
    return redirect("players:profile_edit")

def player_public_profile(request, pk):
    profile = get_object_or_404(PlayerProfile, pk=pk, is_active=True)
    return render(request, "players/public_profile.html", {"p": profile})

@login_required
def profile_complete(request):
    """Show full player profile with all saved information"""
    profile, _ = PlayerProfile.objects.get_or_create(
        user=request.user,
        defaults={"first_name": request.user.first_name or "", "last_name": request.user.last_name or ""}
    )

    # Completion calculations
    personal_fields = ['first_name', 'last_name', 'birth_date', 'nationality', 'gender']
    personal_filled = sum(1 for f in personal_fields if getattr(profile, f, None))
    personal_progress = int((personal_filled / len(personal_fields)) * 100)

    football_fields = ['position', 'foot', 'current_club_name', 'status']
    football_filled = sum(1 for f in football_fields if getattr(profile, f, None))
    football_progress = int((football_filled / len(football_fields)) * 100)

    clubs_progress = min(profile.previous_clubs.count() * 50, 100)
    stats_progress = min(profile.stats.count() * 50, 100)
    files_progress = min(profile.files.count() * 25, 100)

    completion_percentage = int((personal_progress + football_progress + clubs_progress + files_progress) / 4)

    context = {
        'profile': profile,
        'previous_clubs': profile.previous_clubs.all(),
        'stats': profile.stats.all(),
        'files': profile.files.all(),
        'completion_percentage': completion_percentage,
        'personal_progress': personal_progress,
        'football_progress': football_progress,
        'clubs_progress': clubs_progress,
        'stats_progress': stats_progress,
        'files_progress': files_progress,
    }
    return render(request, 'players/profile_complete.html', context)
