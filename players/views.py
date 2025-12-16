from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import PlayerProfile
from .forms import PlayerProfileForm, PreviousClubFormSet, StatFormSet, FileFormSet

@login_required
def player_profile_edit(request):
    profile, _ = PlayerProfile.objects.get_or_create(
        user=request.user,
        defaults={"first_name": request.user.first_name or "", "last_name": request.user.last_name or ""}
    )

    if request.method == "POST":
        form = PlayerProfileForm(request.POST, request.FILES, instance=profile)
        clubs_fs = PreviousClubFormSet(request.POST, instance=profile)
        stats_fs = StatFormSet(request.POST, instance=profile)
        files_fs = FileFormSet(request.POST, request.FILES, instance=profile)

        if form.is_valid() and clubs_fs.is_valid() and stats_fs.is_valid() and files_fs.is_valid():
            form.save()
            clubs_fs.save()
            stats_fs.save()
            files_fs.save()
            messages.success(request, "Profil joueur mis à jour ✅")
            return redirect("players:profile_edit")
    else:
        form = PlayerProfileForm(instance=profile)
        clubs_fs = PreviousClubFormSet(instance=profile)
        stats_fs = StatFormSet(instance=profile)
        files_fs = FileFormSet(instance=profile)

    return render(request, "players/profile_edit.html", {
        "form": form, "clubs_fs": clubs_fs, "stats_fs": stats_fs, "files_fs": files_fs, "profile": profile
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
