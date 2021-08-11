import threading
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from random import randint


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, host_email, recipient_list):
        self.host_email = host_email
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(
            self.subject, self.html_content, self.host_email, self.recipient_list)
        msg.content_subtype = "html"
        msg.send()


def sendMail(email, Type="signup"):
    if Type == "signup":
        otp_code = randint(1000, 9999)
        message = render_to_string("otp.html", {"otp": otp_code})
        subject = "E-mail Verification"
        send_from = settings.EMAIL_HOST_USER
        send_to = [email, ]
        try:
            EmailThread(subject, message, send_from, send_to).start()
        except:
            pass
        return otp_code
