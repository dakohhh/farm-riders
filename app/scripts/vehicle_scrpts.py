from ..models.vehicle import Vehicle

vehicles = [
    {
      "_id": "66e4c44b2ce8ab538ca5e1d1",
      "name": "Isuzu NPR",
      "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726268490/farm_riders/Isuzu%20NPR.jpg"
    },
    {
      "_id": "66e4c44e2ce8ab538ca5e1d2",
      "name": "Tata 407",
      "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726268492/farm_riders/Tata%20407.jpg"
    },
    {
      "_id": "66e4c44f2ce8ab538ca5e1d3",
      "name": "Mitsubishi Fuso Canter",
      "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726268494/farm_riders/Mitsubishi%20Fuso%20Canter.jpg"
    },
    {
      "_id": "66e4c4512ce8ab538ca5e1d4",
      "name": "2021 Ford F-150 Pick Up truck",
      "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726268495/farm_riders/2021%20Ford%20F-150%20Pick%20Up%20truck.jpg"
    },
    {
      "_id": "66e4c4522ce8ab538ca5e1d5",
      "name": "Toyota Hilux",
      "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726268497/farm_riders/Toyota%20Hilux.jpg"
    },
    {
      "_id": "66e4c4532ce8ab538ca5e1d6",
      "name": "Ampere Mitra 250 Load Carrier",
      "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726268498/farm_riders/Ampere%20Mitra%20250%20Load%20Carrier.jpg"
    },
    {
      "_id": "66e4c4542ce8ab538ca5e1d7",
      "name": "Ashok Leyland Dost",
      "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726268500/farm_riders/Ashok%20Leyland%20Dost.jpg"
    },
    {
      "_id": "66e4c4552ce8ab538ca5e1d8",
      "name": "Piaggio Ape Xtra",
      "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726268501/farm_riders/Piaggio%20Ape%20Xtra.jpg"
    },
    {
      "_id": "66e4c4552ce8ab538ca5e1d9",
      "name": "Toyota Hilux Car Toyota Fortuner Pickup Truck",
      "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726268501/farm_riders/Toyota%20Hilux%20Car%20Toyota%20Fortuner%20Pickup%20Truck.jpg"
    },

    {
      "_id": "66e4c4552ce8ab538ca5e1d1",
      "name": "Toyota Hilux Car Toyota Fortuner Pickup Truck",
      "image_url": "https://res.cloudinary.com/do1iufmkf/image/upload/v1726268501/farm_riders/Toyota%20Hilux%20Car%20Toyota%20Fortuner%20Pickup%20Truck.jpg"
    }
]



async def insert_vehicles_on_startup():
    for vehicle in vehicles:
        existing_vehicle = Vehicle.objects(id=vehicle["_id"]).first()
        if not existing_vehicle:
            Vehicle.objects.create(
                id=vehicle["_id"],
                name=vehicle["name"],
                image_url=vehicle["image_url"]
            )
            print(f"Inserted vehicle: {vehicle['name']}")
        else:
            print(f"vehicle {vehicle['name']} already exists.")
