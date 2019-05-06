import requests
from django.shortcuts import render ,redirect
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=4262e180a03f058aff405ca6b951ced6'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
        redirect('/')

    form = CityForm()

    cities = City.objects.all().order_by('-id')

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather.html', context)