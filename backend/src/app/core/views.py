from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def email_preview(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "emails/account_activation.html",
        {
            "url": "nice-url.url",
        },
    )
