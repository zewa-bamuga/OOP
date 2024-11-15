import smtplib
from email.message import EmailMessage


class EmailSender:
    def __init__(
            self,
            smtp_server: str = "smtp.yandex.ru",
            port: int = 465,
            email_address: str = "tikhonov.igor2028@yandex.ru",
            email_password: str = "abqiulywjvibrefg"
    ):
        self.smtp_server = smtp_server
        self.port = port
        self.email_address = email_address
        self.email_password = email_password

    async def send_verification_email(self, recipient_email: str, code: int):
        msg = EmailMessage()
        msg['Subject'] = "Подтверждение почты"
        msg['From'] = self.email_address
        msg['To'] = recipient_email

        html_content = f"""\ 
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #003366; background-color: #486DB5;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #ffffff;">
                <h2 style="color: #FFD700;">Сброс пароля</h2>
                <p>Здравствуйте,</p>
                <p>Подтверждение почты на платформе Отдела Образовательных Программ.</p>
                <p>Код для подтверждения почты:</p>
                <p style="font-size: 18px; font-weight: bold; color: #FFD700;">{code}</p>
                <p>Если вы не запрашивали подтверждения почты, проигнорируйте это письмо.</p>
                <p>С уважением,<br>Ваш Отдел Образовательных Программ</p>
                <p style="margin-top: 20px; color: #777; font-size: 12px;">Если у вас возникли какие-либо вопросы, пожалуйста, свяжитесь с нами.</p>
            </div>
        </body>
        </html>
        """

        msg.set_content(
            f"Здравствуйте,\n\nВы запросили сброс пароля на платформе Отдела Образовательных Программ.\n\nКод для сброса пароля: {code}\n\nЕсли вы не запрашивали сброс пароля, проигнорируйте это письмо.\n\nС уважением,\nВаш Отдел Образовательных Программ"
        )
        msg.add_alternative(html_content, subtype='html')

        with smtplib.SMTP_SSL(self.smtp_server, self.port) as smtp:
            smtp.login(self.email_address, self.email_password)
            smtp.send_message(msg)

    async def send_first_registration(self, user_email: str):
        msg = EmailMessage()
        msg['Subject'] = "Подтверждение регистрации"
        msg['From'] = self.email_address
        msg['To'] = user_email

        html_content = f"""\
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #003366; background-color: #486DB5;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #ffffff;">
                <h2 style="color: #FFD700;">Подтверждение регистрации</h2>
                <p>Дорогой пользователь платформы Отдела Образовательных Программ!</p>
                <p>Мы рады приветствовать тебя!</p>
                <p>Твой Отдел Образовательных Программ <span style="color: #FFD700;">&lt;3</span></p>
                <p style="margin-top: 20px; color: #777; font-size: 12px;">Если у вас возникли какие-либо вопросы, пожалуйста, свяжитесь с нами.</p>
            </div>
        </body>
        </html>
        """

        msg.set_content(
            "Дорогой пользователь платформы Отдела Образовательных Программ! Мы рады приветствовать тебя! Твой Отдел Образовательных Программ <3"
        )
        msg.add_alternative(html_content, subtype='html')

        with smtplib.SMTP_SSL(self.smtp_server, self.port) as smtp:
            smtp.login(self.email_address, self.email_password)
            smtp.send_message(msg)

    async def send_password_reset_email(self, recipient_email: str, code: str):
        msg = EmailMessage()
        msg['Subject'] = "Сброс пароля"
        msg['From'] = self.email_address
        msg['To'] = recipient_email

        html_content = f"""\
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #003366; background-color: #486DB5;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #ffffff;">
                <h2 style="color: #FFD700;">Сброс пароля</h2>
                <p>Здравствуйте,</p>
                <p>Вы запросили сброс пароля на платформе Отдела Образовательных Программ.</p>
                <p>Код для сброса пароля:</p>
                <p style="font-size: 18px; font-weight: bold; color: #FFD700;">{code}</p>
                <p>Если вы не запрашивали сброс пароля, проигнорируйте это письмо.</p>
                <p>С уважением,<br>Ваш Отдел Образовательных Программ</p>
                <p style="margin-top: 20px; color: #777; font-size: 12px;">Если у вас возникли какие-либо вопросы, пожалуйста, свяжитесь с нами.</p>
            </div>
        </body>
        </html>
        """

        msg.set_content(
            f"Здравствуйте,\n\nВы запросили сброс пароля на платформе Отдела Образовательных Программ.\n\nКод для сброса пароля: {code}\n\nЕсли вы не запрашивали сброс пароля, проигнорируйте это письмо.\n\nС уважением,\nВаш Отдел Образовательных Программ"
        )
        msg.add_alternative(html_content, subtype='html')

        with smtplib.SMTP_SSL(self.smtp_server, self.port) as smtp:
            smtp.login(self.email_address, self.email_password)
            smtp.send_message(msg)
