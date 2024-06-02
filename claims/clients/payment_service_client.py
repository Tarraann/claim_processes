from claims.config.config import get_config
from claims.utils.http_client import HttpClient
from typing import List
from claims.lib.logger import logger


class PaymentServiceClient:
    def __init__(self):
        self.http_client = HttpClient(base_url=get_config("PAYMENT_SERVICE_URL"))

    def notify_net_fee(self, payment_data: List):
        logger.info("Notifying net fees to payment service")
        endpoint = f"payments/net_fee"
        request_data = {"payment_data": payment_data}
        response = self.http_client.post(endpoint=endpoint, data=request_data)
        return response
