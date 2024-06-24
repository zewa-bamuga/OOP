import smtplib
from email.message import EmailMessage

from pydantic import EmailStr

from app.domain.common.models import User, PasswordResetCode


async def send_hello(user: User):
    email_address = "tikhonov.igor2028@yandex.ru"
    email_password = "abqiulywjvibrefg"

    msg = EmailMessage()
    msg['Subject'] = "Подтверждение регистрации"
    msg['From'] = email_address
    msg['To'] = user.email
    msg.set_content(
        f"""\
        Вы успешно зарегистрировались на платформе Путеводитель по необычным местам!
        """
    )

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


async def send_password_reset_email(email: str, code: str):
    email_address = "tikhonov.igor2028@yandex.ru"
    email_password = "abqiulywjvibrefg"
    # code = PasswordResetCode.generate_code()

    msg = EmailMessage()
    msg['Subject'] = "Сброс пароля"
    msg['From'] = email_address
    msg['To'] = email
    msg.set_content(
        f"""\
        Здравствуйте,

        Вы запросили сброс пароля на платформе Путеводитель по необычным местам.

        Код для сброса пароля: {code}

        Если вы не запрашивали сброс пароля, проигнорируйте это письмо.

        С уважением,
        Ваша команда Путеводитель по необычным местам
        """
    )

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
