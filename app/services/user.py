from bson import ObjectId
from ..models.profile import Profile, DriverProfile
from ..models.vehicle import Vehicle
from pymongo.collection import Collection
from ..utils.exceptions import BadRequestException
from ..models.user import User
from ..schema.user import UserProfile, DriverProfile as UserDriverProfile
from ..utils.helper_functions import normalize_phone_number


class UserService:

    @staticmethod
    async def get_user(user: User):

        result = user.to_mongo()

        result['_id'] = str(result['_id'])

        result['phone_number'] = normalize_phone_number(result['phone_number'])

        result.pop('password', None)

        context = {"user": result}

        return context

    @staticmethod
    async def update_farmer_and_aggregator_profile(update_profile: UserProfile, user: User):

        profile_collection: Collection = Profile._get_collection()

        update_profile_data = update_profile.model_dump(mode='json', exclude_unset=True)

        profile_collection.find_one_and_update({"user": user.id}, {"$set": update_profile_data})

        user.has_completed_profile = True

        user.save()

        return user

    async def update_driver_profile(update_profile: UserDriverProfile, user: User):

        # check if manufacturer_model exists in the database

        if update_profile.vehicle_info.vehicle:

            vehicle = update_profile.vehicle_info.vehicle

            vehicle = Vehicle.objects.filter(id=vehicle).first()

            if not vehicle:
                raise BadRequestException('Invalid vehicle model')

        profile_collection: Collection = DriverProfile._get_collection()

        update_profile_data = update_profile.model_dump(mode='json', exclude_unset=True)

        update_profile_data['vehicle_info']['vehicle'] = ObjectId(update_profile_data['vehicle_info']['vehicle'])

        profile_collection.find_one_and_update({"user": user.id}, {"$set": update_profile_data})

        user.has_completed_profile = True

        user.save()

        return user
