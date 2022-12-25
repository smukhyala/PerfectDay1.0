from __future__ import print_function, unicode_literals, absolute_import
import random as ran
import math as math
import time as time
import requests as req
import datetime as dt
from threading import *
import subprocess
import json
import toga
from toga.style import Pack
from toga.style.pack import *
from toga.colors import *
from toga.fonts import *
import tempfile
from os.path import exists

dirpath = tempfile.mkdtemp()
file_exists = exists(dirpath + "AllActivities.json")

"""
PerfectDay, IOS app by Sanjay Mukhyala 2022.
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
"""

def hello():
    print("hello, world")

t = Timer(30.0, hello)
t.start()

#daemonLog = subprocess.Popen(["python", "src/hello/daemon.py"], close_fds = True)

user_name = "Default"
goodConditionCount = 0
badConditionCount = 0
weatherEvaluation = ""

### API INFORMATION DO NOT DELETE (HIDE IN GIT)
BaseURL = "http://api.openweathermap.org/data/2.5/forecast?"
OpenMainKey = "b12c5e04c89021d40208a84f66ebd3bb"

def fetchCityData(City):
    NewURL = BaseURL + "appid=" + OpenMainKey + "&q=" + City
    APIRequest = req.get(NewURL).json()
    return(APIRequest)

### Open and read the file after the appending
dirname = tempfile.TemporaryDirectory()
print(dirpath)
#
if file_exists:
    f = open(dirpath + "AllActivities.json", "r")
    data = json.load(f)
else:
    data = {
        "user": "Person",
        "email": "smukhyala@gmail.com",
        "activities": []
    }
user_name = data["user"]
user_email = "smukhyala@gmail.com"

def kelvin_to_fahrenheit(kelvin):
    fahrenheit = (kelvin - 273.15) * (9/5) + 32
    return fahrenheit

### TOGA CREATING UI
def build():
    ### Dictionary for reoccuring user defined data points (UPDATE: REMOVE)
    user_data = {
    "title": "",
    "subtitle": "",
    "icon": "",
    "HighTemp": 0,
    "LowTemp": 0,
    "HighWind": 0,
    "LowWind": 0,
    "HighHumidity": 0,
    "LowHumidity": 0,
    "ActivityChoice": "nothing",
    "CityChoice": "San Francisco"}

    ### Main content
    main_box = toga.Box(id = 'box', style = Pack(direction = "column"))
    BlockCreationBox = toga.Box()
    BlockCreationBox.style.update(direction = "column", padding=10, flex = 1)

    ### Name and Email components
    userNameChangeBox = toga.Box()
    userNameChangeBox.style.update(direction = "column", padding=10, flex = 1)

    nameInput = toga.TextInput(placeholder = "James Alan, John Smith, etc...")
    nameInput.style.update(width = 300, padding_left = 10)
    def updateNameText():
        user_name = nameInput.value
        data["user"] = user_name
        with open(dirpath + "AllActivities.json", "w") as fp:
            json.dump(data, fp, indent = 4)
        return(f'Hi {user_name}.\nChange your name:')
    nameLabel = toga.Label(f'Hi {user_name}.\nChange your name:', style=Pack(text_align = "left"))
    nameLabel.style.update(padding_left = 10, padding_right = 10)

    emailInput = toga.TextInput(placeholder = "james.alan99@gmail.com, JohnSmith123@hotmail.com, etc...")
    emailInput.style.update(width = 300, padding_left = 10)
    def changeEmailFunction(widget):
        user_email = emailInput.value
        data["email"] = user_email
        with open(dirpath + "AllActivities.json", "w") as fp:
            json.dump(data, fp, indent = 4)
        return(f'Change your email:')
    emailLabel = toga.Label(f'Hi {user_name}.\nChange your email:', style=Pack(text_align = "left"))
    emailLabel.style.update(padding_top = 10, padding_left = 10, padding_right = 10)
    
    def nameEmailLabelSaveFunction(widget):
        nameLabel.text = updateNameText()
        data["user"] = user_name
        nameInput.clear()
        emailLabel.text = changeEmailFunction(widget)
        data["email"] = user_email
        emailInput.clear()

    nameEmailLabelSaveButton = toga.Button("Save", on_press = nameEmailLabelSaveFunction)
    nameEmailLabelSaveButton.style.update(width = 300, padding_left = 10)

    ### Email + User
    def changeUserFunction(widget):
        if (len(BlockCreationBox.children) == 0):
            userNameChangeBox.add(nameLabel)
            userNameChangeBox.add(nameInput)
            userNameChangeBox.add(emailLabel)
            userNameChangeBox.add(emailInput)
            userNameChangeBox.add(nameEmailLabelSaveButton)
        changeUserButton.enabled = False
        main_box.add(userNameChangeBox)
    changeUserButton = toga.Button("Change User Details", on_press = changeUserFunction)
    changeUserButton.style.update(width = 300, padding = 10)

    ### City components
    cityInput = toga.TextInput(placeholder = "Brooklyn, Houston, etc...")
    cityInput.style.update(width = 300, padding_left = 10, padding_bottom = 10)
    def updateCityText():
        return(f'Your current city is {user_data["CityChoice"]} (default San Francisco).\nChange your city:')
    cityLabel = toga.Label(f'Your current city is {user_data["CityChoice"]} (default San Francisco).\nChange your city:', style=Pack(text_align = "left"))
    cityLabel.style.update(padding_left = 10, padding_right = 10, padding_top = 20)

    now = dt.datetime.now()
    current_time = now.strftime("%H:%M:%S")

    def cityLabelToResultsTextSaveFunction(widget):
        if cityInput.value != "":
            user_data["CityChoice"] = cityInput.value
        user_data["subtitle"] = user_data["CityChoice"]
        cityLabel.text = updateCityText()
        cityInput.clear()

    ### Activity components
    activityInput = toga.TextInput(placeholder = "Soccer, hiking, running, picnic, etc...")
    activityInput.style.update(width = 300, padding_left = 10, padding_bottom = 10)
    activityLabel = toga.Label('Add an activity:', style=Pack(text_align = "left"))
    activityLabel.style.update(padding_left = 10, padding_right = 10, padding_top = 20)
    def activityLabelSaveFunction(widget):
        user_data["ActivityChoice"] = activityInput.value
        user_data["title"] = user_data["ActivityChoice"]
        activityInput.clear()

    ### Acivity detailed list handling
    deleteNum = 0
    def selection_handler(widget, row):
        deleteNum = row
        return row
    activityList = toga.DetailedList(
        data = data["activities"],
        on_select = selection_handler)
    activityList.style.update(width = 300, height = 100, padding_left = 20, padding_bottom = 10)

    ### Delete buttons
    def deleteActivitiesFunction(widget):
        data["activities"].pop(deleteNum)
        activityList.data = data["activities"]
        with open(dirpath + "AllActivities.json", "w") as fp:
            json.dump(data, fp, indent = 4)

    deleteActivitiesButton = toga.Button("Delete", on_press = deleteActivitiesFunction)
    deleteActivitiesButton.style.update(width = 300, padding_left = 10, padding_bottom = 10)

    ### Uniqueness
    def activityUniqueness(activities, key):
        for blocks in activities:
            if key == blocks["ActivityChoice"] + blocks["CityChoice"]:
                return True

    ### Centralized Save Button
    def mainBlockSaveFunction(widget):
        nameEmailLabelSaveFunction(widget)
        activityLabelSaveFunction(widget)
        cityLabelToResultsTextSaveFunction(widget)

        ### Open and append the file
        f = open(dirpath + "AllActivities.json", "r")
        data = json.load(f)
        f.close()
        neededKey = user_data["ActivityChoice"] + user_data["CityChoice"]

        ### Checking uniqueness
        if(not(activityUniqueness(data["activities"], neededKey))):
            with open(dirpath + "AllActivities.json", "w") as fp:
                data["activities"].append(user_data)
                json.dump(data, fp, indent = 4)
                activityList.data = data["activities"]
        else:
            uniqueErrorLabel = toga.Label("Try again, you have entered the same combination of city and activity.")
            uniqueErrorLabel.style.update(padding = 100)
            uniqueErrorWindow = toga.Window()
            uniqueErrorWindow.app = toga.App('Hello', 'org.SanjayMukhyala.PerfectDay', startup = build)
            uniqueErrorWindow.content = uniqueErrorLabel
            uniqueErrorWindow.show()

    ### Displaying all active components
    main_box.add(activityList)
    main_box.add(deleteActivitiesButton)
    main_box.add(BlockCreationBox)
    main_box.add(changeUserButton)
   
    ErrorLogBox = toga.Box()
    ErrorLogBox.style.update(direction = "column", padding=10, flex = 1)

    file_exists_log = exists(dirpath + "DaemonErrors.log")
    if file_exists_log:
        f = open(dirpath + "DaemonErrors.log", "r")
        ErrorLogs = f.read()
        f.close()
    else:
        ErrorLogs = ""

    ErrorLogText = toga.Label(ErrorLogs)
    ErrorLogText.style.update(width = 300, padding = 10)
    ErrorLogBox.add(ErrorLogText)

    def showErrorLogFunction(widget):
        if (len(BlockCreationBox.children) == 0):
            ErrorLogBox.add(ErrorLogText)
        showErrorLogButton.enabled = False
        main_box.add(ErrorLogBox)
    showErrorLogButton = toga.Button("Show Error Log", on_press = showErrorLogFunction)
    showErrorLogButton.style.update(width = 300, padding = 10)

    def createNewActivityView(self, widget):
        if (len(BlockCreationBox.children) == 0):
            BlockCreationBox.add(activityLabel)
            BlockCreationBox.add(activityInput)
            BlockCreationBox.add(cityLabel)
            BlockCreationBox.add(cityInput)
            
            ### Defining all the user criteria with sliders
            highTempLabel = toga.Label("Your highest temperature: " + str(int(0)))
            highTempLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10, padding_top = 20)

            def highTempSliderFunction(widget):
                user_data["HighTemp"] = widget.value*100
                highTempLabel.text = "Your highest temperature: " + str(int(widget.value*100))

            highTempSlider = toga.Slider(on_change = highTempSliderFunction)
            highTempSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
            highTempSlider.tick_count = 101
            highTempSlider.value = 0.0

            BlockCreationBox.add(highTempLabel)
            BlockCreationBox.add(highTempSlider)

            lowTempLabel = toga.Label("Your lowest temperature: " + str(int(0)))
            lowTempLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)

            def lowTempSliderFunction(widget):
                user_data["LowTemp"] = widget.value*100
                lowTempLabel.text = "Your lowest temperature: " + str(int(widget.value*100))

            lowTempSlider = toga.Slider(on_change = lowTempSliderFunction)
            lowTempSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
            lowTempSlider.tick_count = 101
            lowTempSlider.value = 0.0

            BlockCreationBox.add(lowTempLabel)
            BlockCreationBox.add(lowTempSlider)

            highWindLabel = toga.Label("Your highest wind speed (m/s): " + str(int(0)))
            highWindLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)

            def highWindSliderFunction(widget):
                user_data["HighWind"] = widget.value*100
                highWindLabel.text = "Your highest wind speed (m/s): " + str(int(widget.value*100))

            highWindSlider = toga.Slider(on_change = highWindSliderFunction)
            highWindSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
            highWindSlider.tick_count = 101
            highWindSlider.value = 0.0

            BlockCreationBox.add(highWindLabel)
            BlockCreationBox.add(highWindSlider)

            lowWindLabel = toga.Label("Your lowest wind speed (m/s): " + str(int(0)))
            lowWindLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)

            def lowWindSliderFunction(widget):
                user_data["LowWind"] = widget.value*100
                lowWindLabel.text = "Your lowest wind speed (m/s): " + str(int(widget.value*100))

            lowWindSlider = toga.Slider(on_change = lowWindSliderFunction)
            lowWindSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
            lowWindSlider.tick_count = 101
            lowWindSlider.value = 0.0

            BlockCreationBox.add(lowWindLabel)
            BlockCreationBox.add(lowWindSlider)

            highHumidityLabel = toga.Label("Your highest temperature: " + str(int(0)))
            highHumidityLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)

            def highHumiditySliderFunction(widget):
                user_data["HighHumidity"] = widget.value*100
                highHumidityLabel.text = "Your highest humidity (%): " + str(int(widget.value*100))

            highHumiditySlider = toga.Slider(on_change = highHumiditySliderFunction)
            highHumiditySlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
            highHumiditySlider.tick_count = 101
            highHumiditySlider.value = 0.0

            BlockCreationBox.add(highHumidityLabel)
            BlockCreationBox.add(highHumiditySlider)

            lowHumidityLabel = toga.Label("Your lowest temperature: " + str(int(0)))
            lowHumidityLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)

            def lowHumiditySliderFunction(widget):
                user_data["LowHumidity"] = widget.value*100
                lowHumidityLabel.text = "Your lowest humidity (%): " + str(int(widget.value*100))

            lowHumiditySlider = toga.Slider(on_change = lowHumiditySliderFunction)
            lowHumiditySlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
            lowHumiditySlider.tick_count = 101
            lowHumiditySlider.value = 0.0

            BlockCreationBox.add(lowHumidityLabel)
            BlockCreationBox.add(lowHumiditySlider)
            ### Visual addition of the central save
            BlockCreationBox.add(mainBlockSave)

        showSliderButton.enabled = False
        main_box.add(BlockCreationBox)

    showSliderButton = toga.Button("New Activity",  on_press = createNewActivityView)
    showSliderButton.style.update(width = 300, padding = 10)
    main_box.add(showSliderButton)

    ### Using the centralized saving system
    def resetSliders(widget):
        mainBlockSaveFunction(widget)
        main_box.remove(BlockCreationBox)
        showSliderButton.enabled = True

    mainBlockSave = toga.Button("Save Preferences", on_press = resetSliders)
    mainBlockSave.style.update(width = 300, padding_left = 10, padding_right = 10, padding_top = 15)

    ### Judge Weather
    def judgeWeather(activityData):
        goodDays = []
        
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

        return goodDays

    allActivities = []
    for activity in data["activities"]:
        try:
            goodDays = ', '.join(judgeWeather(activity))
            weatherEvaluation = "Your PerfectDays are {}.{}".format(goodDays, "\n")
            allActivities.append({'title':f"{activity['ActivityChoice']} in {activity['CityChoice']}",'subtitle':goodDays,'icon':''})
        except Exception as e:
            with open("DaemonErrors.log", "a") as fp:
                fp.write("City error at " + current_time + ". Using San Francisco.")
                fp.close()

    verdictLabel = toga.DetailedList(
        data = allActivities)
    verdictLabel.style.update(width = 300, height = 300, padding_left = 10, padding_right = 10, padding_top = 10)

    ### Bottom-most verdict message
    main_box.add(verdictLabel)

    main_box.add(ErrorLogText)
    ### SCROLL CONTAINER DO NOT DELETE
    mainContainer = toga.ScrollContainer(content = main_box, horizontal = False, vertical = True)

    #mainWindow = toga.MainWindow(title = "Perfect Day")
    return mainContainer

class DemoApp(toga.App):
    main_box = None

    def startup(self):
        self.main_window = toga.MainWindow(title="PerfectDay")
        self.box = toga.Box()
        box = self.mainPage()
        self.container = toga.ScrollContainer()
        container = build()
        #self.container.add(container)
        self.main_window.content = build()
        self.box.add(box)
        self.main_window.content = self.box
        self.main_window.show()
        
        #self.main_window.show()

    def mainPage (self):
        box = toga.Box(style=Pack(direction=COLUMN))
        ### Welcome label
        label = toga.Label('PerfectDay\nOptimize your outdoor scheduling needs.\n\n')
        label.style.update(width = 300, padding = 10)
        box.add(label)
        button = toga.Button("Go to activity maker", on_press=self.handle_btn_goto_Activity)
        box.add(button)
        return box

    def ActivityMakerPage (self):
        user_data = {
        "title": "",
        "subtitle": "",
        "icon": "",
        "HighTemp": 0,
        "LowTemp": 0,
        "HighWind": 0,
        "LowWind": 0,
        "HighHumidity": 0,
        "LowHumidity": 0,
        "ActivityChoice": "nothing",
        "CityChoice": "San Francisco"}

        box = toga.Box()
        box.style.update(direction = "column", padding=10, flex = 1)

     ### Defining all the user criteria with sliders
        highTempLabel = toga.Label("Your highest temperature: " + str(int(0)))
        highTempLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10, padding_top = 20)

        def highTempSliderFunction(widget):
            user_data["HighTemp"] = widget.value*100
            highTempLabel.text = "Your highest temperature: " + str(int(widget.value*100))

        highTempSlider = toga.Slider(on_change = highTempSliderFunction)
        highTempSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
        highTempSlider.tick_count = 101
        highTempSlider.value = 0.0

        box.add(highTempLabel)
        box.add(highTempSlider)

        lowTempLabel = toga.Label("Your lowest temperature: " + str(int(0)))
        lowTempLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)

        def lowTempSliderFunction(widget):
            user_data["LowTemp"] = widget.value*100
            lowTempLabel.text = "Your lowest temperature: " + str(int(widget.value*100))

        lowTempSlider = toga.Slider(on_change = lowTempSliderFunction)
        lowTempSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
        lowTempSlider.tick_count = 101
        lowTempSlider.value = 0.0

       # box.add(lowTempLabel)
       # box.add(lowTempSlider)

        highWindLabel = toga.Label("Your highest wind speed (m/s): " + str(int(0)))
        highWindLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)

        def highWindSliderFunction(widget):
            user_data["HighWind"] = widget.value*100
            highWindLabel.text = "Your highest wind speed (m/s): " + str(int(widget.value*100))

        highWindSlider = toga.Slider(on_change = highWindSliderFunction)
        highWindSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
        highWindSlider.tick_count = 101
        highWindSlider.value = 0.0

        box.add(highWindLabel)
        box.add(highWindSlider)

        lowWindLabel = toga.Label("Your lowest wind speed (m/s): " + str(int(0)))
        lowWindLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)

        def lowWindSliderFunction(widget):
            user_data["LowWind"] = widget.value*100
            lowWindLabel.text = "Your lowest wind speed (m/s): " + str(int(widget.value*100))

        lowWindSlider = toga.Slider(on_change = lowWindSliderFunction)
        lowWindSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
        lowWindSlider.tick_count = 101
        lowWindSlider.value = 0.0

        box.add(lowWindLabel)
        box.add(lowWindSlider)

        highHumidityLabel = toga.Label("Your highest temperature: " + str(int(0)))
        highHumidityLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)

        def highHumiditySliderFunction(widget):
            user_data["HighHumidity"] = widget.value*100
            highHumidityLabel.text = "Your highest humidity (%): " + str(int(widget.value*100))

        highHumiditySlider = toga.Slider(on_change = highHumiditySliderFunction)
        highHumiditySlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
        highHumiditySlider.tick_count = 101
        highHumiditySlider.value = 0.0

        box.add(highHumidityLabel)
        box.add(highHumiditySlider)

        lowHumidityLabel = toga.Label("Your lowest temperature: " + str(int(0)))
        lowHumidityLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)

        def lowHumiditySliderFunction(widget):
            user_data["LowHumidity"] = widget.value*100
            lowHumidityLabel.text = "Your lowest humidity (%): " + str(int(widget.value*100))

        lowHumiditySlider = toga.Slider(on_change = lowHumiditySliderFunction)
        lowHumiditySlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
        lowHumiditySlider.tick_count = 101
        lowHumiditySlider.value = 0.0

        box.add(lowHumidityLabel)
        box.add(lowHumiditySlider)

        button = toga.Button("Go back home", on_press=self.handle_btn_goto_Main)
        box.add(button)
        return(box)
    
    def handle_btn_goto_Activity(self, widget):
        box = self.ActivityMakerPage()
        self.box.remove(self.box.children[0])
        self.box.add(box)

    def handle_btn_goto_Main(self, widget):
        box = self.mainPage()
        self.box.remove(self.box.children[0])
        self.box.add(box)

### Toga running main function + setup
def main():
    #return toga.App('Hello', 'org.SanjayMukhyala.PerfectDay', startup = build)
    return DemoApp()