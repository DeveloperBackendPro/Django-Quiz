from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_code(code_user, email):
    html_content = render_to_string("verification_code.html", {'code_user':code_user, 'email':email, })
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        f"Проверочный код",
        text_content,
        f"<Online Quiz           >",
        [email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return 'ok'