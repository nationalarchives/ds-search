from app.ciim.client import ClientAPI
from django.conf import settings


def get_records_client():
    return ClientAPI(
        base_url=settings.CLIENT_BASE_URL,
        api_key=settings.CLIENT_KEY,
        verify_certificates=settings.CLIENT_VERIFY_CERTIFICATES,
    )


records_client = get_records_client()
