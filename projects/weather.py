from django.shortcuts import render
import requests, json, pytz, datetime
from django.http import JsonResponse

class Weather:
    
    def __init__(self, location):
        self.location = location

    def get_weather_data(self, type):
        # Getting data from openweathermap
        # Type for where you want current weather or forecast
        # According to url type have be one if them ( type = current, type = forecast )
        forecast_url = f"https://api.openweathermap.org/data/2.5/{type}"
        api_key = "b4a00d30b961d7281d593a4d88b463e3"
        params = {"q": self.location, "appid": api_key, "units": "metric"}
        forecast_url_response = requests.get(forecast_url, params=params)
        data = json.loads(forecast_url_response.text)
        return data
        
    def get_current_time(self):
        data = self.get_weather_data("weather")
        if "sys" in data:
            global timezone, unformat_hour
            timezone = pytz.timezone(pytz.country_timezones[data['sys']['country']][0])
            unformat_hour = current_hour = int(datetime.datetime.now(timezone).strftime('%H'))
            current_min = int(datetime.datetime.now(timezone).strftime('%M'))
            if current_hour == 0:
                current_time = f"12:{current_min} A.M"
            if current_min < 10:
                current_min = f"0{current_min}"
            if current_hour != 0 and current_hour < 12:
                current_hour = 0 + current_hour
                current_time = f"{current_hour}:{current_min} A.M"
            elif current_hour == 12:
                current_time = f"{current_hour}:{current_min} P.M"
            if current_hour >= 13:
                current_hour = current_hour - 12
                current_time = f"{current_hour}:{current_min} P.M"
            return current_time

    def get_style(self, weather, current_time):
        # Set weather category
        clear_sky = ["clear sky"]
        few_clouds = ["few clouds"]
        cloudy = ["scattered clouds", "broken clouds", "overcast clouds"]
        rain = ["light rain", "moderate rain", "heavy rain", "heavy intensity rain", "drizzle"]
        snow = ["light snow", "moderate snow", "heavy snow"]
        mist = ["mist", "haze", "smoke", "dust", "fog", "ash",]
        storm = ["squall", "thunderstorm", "sand", "tornado"]
        
        # Check weather result and generate weather icon
        if weather in clear_sky  and 6 < current_time < 18:
            weather_image = "https://cdn-icons-png.flaticon.com/512/3222/3222691.png"
            theme = "#CADBE7"
            font_color = "black"
        elif weather in clear_sky and current_time >= 18 or weather in clear_sky and current_time < 6 or weather in clear_sky and current_time == 0:
            weather_image = "https://cdn-icons-png.flaticon.com/512/1808/1808629.png"
            theme = "#072533"
            font_color = "white"
        elif weather in few_clouds and 0 < current_time < 18:
            weather_image = "https://cdn-icons-png.flaticon.com/512/3222/3222807.png"
            theme = "#CADBE7"
            font_color = "black"
        elif weather in few_clouds and current_time >= 18 or weather in few_clouds and current_time == 0:
            weather_image = "https://cdn.icon-icons.com/icons2/960/PNG/512/1477521569_halloween_outline-18_icon-icons.com_74580.png"
            theme = "#072533"
            font_color = "white"
        elif weather in cloudy and 6 < current_time < 18:
            weather_image = "https://cdn-icons-png.flaticon.com/512/4834/4834559.png"
            theme = "#CADBE7"
            font_color = "black"
        elif weather in cloudy and current_time >= 18 or weather in cloudy and current_time >= 0:
            weather_image = "https://cdn-icons-png.flaticon.com/512/4834/4834559.png"
            theme = "#072533"
            font_color = "white"
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
            theme = "gray"
            font_color = "black"
        elif weather in storm:
            weather_image = "https://cdn-icons-png.flaticon.com/512/1946/1946229.png"
            theme = "#072533"
            font_color = "white"
        style_dict = {"weather_image": weather_image, "theme": theme, "font_color": font_color}
        return style_dict

    def get_current_weather(self):
        
        try:
            data = self.get_weather_data("weather")
            valid = True # To check if the location is valid
            location = self.location.title()
            weather = data['weather'][0]['description']
            temperature = f"{data['main']['temp']}°C"
            feels_like = f"{data['main']['feels_like']}°C"
            humidity = f"{data['main']['humidity']}%"
            wind = f"{data['wind']['speed']} m/s"

            # Check the location time
            current_time = self.get_current_time()
            date = datetime.datetime.now(timezone).strftime('%Y-%m-%d')
            
            style = self.get_style(weather, unformat_hour)
            weather_image = style["weather_image"]
            theme = style["theme"]
            font_color = style["font_color"]

            self.current_results = {'valid': valid, 'location': location, 'weather': weather.title(), 'temperature': temperature, 'feels_like': feels_like, 'humidity': humidity, 'wind': wind, 'weather_image': weather_image, 'current_time': current_time, 'theme': theme, 'date': date, 'font_color': font_color}
        except Exception as e:
            error = str(e)
            valid = False
            self.current_results = {'valid': valid, 'error': error}

    def get_forecast_weather(self):
        
        try:
            valid = True
            results = self.get_weather_data("forecast")["list"][0:]
            forecast_weather = []
            forecast_temp = []
            forecast_date = []
            forecast_hour = []

            # Getting each wanted weather results
            for i in results:
                forecast_weather.append(i["weather"][0]["description"])
                forecast_temp.append(i['main']['temp'])
                forecast_date.append(i["dt_txt"].split(" ")[0][5:])
                forecast_hour.append(int(i["dt_txt"].split(" ")[1][:2]))

            forecast_hour = forecast_hour[0]
            if forecast_hour == 0:
                forecast_time = "12 A.M"
            elif forecast_hour < 12:
                forecast_hour = 0 + forecast_hour
                forecast_time = f"{forecast_hour} A.M"
            elif forecast_hour == 12:
                forecast_time = f"{forecast_hour} P.M"
            if forecast_hour > 12:
                forecast_hour = forecast_hour - 12
                forecast_time = f"{forecast_hour} P.M"
            
            forecast_weather_image = []
            theme = []
            font_color = []

            # Getting styles for each forecast with same time e.g every forecasted at 12 P.M(forecast_hour)
            style = [self.get_style(i, forecast_hour) for i in forecast_weather]
            
            for i in style:
                forecast_weather_image.append(i["weather_image"])
                theme.append(i["theme"])
                font_color.append(i["font_color"])
            
            forecast_weather = [i.title() for i in forecast_weather]
            
            forecast_weather = self.reduce_list(forecast_weather)
            
            forecast_temp = self.reduce_list(forecast_temp)
            
            forecast_date = self.reduce_list(forecast_date)
            
            forecast_weather_image = self.reduce_list(forecast_weather_image)
            
            theme = self.reduce_list(theme)
            
            font_color = self.reduce_list(font_color)
            
            self.forecast_results = {"weather": forecast_weather, "temp": forecast_temp, "date": forecast_date, "time": forecast_time, "weather_image": forecast_weather_image, 'theme': theme, 'font_color': font_color}
        except Exception as e:
            error = str(e)
            valid = False
            self.forecast_results = {"valid": valid, "error": error}

    def reduce_list(self, mylist):
        reduced = [mylist[i] for i in range(len(mylist)) if (i+1)%8 == 0]
        return reduced


## Test here ###
## Remove comment to test in console
#while True:
#    app = Weather(input("Test a city : "))
#    app.get_current_weather()
#    app.get_forecast_weather()
#    print(app.current_results)
#    print("\n")
#    print(app.forecast_results)
#    print("\n")

def weather(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        location = " ".join(location.lower().split())
        app = Weather(location)
        app.get_current_weather()
        app.get_forecast_weather()
        return JsonResponse({'current_results': app.current_results, 'forecast_results': app.forecast_results})
    return render(request, 'weather.html')