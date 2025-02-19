from typing import Optional

from app.lib.api import JSONAPIClient
from django.conf import settings


class DeliveryOptionsAPI(JSONAPIClient):
    def __init__(self):
        super().__init__(settings.DELIVERY_OPTIONS_CLIENT_BASE_URL)


def get_delivery_option(iaid: Optional[str] = None):
    do_api = DeliveryOptionsAPI()

    do_api.add_parameter("iaid", iaid)
    do_api.api_path = ""

    return do_api.get()
