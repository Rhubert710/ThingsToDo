from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, JsonResponse

from mainApp.models import *
import json, requests , datetime


def indexDemo(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    context={ 'pageTitle' : pageTitle} 
    # print(request.__dict__)
    # print(request.headers)
    return render(request, "mainApp/index.html", context)







def getEvents(request):
    
    ## Get Events from OUR DB
    l = list( Event.objects.filter(date__gte = datetime.date.today()).values() ) #Time on db seems to be three hours ahead of local time.
    print(datetime.date.today()+datetime.timedelta(days=4))

    
    ## Get from seat geek api
    results_page_number, seatGeekJson = 0, []
    while(True):
        results_page_number += 1
        r = requests.get(f'https://api.seatgeek.com/2/events?geoip=true&datetime_local.gt={datetime.date.today()}&datetime_local.lte={datetime.date.today()+datetime.timedelta(days=4)}&per_page=50&page={results_page_number}&client_id=MzcwNDI1NTB8MTY5NTg3NDM1My4wNjYwMDU1')
        data = r.json()

        for o in data['events']:
            temp_obj = {}
            temp_obj['title'] = ''.join(o["title"].split('-')[:-1]) if len(o["title"].split('-')) > 2 else o["title"].split('-')[0]
            temp_obj['date'] = o["datetime_local"][:10]
            temp_obj['address'] = o["venue"]["name"]
            temp_obj['latitude'] = o['venue']["location"]["lat"]
            temp_obj['longitude'] = o['venue']['location']['lon']
            seatGeekJson.append(temp_obj)

        # seatGeekJson += list ( data['events'] )
        if len(data['events']) == 0:
            break
    # print(seatGeekJson)


    #Combine All Results
    l += seatGeekJson
    print(len(l))
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


