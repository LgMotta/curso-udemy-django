# from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def view_home(request):
    return render(
        request, "home.html", context={"name": "Luiz guilherme"}, status=200
    )
