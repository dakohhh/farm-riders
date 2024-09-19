import aiohttp
from ..settings import settings


paystack_instance = aiohttp.ClientSession(
    base_url=settings.PAYSTACK.PAYSTACK_BASE_URL,
    timeout=aiohttp.ClientTimeout(total=30.0, connect=10.0),
    headers={'Authorization': f'Bearer {settings.PAYSTACK.PAYSTACK_SECRET_KEY}', 'Content-Type': 'application/json'},
)
