from django.core.mail import send_mail
import string
import random
from django.conf import settings

def price_format(value):
    return f'$ {value:.2f}'

def cart_total_amount(cart):
    return sum([item['amount'] for item in cart.values()])

def cart_totals(cart):
    return sum(
        [
            item.get('quantitative_promotional_price')
            if item.get('quantitative_promotional_price')
            else item.get('quantitative_price')
            for item 
            in cart.values()
        ]
    )

def reset_password(email, name, username):
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    random.shuffle(characters)
    password = []
    for i in range(10):
        password.append(random.choice(characters))

    random.shuffle(password)

    password = "".join(password)

    subject = 'E-commerce - Reset your password'
    #TODO: Fazer com que a mensagem tenha o link pro site
    message = f"Hello {str(name)},\n\nWe've received your request for reseting your password." \
    f"We provided you a temporary password, you can check you informations bellow:\n\n" \
    f"Username: {username}\nTemporary password: {password}\n\n" \
    f"To continue, click on the following link:\nhttp://127.0.0.1:8000/user/change-password/" \
    f"\n\nThank you!"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

    return str(password)