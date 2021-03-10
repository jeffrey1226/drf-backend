import traceback

from django.core.mail import EmailMessage


def send_reset_email(to, name, url):
    message = "Hi {},\nYou can reset password by clicking follow link.\n{}".format(name, url)
    email = EmailMessage(
        subject='Reset Password',
        body=message,
        to=[to],
    )

    try:
        email.send(fail_silently=False)
        return True
    except Exception:
        print(traceback.format_exc())
        return False
