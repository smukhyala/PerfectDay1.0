#! /usr/bin/env python
import schedule
import time
import json
import requests as req
import datetime
import smtplib
from email.message import EmailMessage

### API INFORMATION DO NOT DELETE (HIDE IN GIT)
BaseURL = "http://api.openweathermap.org/data/2.5/forecast?"
OpenMainKey = "b12c5e04c89021d40208a84f66ebd3bb"

def getData():
    f = open("AllActivities.json", "r")
    data = json.load(f)
    return data

def fetchCityData(City):
    NewURL = BaseURL + "appid=" + OpenMainKey + "&q=" + City
    APIRequest = req.get(NewURL).json()
    #print(APIRequest)
    return(APIRequest)

### Temperature conversion
def kelvin_to_fahrenheit(kelvin):
    fahrenheit = (kelvin - 273.15) * (9/5) + 32
    return fahrenheit

def sendMail(content):
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(content)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'PerfectDay'
    msg['From'] = "smukhyala@gmail.com"
    msg['To'] = "25mukhyalas62@stu.smuhsd.org"

    # Send the message via our own SMTP server.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('smukhyala@gmail.com', 'kanljwhyimbizlla')
    server.send_message(msg)

def job():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Starting job at", current_time)
    grabbedData = getData()
    allActivities = []
    for activity in grabbedData["activities"]:
        goodDays = ', '.join(judgeWeather(activity))
        weatherEvaluation = "Your PerfectDays are {}.{}".format(goodDays, "\n")
        judgeWeather(activity)
        allActivities.append({'title':f"{activity['ActivityChoice']} in {activity['CityChoice']}",'subtitle':goodDays,'icon':''})
    sendMail(json.dumps(allActivities))
    f = open("PerfectDays.json", "w")
    json.dump(allActivities, f, indent = 4)
    f.close()

### Judge Weather
def judgeWeather(activityData):
    ### Intro
    #print("We are in!")
    goodDays = []

    ### Counts
    goodConditionCount = 0
    badConditionCount = 0

    ### Using fetch and weather data
    weatherData = fetchCityData(activityData["CityChoice"])

    ### Defining and sorting through the dictionary values
    for forecast in weatherData['list']:
        temp_kelvin = forecast['main']['temp']
        low_temp_kelvin = forecast['main']['temp_min']
        high_temp_kelvin = forecast['main']['temp_max']
        feels_temp_kelvin = forecast['main']['feels_like']
        humidity = forecast['main']['humidity']
        description = forecast['weather'][0]['description']
        wind_speed = forecast['wind']['speed']

        ### Using the temperature conversion
        temp_fahrenheit = kelvin_to_fahrenheit(temp_kelvin)
        feels_fahrenheit = kelvin_to_fahrenheit(feels_temp_kelvin)
        low_temp_fahrenheit = kelvin_to_fahrenheit(low_temp_kelvin)
        high_temp_fahrenheit = kelvin_to_fahrenheit(high_temp_kelvin)

        ### Assigning slider values to variables
        activity = activityData["ActivityChoice"]
        idealLowTemp = activityData["LowTemp"]
        idealHighTemp = activityData["HighTemp"]
        idealLowWindSpeed = activityData["LowWind"]
        idealHighWindSpeed = activityData["HighWind"]
        idealLowHumidity = activityData["LowHumidity"]
        idealHighHumidity = activityData["HighHumidity"]

        ### Defining good and bad weather occurences for the specifed user-criteria (chosen above)
        ### Temperature
        if (int(idealLowTemp) <= low_temp_fahrenheit) and (high_temp_fahrenheit <= int(idealHighTemp)):
            goodConditionCount = goodConditionCount + 2
        elif (int(idealLowTemp) <= low_temp_fahrenheit) and (int(idealHighTemp) < high_temp_fahrenheit):
            goodConditionCount = goodConditionCount + 1
            badConditionCount = badConditionCount + 1
        elif (low_temp_fahrenheit < int(idealLowTemp)) and (high_temp_fahrenheit <= int(idealHighTemp)):
            goodConditionCount = goodConditionCount + 1
            badConditionCount = badConditionCount + 1
        elif (low_temp_fahrenheit < int(idealLowTemp)) and (int(idealHighTemp) < high_temp_fahrenheit):
            badConditionCount = badConditionCount + 2

        ### Other forecasts
        if (int(idealLowWindSpeed)) <= wind_speed <= (int(idealHighWindSpeed)):
            goodConditionCount = goodConditionCount + 1
        elif (wind_speed < (int(idealLowWindSpeed))) or ((int(idealHighWindSpeed)) < wind_speed):
            badConditionCount = badConditionCount + 1

        if (int(idealLowHumidity)) <= humidity <= (int(idealHighHumidity)):
            goodConditionCount = goodConditionCount + 1
        elif (humidity < (int(idealLowHumidity))) or ((int(idealHighHumidity)) < humidity):
            badConditionCount = badConditionCount + 1

        ### Determining the final verdict
        if goodConditionCount - badConditionCount >= 3:
            weatherEvaluation = "optimal! What a PerfectDay!"
            goodDays.append(f"{forecast['dt_txt']}")
        elif goodConditionCount - badConditionCount == 2:
            weatherEvaluation = "decent, almost a PerfectDay."
        elif goodConditionCount - badConditionCount == 1:
            weatherEvaluation = "viable, somewhat a PerfectDay."
        elif goodConditionCount - badConditionCount < 1:
            weatherEvaluation = "suboptimal, not a PerfectDay. See another day's forecast or a different location."

        ### Console and assigning the label
        #print("Our verdict is {} on {} in {}.{}".format(weatherEvaluation, forecast["dt_txt"], activityData['CityChoice'], "\n"))

    return goodDays

schedule.every(20).seconds.do(job)
#schedule.every(2).hour.do(judgeWeather(activity))
#schedule.every().day.at("10:30").do(judgeWeather(activity))
#schedule.every().monday.do(judgeWeather(activity))
#schedule.every().wednesday.at("13:15").do(judgeWeather(activity))
#schedule.every().minute.at(":17").do(judgeWeather(activity))

while True:
    schedule.run_pending()
    time.sleep(1)
