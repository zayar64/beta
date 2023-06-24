from django.shortcuts import render
import requests, json, pytz, datetime
from django.http import JsonResponse

def weather(request):

    # Set weather category
    clear_sky = ["clear sky"]
    few_clouds = ["few clouds"]
    cloudy = ["scattered clouds", "broken clouds", "overcast clouds"]
    rain = ["light rain", "moderate rain", "heavy rain", "heavy intensity rain", "drizzle"]
    snow = ["light snow", "moderate snow", "heavy snow"]
    mist = ["mist", "haze", "smoke", "dust", "fog", "ash",]
    storm = ["squall", "thunderstorm", "sand", "tornado"]
    
    if request.method == 'POST':
        location = request.POST.get('location')
        location = " ".join(location.lower().split())
        url = "https://api.openweathermap.org/data/2.5/weather"
        api_key = "b4a00d30b961d7281d593a4d88b463e3"
        params = {"q": location, "appid": api_key, "units": "metric"}
        response = requests.get(url, params=params)
        try:
            data = json.loads(response.text)
            passed = True
            location = location.title()
            weather = data['weather'][0]['description']
            temperature = f"{data['main']['temp']}°C"
            feels_like = f"{data['main']['feels_like']}°C"
            humidity = f"{data['main']['humidity']}%"
            wind = f"{data['wind']['speed']} m/s"

            # Check the location time
            timezone = pytz.timezone(pytz.country_timezones[data['sys']['country']][0])
            date = datetime.datetime.now(timezone).strftime('%m-%d-%Y')
            unformat_hour = current_hour = int(datetime.datetime.now(timezone).strftime('%H'))
            current_min = int(datetime.datetime.now(timezone).strftime('%M'))
            if current_min < 10:
                current_min = f"0{current_min}"
            if unformat_hour < 12:
                current_hour = 0 + unformat_hour
                current_time = f"{int(current_hour)}:{current_min} A.M"
            elif unformat_hour == 12:
                current_time = f"{int(unformat_hour)}:{current_min} P.M"
            elif unformat_hour > 12:
                current_hour = unformat_hour - 12
                current_time = f"{int(current_hour)}:{current_min} P.M"
            
            # Check weather result and generate weather icon
            if weather in clear_sky  and unformat_hour < 18:
                weather_image = "https://cdn-icons-png.flaticon.com/512/3222/3222691.png"
                theme = "#F29F05"
                font_color = "black"
            elif weather in clear_sky and unformat_hour > 18:
                weather_image = "https://cdn-icons-png.flaticon.com/512/1808/1808629.png"
                theme = "#221620"
                font_color = "white"
            elif weather in few_clouds and unformat_hour < 18:
                weather_image = "https://cdn-icons-png.flaticon.com/512/3222/3222807.png"
                theme = "skyblue"
                font_color = "black"
            elif weather in cloudy:
                weather_image = "https://cdn-icons-png.flaticon.com/512/4834/4834559.png"
                theme = "#CADBE7"
                font_color = "black"
            elif weather in rain:
                weather_image = "https://cdn-icons-png.flaticon.com/512/4150/4150897.png"
                theme = "#072533"
                font_color = "white"
            elif weather in snow:
                weather_image = "https://cdn-icons-png.flaticon.com/512/5906/5906790.png"
                theme = "#white"
                font_color = "black"
            elif weather in mist:
                weather_image = "https://cdn-icons-png.flaticon.com/512/175/175959.png"
                theme = "grey"
                font_color = "black"
            elif weather in storm:
                weather_image = "https://cdn-icons-png.flaticon.com/512/1946/1946229.png"
                theme = "#072533"
                font_color = "white"
            
            return JsonResponse({'passed': passed, 'location': location, 'weather': weather.title(), 'temperature': temperature, 'feels_like': feels_like, 'humidity': humidity, 'wind': wind, 'weather_image': weather_image, 'current_time': current_time, 'theme': theme, 'date': date, 'font_color': font_color})
        except Exception as e:
            error = str(e)
            passed = False
            return JsonResponse({'passed': passed, 'error': error})
    return render(request, 'weather.html')