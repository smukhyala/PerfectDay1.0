#! /usr/bin/env python
#FIX EMAIL FORMAT ASAP
import schedule
import pprint
import time
import json
import requests as req
import datetime
import smtplib
from email.message import EmailMessage

### API INFORMATION DO NOT DELETE (HIDE IN GIT)
BaseURL = "http://api.openweathermap.org/data/2.5/forecast?"
OpenMainKey = "b12c5e04c89021d40208a84f66ebd3bb"

"""
https://myaccount.google.com/apppasswords?rapt=AEjHL4PeKvCmEp6mdvHUkNL4iW9wItaC4hNAPD-gFza2LDrglX5Ch1CZAnEnW_MIPbK9wQsMH3A1ZctxdOp1abYQC-47IDfrWQ
"""

f = open("AllActivities.json", "r")
data = json.load(f)
f.close()

b = open("PerfectDays.json", "r")
dataP = json.load(b)
b.close()

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += "\n"
        str1 += ele
    return str1

def getData():
    f = open("AllActivities.json", "r")
    data = json.load(f)
    return data

def getDataP():
    b = open("PerfectDays.json", "r")
    dataP = json.load(b)
    return dataP

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
    f = open("AllActivities.json", "r")
    data = json.load(f)
    f.close()
    msg['Subject'] = 'PerfectDay'
    msg['From'] = "smukhyala@gmail.com"
    msg['To'] = data["email"]
    #msg['From'] = "smukhyala@gmail.com"
    #FIX ABOVE
    #assign to variable from app.py, 25mukhyalas62@stu.smuhsd.org
    # Send the message via our own SMTP server.
    
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")

    try:   
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('smukhyala@gmail.com', 'vxxfqkakjrpaxykd')#random gibberish is google generated
        server.send_message(msg)
    except:
        with open("DaemonErrors.log", "a") as fp:
            fp.write("\nEmail error at " + current_time + ".")
            fp.close()
def job():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Starting job at", current_time)
    grabbedData = getData()
    grabbedDataP = getDataP()
    allActivities = []
    weatherEvaluation = []
    messageHeader = "Hello there " + data["user"] + "!\nWelcome back to PerfectDay. This is a reminder about each of your upcoming PerfectDays. Your PerfectDays are \n"
    messageFooter = "\n\nPlease contact smukhyala@gmail.com for any questions or support. Also, please leave a review and rating on your app store. Have a PerfectDay!\n\nThank you, \nSanjay Mukhyala, PerfectDay Team"
    for activity in grabbedData["activities"]:
    #Here: this forloop doesnt do what it needs to do
        try:
            goodDays = f'\n'.join(judgeWeather(activity))
            print(goodDays)
            weatherEvaluation.append(PerfectDaysFormatting(goodDays, activity["subtitle"]))
            allActivities.append({'title':f"{activity['ActivityChoice']} in {activity['CityChoice']}",'subtitle':goodDays,'icon':''}) #\nThank you, \n Sanjay Mukhyala, PerfectDay Team
            #weatherEvaluation = weatherEvaluation + PerfectDaysFormatting(goodDays)
        except Exception as e:
            weatherEvaluation = "Went bad"
            with open("DaemonErrors.log", "a") as fp:
                fp.write("\nCity error at " + current_time + ".")
                fp.close()

    finalmessage = messageHeader + '\n'.join(weatherEvaluation) + messageFooter
    sendMail(finalmessage)
    #f"Welcome back to PerfectDay. This is a reminder about each of your upcoming PerfectDay\n" + json.dumps(allActivities) "\nPlease contact smukhyala@gmail.com for any questions or support. Also, please leave a review and rating on your app store. Have a PerfectDay!\n\n - PerfectDay Team")
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
    #weatherData = fetchCityData(activityData["CityChoice"])
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    '''
    try:
        weatherData = fetchCityData(activityData["CityChoice"])
    except:
        weatherData = fetchCityData("San Francisco")
        with open("DaemonErrors.log", "w") as fp:
            fp.write("City error at " + current_time + ".")
            fp.close()
    '''
    weatherData = fetchCityData(activityData["CityChoice"])
    pp = pprint.PrettyPrinter(indent=4)
   
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
            goodDays.append(forecast['dt_txt'])
        elif goodConditionCount - badConditionCount == 2:
            weatherEvaluation = "decent, almost a PerfectDay."
        elif goodConditionCount - badConditionCount == 1:
            weatherEvaluation = "viable, somewhat a PerfectDay."
        elif goodConditionCount - badConditionCount < 1:
            weatherEvaluation = "suboptimal, not a PerfectDay. See another day's forecast or a different location."
    return goodDays

def PerfectDaysFormatting(newGoodDays, City):
    finalsubtitle = []
    newGoodDays = (newGoodDays.split("\n"))
    grabbedDataP = getDataP()
    for time in newGoodDays:
        #Day ending
        if time[9] == "1":
            time = time[:10] + "st," + time[10:]
        elif time[9] == "2":
            time = time[:10] + "nd," + time[10:]
        elif time[9] == "3":
            time = time[:10] + "rd," + time[10:]
        else:
            time = time[:10] + "th," + time[10:]

            #AM PM
        if time[-8] == "0":
            time = time[:16] + ":00 am"
        elif time[-8] == "1" and (time[-7] == "1"):
            time = time[:16] + ":00 am"
        elif time[-8] == "1" or time[-8] == "2":
            time = time[:16] + ":00 pm"
        
            #Miltary Standard Clock            
        if time[14] == "0" and time[15] == "0":
            time = time[:13] + " 12" + time[16:]
        elif time[14] == "1" and time[15] == "3":
            time = time[:13] + " 01" + time[16:]
        elif time[14] == "1" and time[15] == "4":
            time = time[:13] + " 02" + time[16:]
        elif time[14] == "1" and time[15] == "5":
            time = time[:13] + " 03" + time[16:]
        elif time[14] == "1" and time[15] == "6":
            time = time[:13] + " 04" + time[16:]
        elif time[14] == "1" and time[15] == "7":
            time = time[:13] + " 05" + time[16:]
        elif time[14] == "1" and time[15] == "8":
            time = time[:13] + " 06" + time[16:]
        elif time[14] == "1" and time[15] == "9":
            time = time[:13] + " 07" + time[16:]
        elif time[14] == "2" and time[15] == "0":
            time = time[:13] + " 08" + time[16:]
        elif time[14] == "2" and time[15] == "1":
            time = time[:13] + " 09" + time[16:]
        elif time[14] == "2" and time[15] == "2":
            time = time[:13] + " 10" + time[16:]
        elif time[14] == "2" and time[15] == "3":
            time = time[:13] + " 11" + time[16:]
            
            #Month
        if time[5] == "0" and time[6] == "1":
            time = " January " + time[8:] + ", " + time[:4]
        elif time[5] == "0" and time[6] == "2":
            time = " February " + time[8:] + ", " + time[:4]
        elif time[5] == "0" and time[6] == "3":
            time = " March " + time[8:] + ", " + time[:4]
        elif time[5] == "0" and time[6] == "4":
            time = " April " + time[8:] + ", " + time[:4]
        elif time[5] == "0" and time[6] == "5":
            time = " May " + time[8:] + ", " + time[:4]
        elif time[5] == "0" and time[6] == "6":
            time = " June " + time[8:] + ", " + time[:4]
        elif time[5] == "0" and time[6] == "7":
            time = " July " + time[8:] + ", " + time[:4]
        elif time[5] == "0" and time[6] == "8":
            time = " August " + time[8:] + ", " + time[:4]
        elif time[5] == "0" and time[6] == "9":
            time = " September " + time[8:] + ", " + time[:4]
        elif time[5] == "1" and time[6] == "0":
            time = " October " + time[8:] + ", " + time[:4]
        elif time[5] == "1" and time[6] == "1":
            time = " November " + time[8:] + ", " + time[:4]
        elif time[5] == "1" and time[6] == "2":
            time = " December " + time[8:] + ", " + time[:4]

        finalsubtitle.append(time + " for " + City + ".")
    
    return("\n".join(finalsubtitle))

schedule.every(10).seconds.do(job)
#schedule.every(2).hour.do(judgeWeather(activity))
#schedule.every().day.at("10:30").do(judgeWeather(activity))
#schedule.every().monday.do(judgeWeather(activity))
#schedule.every().wednesday.at("13:15").do(judgeWeather(activity))
#schedule.every().minute.at(":17").do(judgeWeather(activity))

while True:
    schedule.run_pending()
    time.sleep(1)
