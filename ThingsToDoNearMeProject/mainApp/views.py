from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, JsonResponse

from mainApp.models import *
import json
import requests , datetime


def indexDemo(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    context={ 'pageTitle' : pageTitle} 
    # print(request.__dict__)
    # print(request.headers)
    return render(request, "mainApp/index.html", context)

def getEvents(request):
    l = Event.objects.filter(date__gte = datetime.date.today()).values() #Time on db seems to be three hours ahead of local time.
    # print(datetime.date.today())
    return JsonResponse(list(l), safe=False)

def addEventForm(request):
    return render(request, "mainApp/addEventForm.html", { 'pageTitle' : pageTitle})

def postEvent(request):
    
    p = request.POST.dict()
    newEvent = Event(title=p['titleInput'], description=p['descriptionInput'], date=p['dateInput'], address=p['addressInput'])

    #get geocode
    r = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={p["addressInput"]}&key=AIzaSyBsjbLLe2RaAjIzUe5lxKb7wLFvebnX2gY')
    # print(r.text)
    rj= json.loads(r.text)
    # print(rj['results'][0]['geometry']['location'])
    # print(rj['results'][0]['geometry']['location']['lat'])

    newEvent.latitude = rj['results'][0]['geometry']['location']['lat']
    newEvent.longitude = rj['results'][0]['geometry']['location']['lng']

    newEvent.save()
    return render(request, "mainApp/index.html")

pageTitle = 'Things-to-do-near-me!'


