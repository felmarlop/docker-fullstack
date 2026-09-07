from rest_framework.exceptions import APIException


class StripePriceNotActive(APIException):
    status_code = 400
    default_detail = "Subscription plan is not active."
    default_code = "stripe_price_not_active"


class StripePriceNotFound(APIException):
    status_code = 400
    default_detail = "Subscription plan does not exist."
    default_code = "stripe_price_not_found"
