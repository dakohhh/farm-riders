from ..models.rental import Rentals

rentals = [
      {
        "id": "66e844dae4eb4215bc946720",
        "name": "Water Tanker",
        "price": 32000,
        "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726498009/farm_riders/farm_riders/Water%20Tanker.jpg"
      },
      {
        "id": "66e844dae4eb4215bc946721",
        "name": "Crop Sprayers",
        "price": 21000,
        "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726498010/farm_riders/farm_riders/Crop%20Sprayers.jpg"
      },
      {
        "id": "66e844dce4eb4215bc946722",
        "name": "Milling Machines",
        "price": 27000,
        "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726498012/farm_riders/farm_riders/Milling%20Machines.jpg"
      },
      {
        "id": "66e844dde4eb4215bc946723",
        "name": "Rotavators",
        "price": 45000,
        "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726498013/farm_riders/farm_riders/Rotavators.jpg"
      },
      {
        "id": "66e844dee4eb4215bc946724",
        "name": "Cold Storage Units",
        "price": 30000,
        "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726498014/farm_riders/farm_riders/Cold%20Storage%20Units.jpg"
      },
      {
        "id": "66e844dfe4eb4215bc946725",
        "name": "Tractor",
        "price": 30000,
        "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726498015/farm_riders/farm_riders/Tractor.jpg"
      }
]





async def insert_rentals_on_startup():
    for rental in rentals:
        existing_rentals = Rentals.objects(id=rental["id"]).first()

        if not existing_rentals:
            Rentals.objects.create(
                id=rental["id"], name=rental["name"], price=rental["price"], image_url=rental["image_url"]
            )
            print(f"Inserted rental: {rental['name']}")
        else:
            print(f"rental {rental['name']} already exists.")