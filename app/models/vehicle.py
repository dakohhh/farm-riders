from mongoengine import Document, StringField, URLField, IntField


class Vehicle(Document):

    name = StringField(required=True)

    price = IntField()

    image_url = URLField()

    meta = {"collection": "vehicle", "strict": False}

