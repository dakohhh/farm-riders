from mongoengine import Document, StringField, URLField


class Vehicle(Document):

    name = StringField(required=True)

    image_url = URLField()

    meta = {"collection": "vehicle", "strict": False}

