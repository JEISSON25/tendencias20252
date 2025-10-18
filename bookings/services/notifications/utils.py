from django.template import loader

def render_email_template(template_name: str, context: dict) -> str:
    """Renders a Django template (TXT or HTML) for email content."""

    template = loader.get_template(f'bookings/emails/{template_name}')
    
    return template.render(context)