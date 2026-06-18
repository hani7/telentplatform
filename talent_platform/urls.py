from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.shortcuts import redirect as _redirect
from django.http import FileResponse, HttpResponse
from rest_framework_simplejwt.views import TokenRefreshView
import os
# API Views
from accounts.api_views import APILoginView, APIRegisterView, APIMeView, APIOTPVerifyView, APIOTPResendView
from players.api_views import APIPlayerProfileView, APIPlayerPublicView, APIPlayersListView
from coaches.api_views import APICoachProfileView
from offers.api_views import APIMyOffersView, APIMySuggestionsView, APISendOfferView, APIOfferRespondView

def download_apk_page(request):
    """Styled download page for the FOOTOP APK."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FOOTOP – Download App</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a1a10; font-family: 'Segoe UI', sans-serif; min-height: 100vh;
         display: flex; align-items: center; justify-content: center; }
  .card { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
          border-radius: 24px; padding: 48px 40px; text-align: center; max-width: 380px; margin: 24px; }
  .logo { color: #4CAF50; font-size: 32px; font-weight: 900; letter-spacing: 4px; margin-bottom: 8px; }
  .tagline { color: rgba(255,255,255,0.5); font-size: 14px; margin-bottom: 40px; }
  .icon { font-size: 72px; margin-bottom: 24px; }
  h1 { color: #fff; font-size: 22px; font-weight: 700; margin-bottom: 12px; }
  p { color: rgba(255,255,255,0.6); font-size: 14px; line-height: 1.6; margin-bottom: 32px; }
  .btn { display: inline-block; background: #FFD700; color: #000; font-weight: 700;
         font-size: 16px; padding: 16px 40px; border-radius: 50px; text-decoration: none;
         transition: transform 0.2s, box-shadow 0.2s; }
  .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(255,215,0,0.3); }
  .note { color: rgba(255,255,255,0.35); font-size: 12px; margin-top: 20px; }
  .steps { text-align: left; background: rgba(0,0,0,0.3); border-radius: 12px;
           padding: 16px 20px; margin-bottom: 28px; }
  .steps li { color: rgba(255,255,255,0.65); font-size: 13px; margin-bottom: 6px; padding-left: 4px; }
  .steps li::marker { color: #4CAF50; }
</style>
</head>
<body>
<div class="card">
  <div class="logo">FOOTOP</div>
  <div class="tagline">Football Talent Platform</div>
  <div class="icon">⚽</div>
  <h1>Download the App</h1>
  <p>Connect players, coaches, clubs and agents on one platform.</p>
  <ol class="steps">
    <li>Tap the button below to download</li>
    <li>Open the downloaded APK file</li>
    <li>Allow installation from unknown sources if prompted</li>
    <li>Install and enjoy!</li>
  </ol>
  <a class="btn" href="/download/apk/">⬇ Download APK</a>
  <div class="note">Android only &nbsp;•&nbsp; v1.0 &nbsp;•&nbsp; ~58 MB</div>
</div>
</body>
</html>"""
    return HttpResponse(html)


def serve_apk(request):
    """Serve the APK file as a download."""
    apk_path = os.path.join(settings.MEDIA_ROOT, 'footop.apk')
    if not os.path.exists(apk_path):
        return HttpResponse('APK not found.', status=404)
    response = FileResponse(open(apk_path, 'rb'), content_type='application/vnd.android.package-archive')
    response['Content-Disposition'] = 'attachment; filename="FOOTOP.apk"'
    return response


def home_view(request):
    if request.user.is_authenticated:
        role = getattr(request.user, "role", None)
        if role == "AGENT":
            return _redirect("agents:dashboard")
        if role == "CLUB":
            return _redirect("clubs:dashboard")
    from django.shortcuts import render
    return render(request, "home.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),

    # ── APK Download (public) ──
    path("download/", download_apk_page, name="download_page"),
    path("download/apk/", serve_apk, name="serve_apk"),

    path("service-worker.js", TemplateView.as_view(
        template_name="service-worker.js",
        content_type="application/javascript",
    ), name="service_worker"),

    # ── Web routes ──
    path("accounts/", include("accounts.urls")),
    path("players/", include("players.urls")),
    path("coaches/", include("coaches.urls")),
    path("search/", include("search.urls")),
    path("offers/", include("offers.urls")),
    path("agents/", include("agents.urls")),
    path("clubs/", include("clubs.urls")),

    # ── REST API ──
    path("api/auth/token/",       APILoginView.as_view(),      name="api_login"),
    path("api/auth/token/refresh/",TokenRefreshView.as_view(), name="api_token_refresh"),
    path("api/auth/register/",    APIRegisterView.as_view(),   name="api_register"),
    path("api/auth/me/",          APIMeView.as_view(),         name="api_me"),
    path("api/auth/otp/verify/",  APIOTPVerifyView.as_view(),  name="api_otp_verify"),
    path("api/auth/otp/resend/",  APIOTPResendView.as_view(),  name="api_otp_resend"),

    path("api/players/profile/",  APIPlayerProfileView.as_view(), name="api_player_profile"),
    path("api/players/list/",     APIPlayersListView.as_view(),   name="api_players_list"),
    path("api/players/<int:pk>/", APIPlayerPublicView.as_view(),  name="api_player_detail"),

    path("api/coaches/profile/",  APICoachProfileView.as_view(),  name="api_coach_profile"),

    path("api/offers/my/",        APIMyOffersView.as_view(),       name="api_my_offers"),
    path("api/offers/suggestions/",APIMySuggestionsView.as_view(), name="api_suggestions"),
    path("api/offers/send/",      APISendOfferView.as_view(),      name="api_send_offer"),
    path("api/offers/<int:pk>/respond/", APIOfferRespondView.as_view(), name="api_offer_respond"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
