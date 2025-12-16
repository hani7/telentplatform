from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CoachProfile
from .forms import CoachProfileForm, PreviousClubFormSet, FileFormSet

@login_required
def coach_profile_edit(request):
    profile, _ = CoachProfile.objects.get_or_create(
        user=request.user,
        defaults={"first_name": request.user.first_name or "", "last_name": request.user.last_name or ""}
    )

    if request.method == "POST":
        form = CoachProfileForm(request.POST, request.FILES, instance=profile)
        clubs_fs = PreviousClubFormSet(request.POST, instance=profile)
        files_fs = FileFormSet(request.POST, request.FILES, instance=profile)

        if form.is_valid() and clubs_fs.is_valid() and files_fs.is_valid():
            form.save()
            clubs_fs.save()
            files_fs.save()
            messages.success(request, "Profil entraîneur mis à jour ✅")
            return redirect("coaches:profile_edit")
    else:
        form = CoachProfileForm(instance=profile)
        clubs_fs = PreviousClubFormSet(instance=profile)
        files_fs = FileFormSet(instance=profile)

    return render(request, "coaches/profile_edit.html", {
        "form": form, "clubs_fs": clubs_fs, "files_fs": files_fs, "profile": profile
    })

@login_required
def coach_activate_ad(request):
    profile = get_object_or_404(CoachProfile, user=request.user)
    if not profile.is_complete_for_activation():
        messages.error(request, "Complète les champs obligatoires avant d’activer l’annonce.")
        return redirect("coaches:profile_edit")
    if profile.files.count() == 0:
        messages.error(request, "Ajoute au moins un fichier (CV/Photo/Vidéo) avant activation.")
        return redirect("coaches:profile_edit")

    profile.is_active = True
    profile.save(update_fields=["is_active"])
    messages.success(request, "Annonce activée ✅")
    return redirect("coaches:profile_edit")

@login_required
def coach_deactivate_ad(request):
    profile = get_object_or_404(CoachProfile, user=request.user)
    profile.is_active = False
    profile.save(update_fields=["is_active"])
    messages.info(request, "Annonce désactivée.")
    return redirect("coaches:profile_edit")

def coach_public_profile(request, pk):
    profile = get_object_or_404(CoachProfile, pk=pk, is_active=True)
    return render(request, "coaches/public_profile.html", {"c": profile})
