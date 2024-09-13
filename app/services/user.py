from ..models.profile import Profile, DriverProfile
from pymongo.collection import Collection
from ..models.user import User
from ..schema.user import UserProfile
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

    async def update_driver_profile(update_profile: UserProfile, user: User):

        profile_collection: Collection = DriverProfile._get_collection()

        update_profile_data = update_profile.model_dump(mode='json', exclude_unset=True)

        profile_collection.find_one_and_update({"user": user.id}, {"$set": update_profile_data})

        user.has_completed_profile = True

        user.save()

        return user
