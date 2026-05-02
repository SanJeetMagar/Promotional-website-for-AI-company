from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .models import ContactMessage


@shared_task
def send_contact_email(contact_message_id):
    try:
        msg = ContactMessage.objects.get(pk=contact_message_id)
    except ContactMessage.DoesNotExist:
        return

    subject = f"New contact message: {msg.subject}"
    admin_email = getattr(settings, "CONTACT_ADMIN_EMAIL", None) or getattr(settings, "DEFAULT_FROM_EMAIL", None)
    
    if not admin_email:
        return

    # Prepare context for template
    context = {
        'first_name': msg.first_name,
        'last_name': msg.last_name,
        'email': msg.email,
        'subject': msg.subject,
        'message': msg.message,
        'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    # Render HTML template
    html_content = render_to_string('contact/contact_email.html', context)
    
    # Create plain text version as fallback
    plain_text_lines = [
        f"From: {msg.first_name} {msg.last_name}",
        f"Email: {msg.email}",
        "",
        f"Subject: {msg.subject}",
        "",
        "Message:",
        msg.message,
    ]
    plain_text = "\n".join(plain_text_lines)
    
    # Create email with both plain text and HTML
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_text,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", admin_email),
        to=[admin_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
