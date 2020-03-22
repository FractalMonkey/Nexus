from django import template
import pyowm

register = template.Library()

@register.simple_tag
def GetTemp():
    owm = pyowm.OWM('979c2f550921b842219612f6b2a6eb27')
    obs = owm.weather_at_place('Hanga Roa, CL')
    weather = obs.get_weather()
    return str(weather.get_temperature('celsius')['temp']) + "℃ / " + str(weather.get_temperature('fahrenheit')['temp']) + "℉"

@register.simple_tag
def GetWeatherStatus():
    owm = pyowm.OWM('979c2f550921b842219612f6b2a6eb27')
    obs = owm.weather_at_place('Hanga Roa, CL')
    weather = obs.get_weather()
    w = "weather_sunny.png"
    if weather.get_status() == "Clouds":
        w = "weather_clouds.png"
    elif weather.get_status() == "Rain":
        w = "weather_rain.png"
    return w