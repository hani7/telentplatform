from django.core.mail import send_mail
from django.conf import settings
import threading


def send_otp_email(user, otp_code):
    """
    Send an OTP verification code to the user's email address.
    Shared between the web views (accounts/views.py) and the API views (accounts/api_views.py).
    """
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
        def send_email_task():
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"[OTP EMAIL ERROR] Failed to send to {user.email}: {e}")
        
        # Run email sending in a background thread to prevent blocking
        threading.Thread(target=send_email_task).start()
    except Exception as e:
        # Log but don't crash the registration flow
        print(f"[OTP EMAIL ERROR] Failed to send to {user.email}: {e}")
