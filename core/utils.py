from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

def send_order_notification_email(order):
    """
    Send order notification email to the admin
    """
    subject = f'New Order #{order.id} Received - Action Required'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = settings.ORDER_NOTIFICATION_EMAIL

    # Render HTML content
    html_content = render_to_string('email/order_notification.html', {
        'order': order
    })
    text_content = strip_tags(html_content)  # Strip HTML for text version

    # Create email message
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=[to_email]
    )
    
    # Attach HTML content
    email.attach_alternative(html_content, "text/html")
    
    # Send email
    email.send()
