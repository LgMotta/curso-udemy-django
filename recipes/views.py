# from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def view_home(request):
    return render(
        request, "home.html", context={"name": "Luiz guilherme"}, status=200
    )


def view_about(request):
    return render(request, "global/about.html")


def view_contact(request):
    return render(request, "recipes/contact.html")
