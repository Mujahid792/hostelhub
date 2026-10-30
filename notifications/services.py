from django.conf import settings
from .models import SMSLog

def send_sms(to, body):
    """Send SMS via Twilio. Falls back to logging if Twilio isn't configured."""
    sid = settings.TWILIO_ACCOUNT_SID
    token = settings.TWILIO_AUTH_TOKEN
    from_number = settings.TWILIO_PHONE_NUMBER

    if not (sid and token and from_number):
        # Twilio not configured - log and return
        log = SMSLog.objects.create(to_number=to, body=body, status='failed',
                                    error_message='Twilio not configured')
        return log

    try:
        from twilio.rest import Client
        client = Client(sid, token)
        msg = client.messages.create(body=body, from_=from_number, to=to)
        return SMSLog.objects.create(to_number=to, body=body, status='sent')
    except Exception as e:
        return SMSLog.objects.create(to_number=to, body=body, status='failed',
                                     error_message=str(e))