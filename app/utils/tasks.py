import asyncio
from fastapi import UploadFile
from ..models import Menu, Orders, Users
from ..libraries.mail import get_order_served_message_schema, conf
from fastapi_mail import FastMail
from ..utils.storage import ChowUpload


def save_custom_menu_image(menu: Menu, uploader: ChowUpload, image: UploadFile):

    print("saving image")

    metadata = uploader.handle_upload(image)

    menu.image_url = metadata["secure_url"]

    menu.save()


async def delete_custom_menu_image(menu_item: Menu):

    uploader = ChowUpload(str(menu_item.id))

    metadata = await uploader.handle_delete()

    return metadata
