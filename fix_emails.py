import os

filepath = 'players/views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('import uuid', 'import uuid\nimport threading')

old_send = '''                        send_mail(
                            "Consentement parental requis - Talent Platform",
                            msg,
                            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@talentplatform.com',
                            [profile.parent_email],
                            fail_silently=True,
                            html_message=html_msg
                        )'''

new_send = '''                        def send_consent_email_task():
                            try:
                                send_mail(
                                    "Consentement parental requis - Talent Platform",
                                    msg,
                                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@talentplatform.com',
                                    [profile.parent_email],
                                    fail_silently=True,
                                    html_message=html_msg
                                )
                            except Exception as e:
                                print(f"[CONSENT EMAIL ERROR] {e}")
                        
                        threading.Thread(target=send_consent_email_task).start()'''

content = content.replace(old_send, new_send)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
