from datetime import datetime
from ..libraries.mail import mailer
from ..settings import settings
from fastapi_mail import MessageSchema
from ..models import Users
from jinja2 import Environment, FileSystemLoader


template_loader = FileSystemLoader(settings.MAILER.TEMPLATE_DIR)
template_environment = Environment(loader=template_loader)


class MailService:

    @staticmethod
    async def send_order_served_mail(user: Users, orderId: str, vendorName: str):

        email_props = {
            "title": "Order Served",
            "firstname": user.firstname,
            "lastname": user.lastname,
            "vendorName": vendorName,
            "orderId": orderId,
            "currentYear": datetime.now().year,
        }

        # Load the template
        template = template_environment.get_template('order_served.html')  # Use the correct template file name

        rendered_template = template.render(email_props)

        message = MessageSchema(
            subject="Order Served", recipients=[user.email], subtype="html", template_body=rendered_template
        )

        await mailer.transporter.send_message(message)
