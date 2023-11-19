from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, JsonResponse

from mainApp.models import *
import json, requests , datetime

from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie

def indexDemo(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@ensure_csrf_cookie
def index(request):
    context={ 'pageTitle' : pageTitle} 
    # print(request.__dict__)
    # print(request.headers)
    return render(request, "mainApp/index.html", context)








def getEvents(request):

    lat , lon, message = get_my_user_Lat_Lon(request)
    # print(lat , lon, message)

    #throws error if location cant be found
    if (lat == 0 and lon == 0):
        return JsonResponse( {'status' : 'error' , 'errorMessage': render_to_string('mainApp/modal.html', context=message) }, safe=False)
    
    ## Get lat, lon from client ip
    # rl = requests.get(f'https://api.seatgeek.com/2/events?geoip={client_ip}&rnage=1mi&per_page=1&client_id=MzcwNDI1NTB8MTY5NTg3NDM1My4wNjYwMDU1')

    # datal = rl.json()
    # print(datal)
    # print(datal['meta']['geolocation']['lat'], data['meta']['geolocation']['lon'])

    ## Get Events from OUR DB
    myDbJson = list( Event.objects.filter(date__gte = datetime.date.today()).values() ) #Time on db seems to be three hours ahead of local time.(its UTC)
    # print(datetime.date.today()+datetime.timedelta(days=6))

    
    ## Get from seat geek api
    seatGeekList = get_seatGeek_list(lat, lon)
    ticketMasterDiscoveryList = get_ticketMasterDiscovery_list(lat, lon)


    #Combine All Results
    response = { 'events' : list(myDbJson + seatGeekList + ticketMasterDiscoveryList)}
    response['location'] = {'lat' : lat , 'lon' : lon}
    response['message'] = message

    # print(len(response))
    return JsonResponse( response , safe=False)

## /addEventForm/ ##
def addEventForm(request):
    return render(request, "mainApp/addEventForm.html", { 'pageTitle' : pageTitle})

def postEvent(request):
    
    p = request.POST.dict()
    newEvent = Event(title=p['titleInput'], description=p['descriptionInput'], date=p['dateInput'], address=p['addressInput'])

    #get geocode
    geocode = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={p["addressInput"]}&key=AIzaSyBsjbLLe2RaAjIzUe5lxKb7wLFvebnX2gY')
    # print(r.text)
    geocode_json= json.loads(geocode.text)
    # print(rj['results'][0]['geometry']['location'])
    # print(rj['results'][0]['geometry']['location']['lat'])

    newEvent.latitude = geocode_json['results'][0]['geometry']['location']['lat']
    newEvent.longitude = geocode_json['results'][0]['geometry']['location']['lng']

    newEvent.save()
    return render(request, "mainApp/index.html")











#### variables ####
pageTitle = 'Things-to-do-near-me!'


## FUNC GET CLIENT IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
       ip = x_forwarded_for.split(',')[0]
    else:
       ip = request.META.get('REMOTE_ADDR')
    return ip





## FUNC GET USER LAT LON
def get_my_user_Lat_Lon(request):

    requestBody = json.loads(request.body)
    # print(requestBody)
    # if lat, lon
    try:
        
        lat, lon = requestBody['props']['lat'] , requestBody['props']['lon']
        return lat, lon, {}
    
    except: pass

    # if address
    try:
        
        geocode = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={requestBody["props"]["addressInput"]}&key=AIzaSyBsjbLLe2RaAjIzUe5lxKb7wLFvebnX2gY')
        # print(geocode.text)
        geocode_json= json.loads(geocode.text)
        # print(geocode.text)
        # print(rj['results'][0]['geometry']['location'])
        # print(rj['results'][0]['geometry']['location']['lat'])
        try:
            lat = geocode_json['results'][0]['geometry']['location']['lat']
            lon = geocode_json['results'][0]['geometry']['location']['lng']
        except: return 0, 0, {"title":"Couldn't find address" , "subTitle": "check spelling and try again", "addressBar":True, "footer": True }

        return lat, lon, {"addressInput":requestBody["props"]["addressInput"]}
    
    # except: pass

    # else try ip
    # try:
    #     print(3)
        # client_ip = get_client_ip(request)
        # r = requests.get(f'https://api.seatgeek.com/2/events?geoip={client_ip}&datetime_local={datetime.date.today()}&per_page=1&client_id=MzcwNDI1NTB8MTY5NTg3NDM1My4wNjYwMDU1')
        # r_JSON = r.json()
        # print(client_ip)
        # print(r.json)
        # lat = r_JSON['meta']['geolocation']['lat']
        # lon = r_JSON['meta']['geolocation']['lon']

        # return lat, lon

    #catch all
    except:
        return 0 , 0 , {"title":"Find Things to do" , "subTitle": "Search city, town, zip etc.", "addressBar":True, "footer": False }
        

## APIs ##

# SeatGeek
def get_seatGeek_list(lat, lon):

    results_page_number, seatGeekList = 0, []

    while(True):
        results_page_number += 1
        r = requests.get(f'https://api.seatgeek.com/2/events?lat={lat}&lon={lon}&datetime_local.gt={datetime.date.today()}&datetime_local.lte={datetime.date.today()+datetime.timedelta(days=6)}&per_page=50&page={results_page_number}&client_id=MzcwNDI1NTB8MTY5NTg3NDM1My4wNjYwMDU1')
        data = r.json()

        for o in data['events']:
            temp_obj = {}
            temp_obj['title'] = ''.join(o["title"].split('-')[:-1]) if len(o["title"].split('-')) > 2 else o["title"].split('-')[0]
            temp_obj['date'] = o["datetime_local"][:10]
            temp_obj['address'] = o["venue"]["name"]
            temp_obj['latitude'] = o['venue']["location"]["lat"]
            temp_obj['longitude'] = o['venue']['location']['lon']
            temp_obj['url'] = o['performers'][0]["url"]
            seatGeekList.append(temp_obj)
            # print(type(temp_obj['latitude']),temp_obj['longitude'])

        if len(data['events']) == 0:
            break
    # print(seatGeekList)
    return( seatGeekList )

# TicketMaster Discovery
def get_ticketMasterDiscovery_list(lat, lon):

    results_page_number, data_list = 0, []

    while(True):
        r = requests.get(f'https://app.ticketmaster.com/discovery/v2/events.json?apikey=YJLOMi9Nx8ze3SqTew85sb32Wk87AWR3&latlong=40.7561988,-73.7920859&size=199&startDateTime={datetime.date.today()}T00:00:00Z&endDateTime={datetime.date.today()+datetime.timedelta(days=6)}T00:00:00Z&radius=50&page={results_page_number}')
        data = r.json()

        for o in data['_embedded']['events']:
            temp_obj = {}
            temp_obj['title'] = o['name']
            temp_obj['date'] = o['dates']['start']['localDate']
            temp_obj['address'] = o['_embedded']['venues'][0]['name']
            temp_obj['latitude'] = float (o['_embedded']['venues'][0]['location']['latitude'])
            temp_obj['longitude'] = float (o['_embedded']['venues'][0]['location']['longitude'])
            temp_obj['url'] = o['url']
            data_list.append(temp_obj)
            # print(type(temp_obj['latitude']),temp_obj['longitude'])
            if (o['name'] == 'FOOD'):
                print(o)

        print(data['page']['number'] , data['page']['totalPages'])
        if data['page']['number'] == data['page']['totalPages']-1: #keep an eye on! -last page is always empty today****
            break

        results_page_number += 1
        # print(results_page_number)
    print(len(data_list))
    return data_list