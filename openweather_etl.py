import json
from datetime import datetime
import pandas as pd
import requests

city_name = "London"
base_url = "https://api.openweathermap.org/data/2.5/weather?q="

with open("credentials.txt", "r") as f:
    api_key = f.read()

full_url = base_url + city_name + "&APPID=" + api_key

def kelvin_to_farenheit(temp_in_kelvin):
    temp_farenheit = (temp_in_kelvin - 273.15) + (9/5 +32)
    return temp_farenheit

def etl_weather_data(url):
    r = requests.get(url)
    data = r.json()
    # print(data)

    city = data["name"]
    weather_description = data["weather"][0]["description"]
    temp_farenheit = kelvin_to_farenheit(data["main"]["temp"])
    feels_like_farenheit = kelvin_to_farenheit(data["main"]["feels_like"])
    min_temp_farenheit = kelvin_to_farenheit(data["main"]["temp_min"])
    max_temp_farenheit = kelvin_to_farenheit(data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    time_of_record = datetime.utcfromtimestamp(data["dt"] + data["timezone"])
    sunrise_time = datetime.utcfromtimestamp(data["sys"]["sunrise"] + data["timezone"])
    sunset_time = datetime.utcfromtimestamp(data["sys"]["sunset"] + data["timezone"])

    transformed_data = {
        'city' : city,
        'weather_description' : weather_description,
        'temperature (f)' : temp_farenheit,
        'feels_like (f)' : feels_like_farenheit,
        'minimum_temperature (f)' : min_temp_farenheit,
        'maximum_temperature (f)' : max_temp_farenheit,
        'pressure' : pressure,
        'humidity' : humidity,
        'wind_speed' : wind_speed,
        'time_of_record' : time_of_record,
        'sunrise (local_time)' : sunrise_time,
        'sunset ((local_time))' : sunset_time
    }

    # print(transformed_data)

    transformed_data_list = [transformed_data]
    df_data = pd.DataFrame(transformed_data_list)
    # print(df_data)

    df_data.to_csv('openweather_london_etl.csv', index=False)

if __name__ == '__main__':
    etl_weather_data(url = full_url)
