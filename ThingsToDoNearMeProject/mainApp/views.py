from django.shortcuts import render
from django.http import HttpResponse


def indexDemo(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    context={}
    return render(request, "mainApp/index.html", context)


