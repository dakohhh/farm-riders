import logging
from .base import paystack_instance
from pydantic import BaseModel
from beanie import PydanticObjectId
from typing import Optional, Dict, Any
from ..settings import settings
import aiohttp

##############   Paystack   #################


class CheckoutParams(BaseModel):
    email: str
    amount: int
    metadata: Dict[str, Any]


class PaystackResponse(BaseModel):
    status: bool
    message: str
    data: Dict[Any, Any]


class PaystackClient:

    def __init__(self) -> None:

        self.base_url = settings.PAYSTACK.PAYSTACK_BASE_URL
        self.timeout = aiohttp.ClientTimeout(total=30.0, connect=10.0)
        self.headers = {
            'Authorization': f'Bearer {settings.PAYSTACK.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

    async def APIPaystackCheckoutURL(self, params: CheckoutParams):
        params = {
            "email": params.email,
            "amount": str(params.amount * 100),
            "callback_url": "https://farmriders.vercel.app/dashboard",
            "metadata": params.metadata,
        }

        async with aiohttp.ClientSession(base_url=self.base_url, timeout=self.timeout, headers=self.headers) as session:

            async with session.post('/transaction/initialize', json=params) as response:

                if response.status >= 400:
                    error_data = await response.json()

                    # Log the error data
                    logging.warning(error_data)

                    message = error_data.get('message', "An error has occurred")

                    raise aiohttp.ClientResponseError(
                        response.request_info, response.history, status=response.status, message=message
                    )

                data = await response.json()

                return PaystackResponse(**data)
