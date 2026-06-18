from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings

from .models import User, OTPCode
from .serializers import UserSerializer, RegisterSerializer


def _send_otp_email(user, otp_code):
    """Send OTP code to user's email via Gmail SMTP."""
    subject = "🔐 Votre code de vérification FOOTOP"
    message = (
        f"Bonjour {user.first_name or user.username},\n\n"
        f"Votre code de vérification FOOTOP est :\n\n"
        f"    {otp_code}\n\n"
        f"Ce code expire dans 10 minutes.\n"
        f"Si vous n'avez pas créé de compte, ignorez cet email.\n\n"
        f"— L'équipe FOOTOP"
    )
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        # Log but don't crash the registration
        print(f"[OTP EMAIL ERROR] Failed to send to {user.email}: {e}")


# ─── Auth ───────────────────────────────────────────────────────────

class APILoginView(APIView):
    """POST /api/auth/token/  →  {access, refresh, user}"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'detail': 'Identifiants incorrects.'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
        })


class APIRegisterView(generics.CreateAPIView):
    """POST /api/auth/register/  →  creates user + sends OTP"""
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Generate OTP and send via email
        otp = OTPCode.generate_for(user)
        if user.email:
            _send_otp_email(user, otp.code)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
            'otp_hint': otp.code,  # keep for dev/debug; remove in production
        }, status=status.HTTP_201_CREATED)


class APIMeView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/auth/me/  →  current user info"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class APIOTPVerifyView(APIView):
    """POST /api/auth/otp/verify/  →  {code}"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = str(request.data.get('code', '')).strip()
        otp = OTPCode.objects.filter(
            user=request.user, code=code, is_used=False
        ).order_by('-created_at').first()
        if not otp or otp.is_expired():
            return Response({'detail': 'Code invalide ou expiré.'}, status=status.HTTP_400_BAD_REQUEST)
        otp.is_used = True
        otp.save()
        request.user.is_verified = True
        request.user.save(update_fields=['is_verified'])
        return Response({'detail': 'Compte vérifié avec succès.'})


class APIOTPResendView(APIView):
    """POST /api/auth/otp/resend/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        otp = OTPCode.generate_for(request.user)
        if request.user.email:
            _send_otp_email(request.user, otp.code)
        return Response({'detail': 'OTP renvoyé.', 'otp_hint': otp.code})
