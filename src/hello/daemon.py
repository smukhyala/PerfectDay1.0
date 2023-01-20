import schedule
import time
import json
import requests as req
import datetime
import smtplib
import tempfile
from email.message import EmailMessage
from os.path import exists

### API INFORMATION DO NOT DELETE (HIDE IN GIT)
BaseURL = "http://api.openweathermap.org/data/2.5/forecast?"
OpenMainKey = "b12c5e04c89021d40208a84f66ebd3bb"

"""
https://myaccount.google.com/apppasswords?rapt=AEjHL4PeKvCmEp6mdvHUkNL4iW9wItaC4hNAPD-gFza2LDrglX5Ch1CZAnEnW_MIPbK9wQsMH3A1ZctxdOp1abYQC-47IDfrWQ
"""

dirpath = tempfile.gettempdir()
file_exists = exists(dirpath + "AllActivities.json")
if file_exists:
    f = open(dirpath + "AllActivities.json", "r")
    data = json.load(f)
    f.close()
else:
    data = {
    "user": "User",
    "email": "smukhyala@gmail.com",
}

class Daemon():
    def listToString(self, s):
        str1 = ""
        for ele in s:
            str1 += "\n"
            str1 += ele
        return str1

    def getData(self):
        file_exists = exists(dirpath + "AllActivities.json")
        if file_exists:
            f = open(dirpath + "AllActivities.json", "r")
            data = json.load(f)
            #print("daemon" + dirpath + "AllActivities.json")
        else:
            data = {
                "user": "User",
                "email": "smukhyala@gmail.com",
}
        return data

    def fetchCityData(self, City):
        NewURL = BaseURL + "appid=" + OpenMainKey + "&q=" + City
        APIRequest = req.get(NewURL).json()
        return(APIRequest)

    def kelvin_to_fahrenheit(self, kelvin):
        fahrenheit = (kelvin - 273.15) * (9/5) + 32
        return fahrenheit

    def sendMail(self, content):
        msg = EmailMessage()
        msg.set_content(content)

        '''f = open(dirpath + "AllActivities.json", "r")
        data = json.load(f)
        f.close()'''

        msg['Subject'] = 'PerfectDay'
        msg['From'] = "smukhyala@gmail.com"
        msg['To'] = data["email"]
        
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        # Send the message via our own SMTP server.
        try:   
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('smukhyala@gmail.com', 'ubyhrajhjgjobelv')#random gibberish is google generated
            server.send_message(msg)
        except Exception as e:
            with open(dirpath + "DaemonErrors.log", "a") as fp:
                fp.write("Email error at " + current_time + " " + type(e) + ".")
                fp.close()

    def job(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Starting job at", current_time)
        grabbedData = self.getData()
        allActivities = []
        weatherEvaluation = []
        if "activities" in grabbedData.keys():
            messageHeader = "Hello there " + data["user"] + "!\nWelcome back to PerfectDay. This is a reminder about each of your upcoming PerfectDays. Your PerfectDays are \n\n"
            messageFooter = "\n\nPlease contact smukhyala@gmail.com for any questions or support. Also, please leave a review and rating on your app store. Have a PerfectDay!\n\nThank you, \nSanjay Mukhyala, PerfectDay Team"
            for activity in grabbedData["activities"]:
                try:
                    goodDays = f'\n'.join(self.judgeWeather(activity))
                    weatherEvaluation.append(self.PerfectDaysFormatting(goodDays, activity["title"], activity["subtitle"]))
                    allActivities.append({'title':f"{activity['ActivityChoice']} in {activity['CityChoice']}",'subtitle':goodDays,'icon':''})
                except Exception as e:
                    weatherEvaluation = "Unfortunately, we have ran into some issues processing your city request. Please check to make sure the information you entered is correct."
                    with open(dirpath + "DaemonErrors.log", "a") as fp:
                        fp.write("City error at " + current_time + ".")
                        fp.close()

            finalmessage = messageHeader + '\n'.join(weatherEvaluation) + messageFooter
            self.sendMail(finalmessage)
            f = open(dirpath + "PerfectDays.json", "w")
            json.dump(allActivities, f, indent = 4)
            f.close()

        else:
            firstMessageHeader = "Hello there " + data["user"] + "! Welcome to PerfectDay. It looks like you haven't made any activities yet. Please make your first activity in the PerfectDay app.\n\n"
            firstMessagefooter = "\n\nPlease contact smukhyala@gmail.com for any questions or support. Also, please leave a review and rating on your app store. Have a PerfectDay!\n\nThank you, \nSanjay Mukhyala, PerfectDay Team"
            finalmessage = firstMessageHeader + firstMessagefooter
            self.sendMail(finalmessage)

    def judgeWeather(self, activityData):
        goodDays = []

        goodConditionCount = 0
        badConditionCount = 0

        ### Using fetch and weather data
        weatherData = self.fetchCityData(activityData["CityChoice"])
    
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
            temp_fahrenheit = self.kelvin_to_fahrenheit(temp_kelvin)
            feels_fahrenheit = self.kelvin_to_fahrenheit(feels_temp_kelvin)
            low_temp_fahrenheit = self.kelvin_to_fahrenheit(low_temp_kelvin)
            high_temp_fahrenheit = self.kelvin_to_fahrenheit(high_temp_kelvin)

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
                goodDays.append(forecast['dt_txt'])

        return goodDays

    def PerfectDaysFormatting(self, newGoodDays, City, Activity):
        finalsubtitle = []
        newGoodDays = (newGoodDays.split("\n"))
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

            finalsubtitle.append(time + " for " + City + " in " + Activity + ".")
        
        return("\n".join(finalsubtitle))
