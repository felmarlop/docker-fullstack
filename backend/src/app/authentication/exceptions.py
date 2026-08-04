from rest_framework.exceptions import AuthenticationFailed


class AccountNotActivated(AuthenticationFailed):
    default_detail = "Please activate your account before signing in."
    default_code = "account_not_activated"
