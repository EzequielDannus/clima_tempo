import requests
# requests module is not actually a part of the Pyramid framework itself. Instead, it is a separate Python library used for making HTTP requests to web services or web resources. It provides a convenient way to send HTTP requests, handle responses, and work with web APIs.

from pyramid.view import view_config

@view_config(route_name="home", renderer = 'templates/home.jinja2')
def home(request):
    return {}

@view_config(route_name='weather', renderer='templates/home.jinja2')
def weather(request):
    city = request.params.get('city', 'New York')
    api_key = 'd8d31293bee740761c9ba933823c09ea'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        response = requests.get(url)
        data = response.json()
        weather_data = {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
        }
        return {'weather_data': weather_data}
    except Exception:
        return {'error': "Cidade não encontrada, ou digitada incorretamente"}

