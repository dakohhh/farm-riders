from ..models import Orders, Users
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from ..settings import settings


class Mailer:

    _instance = None

    def __init__(self) -> None:

        if settings.USE_AWS_SES:
            ...

            # Setup AWS configurations
        else:

            self.configurations = ConnectionConfig(
                MAIL_USERNAME=settings.MAILER.SMTP_USER,
                MAIL_PASSWORD=settings.MAILER.SMTP_PASSWORD,
                MAIL_FROM=settings.DEFAULT_EMAIL_FROM,
                MAIL_FROM_NAME="ChowGoo",
                MAIL_PORT=settings.MAILER.SMTP_PORT,
                MAIL_SERVER=settings.MAILER.SMTP_HOST,
                USE_CREDENTIALS=True,
                VALIDATE_CERTS=True,
                MAIL_STARTTLS=False,
                MAIL_SSL_TLS=True,
            )

            self.transporter = FastMail(self.configurations)

    def send_mail():

        pass

    @staticmethod
    def get_mail_instance():
        if not Mailer._instance:
            Mailer._instance = Mailer()

        return Mailer._instance


mailer = Mailer.get_mail_instance()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAILER.SMTP_USER,
    MAIL_PASSWORD=settings.MAILER.SMTP_PASSWORD,
    MAIL_FROM=settings.DEFAULT_EMAIL_FROM,
    MAIL_FROM_NAME="ChowGoo",
    MAIL_PORT=settings.MAILER.SMTP_PORT,
    MAIL_SERVER="smtp.gmail.com",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
)


def get_order_served_message_schema(student: Users, order: Orders, vendor: Users):

    html = f"""<div style="text-align: center;">
            <img src="https://res.cloudinary.com/marvel6/image/upload/v1681901707/chow_qjjtro.jpg" alt="Company Logo" style="border-radius: 50%; width: 200px; height: 200px; object-fit: cover; margin-top: 20px;">
        </div>
        <p style="font-size: 16px; margin-bottom: 20px;">Dear {student.firstname} {student.lastname} ,</p>
        <p style="font-size: 16px; margin-bottom: 20px;">Your order {order.orderId}  has been served at {vendor.username}.</p>
        <p style="font-size: 16px; margin-bottom: 20px;">Thank you!</p>
        <p style="font-size: 16px; margin-bottom: 0;">chowgoo.com</p>
    </div>"""

    return MessageSchema(
        subject=f"Order {order.orderId} has been served !",
        recipients=[student.email],
        body=html,
        subtype=MessageType.html,
    )
