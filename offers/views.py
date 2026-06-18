from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from accounts.models import User
from .models import Offer


# ── Helpers ─────────────────────────────────────────────────────────────────

def _require_role(request, *roles):
    """Return True if user has one of the given roles, else redirect home."""
    if request.user.role not in roles:
        messages.error(request, "Accès refusé.")
        return False
    return True


# ── Player / Coach views ─────────────────────────────────────────────────────

@login_required
def my_offers(request):
    """Joueur / Entraîneur: list of received offers."""
    if not _require_role(request, User.Role.PLAYER, User.Role.COACH):
        return redirect("home")

    offers = Offer.objects.filter(recipient=request.user).select_related("sender")
    return render(request, "offers/my_offers.html", {"offers": offers})


@login_required
@require_POST
def respond_offer(request, pk):
    """Joueur / Entraîneur: accept or decline an offer."""
    if not _require_role(request, User.Role.PLAYER, User.Role.COACH):
        return redirect("home")

    offer = get_object_or_404(Offer, pk=pk, recipient=request.user)
    action = request.POST.get("action")

    if action == "accept" and offer.status == Offer.Status.PENDING:
        offer.status = Offer.Status.ACCEPTED
        offer.save()
        messages.success(request, "Offre acceptée ✅")
    elif action == "decline" and offer.status == Offer.Status.PENDING:
        offer.status = Offer.Status.DECLINED
        offer.save()
        messages.info(request, "Offre refusée.")
    else:
        messages.warning(request, "Action invalide.")

    return redirect("offers:my_offers")


# ── Agent / Club views ───────────────────────────────────────────────────────

@login_required
def my_suggestions(request):
    """Agent / Club: list of sent offers/suggestions."""
    if not _require_role(request, User.Role.AGENT, User.Role.CLUB):
        return redirect("home")

    sent = Offer.objects.filter(sender=request.user).select_related("recipient")
    return render(request, "offers/my_suggestions.html", {"sent_offers": sent})


@login_required
def send_offer(request):
    """Agent / Club: compose and send a new offer."""
    if not _require_role(request, User.Role.AGENT, User.Role.CLUB):
        return redirect("home")

    # Build recipient list: active players + coaches
    players = User.objects.filter(role=User.Role.PLAYER, is_verified=True).order_by("username")
    coaches = User.objects.filter(role=User.Role.COACH,  is_verified=True).order_by("username")

    error = None
    if request.method == "POST":
        recipient_id = request.POST.get("recipient_id")
        title        = request.POST.get("title", "").strip()
        message      = request.POST.get("message", "").strip()

        if not recipient_id or not title or not message:
            error = "Tous les champs sont obligatoires."
        else:
            recipient = get_object_or_404(User, pk=recipient_id)
            if recipient.role not in (User.Role.PLAYER, User.Role.COACH):
                error = "Destinataire invalide."
            else:
                Offer.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    title=title,
                    message=message,
                )
                messages.success(request, f"Offre envoyée à {recipient.get_full_name() or recipient.username} ✅")
                return redirect("offers:my_suggestions")

    return render(request, "offers/send_offer.html", {
        "players": players,
        "coaches": coaches,
        "error": error,
    })
