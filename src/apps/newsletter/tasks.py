from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Newsletter


@shared_task
def send_welcome_email(email):
    """Send welcome email to new newsletter subscriber"""
    try:
        subject = "Welcome to AI website Newsletter!"
        message = f"""
        Hello,
        
        Thank you for subscribing to our newsletter. We're excited to share 
        updates, insights, and exclusive content with you.
        
        Best regards,
        AI website Team
        """
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return f"Welcome email sent to {email}"
    except Exception as e:
        return f"Failed to send email to {email}: {str(e)}"


@shared_task
def send_bulk_newsletter(subject, message):
    """Send newsletter to all subscribers"""
    subscribers = Newsletter.objects.all()
    email_list = [subscriber.email for subscriber in subscribers]
    
    if not email_list:
        return "No subscribers found"
    
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            email_list,
            fail_silently=False,
        )
        return f"Newsletter sent to {len(email_list)} subscribers"
    except Exception as e:
        return f"Failed to send newsletter: {str(e)}"


@shared_task
def test_celery_task():
    """Simple test task to verify Celery is working"""
    return "Celery is working properly!"
