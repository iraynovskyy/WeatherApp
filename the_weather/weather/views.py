import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views import View
from .models import City
from .forms import CityForm
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from datetime import datetime

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=15f9800be566168462df7bb35a93302b'
    url2 = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&appid=15f9800be566168462df7bb35a93302b'
    # city = 'Amsterdam'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        # pass
        # print(request.POST)
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count() # quering the db to check if there are no match the same name.
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                # print(r)
        
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    print(err_msg)
    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()
        # print(r.text)      | for r as not a json()

        lat = r['coord']['lat']
        lon = r['coord']['lon']
        r7 = requests.get(url2.format(lat, lon)).json()
        # print('R7T===',r7['current']['humidity'])

        city_weather = {
            'city' : city,
            'temperature' : r['main']['temp'],
            'wind_speed': r7['current']['wind_speed'],
            'humidity': r7['current']['humidity'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)    

    global_weather = []
    glob_city = []
    glob_temperature = []
    glob_wind_speed = []
    glob_humidity = []
    for i in range(0, len(weather_data)):

        glob_city.append(weather_data[i]['city'].name)
        glob_temperature.append(weather_data[i]['temperature'])
        glob_wind_speed.append(weather_data[i]['wind_speed'])
        glob_humidity.append(weather_data[i]['humidity'])

    context = {
        'weather_data': weather_data,
        'global_weather': global_weather,
        'glob_city': glob_city,
        'glob_temperature': glob_temperature,
        'glob_wind_speed': glob_wind_speed,
        'glob_humidity': glob_humidity,
        'form': form,
        'message': message,
        'message_class': message_class
    }
    return render(request, 'weather.html', context)


def detail_city(request, city_name):

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=15f9800be566168462df7bb35a93302b'
    url2 = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&appid=15f9800be566168462df7bb35a93302b'

    form = CityForm()
    print(city_name)
    city = City.objects.filter(name=city_name)[0]
    print('city=',city)
    r = requests.get(url.format(city)).json()
    print('r',r)     

    lat = r['coord']['lat']
    lon = r['coord']['lon']
    r7 = requests.get(url2.format(lat, lon)).json()
    print('Added city is', city, r7)

   
    chart_labels = ['now', '+1:00', '+2:00', '+3:00', '+4:00', '+5:00', '+6:00', '+7:00', '+8:00', '+9:00', '+10:00', '+11:00', '+12:00', '+13:00', '+14:00', '+15:00', '+16:00', '+17:00', '+18:00', '+19:00', '+20:00', '+21:00', '+22:00', '+23:00', '+24:00', '+25:00', '+26:00', '+27:00', '+28:00', '+29:00', '+30:00', '+31:00', '+32:00']
    # chart_labels = ['now', '+1h', '+2h', '+3h', '+4h', '+5h', '+6h', '+7h', '+8h', '+9h', '+10h', '+11h', '+12h', '+13h', '+14h', '+15h', '+16h', '+17h', '+18h', '+19h', '+20h', '+21h', '+22h', '+23h', '+24h', '+25h', '+26h', '+27h', '+28h']
  
    chart_data_temp = [
                r7['hourly'][0]['temp'], 
                r7['hourly'][1]['temp'], 
                r7['hourly'][2]['temp'],
                r7['hourly'][3]['temp'],
                r7['hourly'][4]['temp'], 
                r7['hourly'][5]['temp'],
                r7['hourly'][6]['temp'],
                r7['hourly'][7]['temp'],
                r7['hourly'][8]['temp'],
                r7['hourly'][9]['temp'],
                r7['hourly'][10]['temp'],
                r7['hourly'][11]['temp'],
                r7['hourly'][12]['temp'],
                r7['hourly'][13]['temp'],
                r7['hourly'][14]['temp'],
                r7['hourly'][15]['temp'],
                r7['hourly'][16]['temp'],
                r7['hourly'][17]['temp'],
                r7['hourly'][18]['temp'],
                r7['hourly'][19]['temp'],
                r7['hourly'][20]['temp'],
                r7['hourly'][21]['temp'],
                r7['hourly'][22]['temp'],
                r7['hourly'][23]['temp'],
                r7['hourly'][24]['temp'],
                r7['hourly'][25]['temp'],
                r7['hourly'][26]['temp'],
                r7['hourly'][27]['temp'],
                r7['hourly'][28]['temp'],
                r7['hourly'][29]['temp'],
                r7['hourly'][30]['temp'],
                r7['hourly'][31]['temp'],
                r7['hourly'][32]['temp']
                ]

    chart_data_wind = [
                r7['hourly'][0]['wind_speed'], 
                r7['hourly'][1]['wind_speed'], 
                r7['hourly'][2]['wind_speed'],
                r7['hourly'][3]['wind_speed'],
                r7['hourly'][4]['wind_speed'], 
                r7['hourly'][5]['wind_speed'],
                r7['hourly'][6]['wind_speed'],
                r7['hourly'][7]['wind_speed'],
                r7['hourly'][8]['wind_speed'],
                r7['hourly'][9]['wind_speed'],
                r7['hourly'][10]['wind_speed'],
                r7['hourly'][11]['wind_speed'],
                r7['hourly'][12]['wind_speed'],
                r7['hourly'][13]['wind_speed'],
                r7['hourly'][14]['wind_speed'],
                r7['hourly'][15]['wind_speed'],
                r7['hourly'][16]['wind_speed'],
                r7['hourly'][17]['wind_speed'],
                r7['hourly'][18]['wind_speed'],
                r7['hourly'][19]['wind_speed'],
                r7['hourly'][20]['wind_speed'],
                r7['hourly'][21]['wind_speed'],
                r7['hourly'][22]['wind_speed'],
                r7['hourly'][23]['wind_speed'],
                r7['hourly'][24]['wind_speed'],
                r7['hourly'][25]['wind_speed'],
                r7['hourly'][26]['wind_speed'],
                r7['hourly'][27]['wind_speed'],
                r7['hourly'][28]['wind_speed'],
                r7['hourly'][29]['wind_speed'],
                r7['hourly'][30]['wind_speed'],
                r7['hourly'][31]['wind_speed'],
                r7['hourly'][32]['wind_speed']
                ]

    chart_data_humidity = [
                r7['hourly'][0]['humidity'], 
                r7['hourly'][1]['humidity'], 
                r7['hourly'][2]['humidity'],
                r7['hourly'][3]['humidity'],
                r7['hourly'][4]['humidity'], 
                r7['hourly'][5]['humidity'],
                r7['hourly'][6]['humidity'],
                r7['hourly'][7]['humidity'],
                r7['hourly'][8]['humidity'],
                r7['hourly'][9]['humidity'],
                r7['hourly'][10]['humidity'],
                r7['hourly'][11]['humidity'],
                r7['hourly'][12]['humidity'],
                r7['hourly'][13]['humidity'],
                r7['hourly'][14]['humidity'],
                r7['hourly'][15]['humidity'],
                r7['hourly'][16]['humidity'],
                r7['hourly'][17]['humidity'],
                r7['hourly'][18]['humidity'],
                r7['hourly'][19]['humidity'],
                r7['hourly'][20]['humidity'],
                r7['hourly'][21]['humidity'],
                r7['hourly'][22]['humidity'],
                r7['hourly'][23]['humidity'],
                r7['hourly'][24]['humidity'],
                r7['hourly'][25]['humidity'],
                r7['hourly'][26]['humidity'],
                r7['hourly'][27]['humidity'],
                r7['hourly'][28]['humidity'],
                r7['hourly'][29]['humidity'],
                r7['hourly'][30]['humidity'],
                r7['hourly'][31]['humidity'],
                r7['hourly'][32]['humidity']
                ]

    chart_data_clouds = [
                r7['hourly'][0]['clouds'], 
                r7['hourly'][1]['clouds'], 
                r7['hourly'][2]['clouds'],
                r7['hourly'][3]['clouds'],
                r7['hourly'][4]['clouds'], 
                r7['hourly'][5]['clouds'],
                r7['hourly'][6]['clouds'],
                r7['hourly'][7]['clouds'],
                r7['hourly'][8]['clouds'],
                r7['hourly'][9]['clouds'],
                r7['hourly'][10]['clouds'],
                r7['hourly'][11]['clouds'],
                r7['hourly'][12]['clouds'],
                r7['hourly'][13]['clouds'],
                r7['hourly'][14]['clouds'],
                r7['hourly'][15]['clouds'],
                r7['hourly'][16]['clouds'],
                r7['hourly'][17]['clouds'],
                r7['hourly'][18]['clouds'],
                r7['hourly'][19]['clouds'],
                r7['hourly'][20]['clouds'],
                r7['hourly'][21]['clouds'],
                r7['hourly'][22]['clouds'],
                r7['hourly'][23]['clouds'],
                r7['hourly'][24]['clouds'],
                r7['hourly'][25]['clouds'],
                r7['hourly'][26]['clouds'],
                r7['hourly'][27]['clouds'],
                r7['hourly'][28]['clouds'],
                r7['hourly'][29]['clouds'],
                r7['hourly'][30]['clouds'],
                r7['hourly'][31]['clouds'],
                r7['hourly'][32]['clouds']
                ]

    weather_data_detail = {
        'city' : city,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'],

        # data for hourly forecast
        'temperature_now' : r7['hourly'][0]['temp'],
        'humidity_now' : r7['hourly'][0]['humidity'],
        'description_now' : r7['hourly'][0]['weather'][0]['description'],
        'icon_now' : r7['hourly'][0]['weather'][0]['icon'],
        'wind_speed_now' : r7['hourly'][0]['wind_speed'],
        'clouds_now' : r7['hourly'][0]['clouds'],

        'temperature_1hour' : r7['hourly'][1]['temp'],
        'humidity_1hour' : r7['hourly'][1]['humidity'],
        'description_1hour' : r7['hourly'][1]['weather'][0]['description'],
        'icon_1hour' : r7['hourly'][1]['weather'][0]['icon'],
        'wind_speed_1hour' : r7['hourly'][1]['wind_speed'],
        'clouds_1hour' : r7['hourly'][1]['clouds'],

        'temperature_2hour' : r7['hourly'][2]['temp'],
        'humidity_2hour' : r7['hourly'][2]['humidity'],
        'description_2hour' : r7['hourly'][2]['weather'][0]['description'],
        'icon_2hour' : r7['hourly'][2]['weather'][0]['icon'],
        'wind_speed_2hour' : r7['hourly'][2]['wind_speed'],
        'clouds_2hour' : r7['hourly'][2]['clouds'],

        'temperature_3hour' : r7['hourly'][3]['temp'],
        'humidity_3hour' : r7['hourly'][3]['humidity'],
        'description_3hour' : r7['hourly'][3]['weather'][0]['description'],
        'icon_3hour' : r7['hourly'][3]['weather'][0]['icon'],
        'wind_speed_3hour' : r7['hourly'][3]['wind_speed'],
        'clouds_3hour' : r7['hourly'][3]['clouds'],

        'temperature_4hour' : r7['hourly'][4]['temp'],
        'humidity_4hour' : r7['hourly'][4]['humidity'],
        'description_4hour' : r7['hourly'][4]['weather'][0]['description'],
        'icon_4hour' : r7['hourly'][4]['weather'][0]['icon'],
        'wind_speed_4hour' : r7['hourly'][4]['wind_speed'],
        'clouds_4hour' : r7['hourly'][4]['clouds'],

        'temperature_5hour' : r7['hourly'][5]['temp'],
        'humidity_5hour' : r7['hourly'][5]['humidity'],
        'description_5hour' : r7['hourly'][5]['weather'][0]['description'],
        'icon_5hour' : r7['hourly'][5]['weather'][0]['icon'],
        'wind_speed_5hour' : r7['hourly'][5]['wind_speed'],
        'clouds_5hour' : r7['hourly'][5]['clouds'],

        'temperature_6hour' : r7['hourly'][6]['temp'],
        'humidity_6hour' : r7['hourly'][6]['humidity'],
        'description_6hour' : r7['hourly'][6]['weather'][0]['description'],
        'icon_6hour' : r7['hourly'][6]['weather'][0]['icon'],
        'wind_speed_6hour' : r7['hourly'][6]['wind_speed'],
        'clouds_6hour' : r7['hourly'][6]['clouds'],

        'temperature_7hour' : r7['hourly'][7]['temp'],
        'humidity_7hour' : r7['hourly'][7]['humidity'],
        'description_7hour' : r7['hourly'][7]['weather'][0]['description'],
        'icon_7hour' : r7['hourly'][7]['weather'][0]['icon'],
        'wind_speed_7hour' : r7['hourly'][7]['wind_speed'],
        'clouds_7hour' : r7['hourly'][7]['clouds'],
        
        'temperature_8hour' : r7['hourly'][8]['temp'],
        'humidity_8hour' : r7['hourly'][8]['humidity'],
        'description_8hour' : r7['hourly'][8]['weather'][0]['description'],
        'icon_8hour' : r7['hourly'][8]['weather'][0]['icon'],
        'wind_speed_8hour' : r7['hourly'][8]['wind_speed'],
        'clouds_8hour' : r7['hourly'][8]['clouds'],

        'temperature_9hour' : r7['hourly'][9]['temp'],
        'humidity_9hour' : r7['hourly'][9]['humidity'],
        'description_9hour' : r7['hourly'][9]['weather'][0]['description'],
        'icon_9hour' : r7['hourly'][9]['weather'][0]['icon'],
        'wind_speed_9hour' : r7['hourly'][9]['wind_speed'],
        'clouds_9hour' : r7['hourly'][9]['clouds'],
    }


    context = {
        'weather_data_detail': weather_data_detail,
        'chart_labels': chart_labels,
        'chart_data_temp': chart_data_temp,
        'chart_data_wind': chart_data_wind,
        'chart_data_humidity': chart_data_humidity,
        'chart_data_clouds': chart_data_clouds
    }

    print('City is:',City.objects.filter(name=city_name)[0])
    return render(request, 'weather_detail.html',context)


@login_required(login_url='login')  # redirect when user is not logged in
def delete_city(request, city_name):
    # City.objects.get(name=city_name).delete()
    # return redirect('home')
    if request.user.is_authenticated:
        City.objects.filter(name=city_name).delete()
        return redirect('home')
    else:
        return HttpResponseForbidden()


def logout(request):
    auth.logout(request)
    # print('gooody')
    # return redirect('/')    # same as '/'='home'
    return redirect('home')

def logout_detail(request, city_name):
    auth.logout(request)
    # print('gooody')
    # return redirect('/')    # same as '/'='home'
    return redirect('home')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')
    # pass

def register(request):
    # pass

    if request.method == 'POST':
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                # print('Username taken')
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email) #, first_name=first_name,
                                                #last_name=last_name)
                user.save()
                print('user created')
                return redirect('login')

        else:
            messages.info(request, 'password not matching..')
            return redirect('register')
        return redirect('/')

    else:
        return render(request, 'register.html')






