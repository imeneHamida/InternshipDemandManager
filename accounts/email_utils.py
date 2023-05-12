# email_utils.py
from django.core.mail import send_mail

def send_account_details_email(user_email, username, password):
    subject = 'Your Account Credentials'
    message = 'Username: {username}\nPassword: {password}'  # Customize the email message as needed
    from_email = 'imene.hamida18@gmail.com'
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)