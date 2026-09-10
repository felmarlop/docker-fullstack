from rest_framework.exceptions import APIException


class StripeGeneralError(APIException):
    status_code = 502
    default_detail = "An error occurred while communicating with Stripe."
    default_code = "stripe_general_error"


class StripePaymentCannotBeResumed(APIException):
    status_code = 400
    default_detail = "Stripe payment cannot be resumed."
    default_code = "stripe_payment_cannot_be_resumed"


class StripePaymentCannotBeCanceled(APIException):
    status_code = 400
    default_detail = "Stripe payment cannot be canceled."
    default_code = "stripe_payment_cannot_be_canceled"


class StripePaymentNotFound(APIException):
    status_code = 400
    default_detail = "Subscription payment does not exist."
    default_code = "stripe_payment_not_found"


class StripePriceNoAmount(APIException):
    status_code = 400
    default_detail = "Stripe price does not have a valid amount."
    default_code = "stripe_price_no_amount"


class StripePriceNotActive(APIException):
    status_code = 400
    default_detail = "Subscription plan is not active."
    default_code = "stripe_price_not_active"


class StripePriceNotFound(APIException):
    status_code = 400
    default_detail = "Subscription plan does not exist."
    default_code = "stripe_price_not_found"
