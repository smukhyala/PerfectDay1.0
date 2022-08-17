"""
PerfectDay, IOS app by Sanjay Mukhyala summer 2022.
"""
### Imports
from __future__ import print_function, unicode_literals, absolute_import
import toga
import json
from toga.style import Pack
from toga.style.pack import *
import random as ran
import math as math
import time as time
import requests as req
import datetime as dt
import subprocess

daemonLog = subprocess.Popen(["python", "src/hello/daemon.py"], close_fds = True)

### Convenient globals
user_name = "nameless"
goodConditionCount = 0
badConditionCount = 0
weatherEvaluation = ""

### API INFORMATION DO NOT DELETE (HIDE IN GIT)
BaseURL = "http://api.openweathermap.org/data/2.5/forecast?"
OpenMainKey = "b12c5e04c89021d40208a84f66ebd3bb"

def fetchCityData(City):
    NewURL = BaseURL + "appid=" + OpenMainKey + "&q=" + City
    APIRequest = req.get(NewURL).json()
    #print(APIRequest)
    return(APIRequest)

### Open and read the file after the appending
f = open("AllActivities.json", "r")
data = json.load(f)
user_name = data["user"]
#print(json.dumps(data, indent=4, sort_keys=True))

### Temperature conversion
def kelvin_to_fahrenheit(kelvin):
    fahrenheit = (kelvin - 273.15) * (9/5) + 32
    return fahrenheit



### TOGA CREATING UI
def build(app):
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
    main_box = toga.Box(id = 'box', style = Pack(direction = COLUMN))
    BlockCreationBox = toga.Box()
    BlockCreationBox.style.update(direction=COLUMN, padding=10, flex = 1)

    ### Welcome label
    welcomeLabel = toga.Label('Welcome to PerfectDay. This is a tool created to optimize your outdoor scheduling needs.\n\n')
    welcomeLabel.style.update(width = 750, padding_left = 20, padding_bottom = 10, padding_top = 10)
    main_box.add(welcomeLabel)

    ### City components
    cityInput = toga.TextInput(placeholder = "Brooklyn, Houston, etc...")
    cityInput.style.update(width = 450, padding_left = 10, padding_bottom = 10)
    def updateCityText():
        return(f'Your current city is {user_data["CityChoice"]} (default San Francisco).\nChange your city:')
    cityLabel = toga.Label(f'Your current city is {user_data["CityChoice"]} (default San Francisco).\nChange your city:', style=Pack(text_align=LEFT))
    cityLabel.style.update(padding_left = 10, padding_right = 10, padding_top = 20)

    ### Results components
    def updateResultsText(weatherData):
        City = user_data["CityChoice"]
        return(f"Weather Results:\n\nThe temperature in {City}: {temp_fahrenheit:.2f} degrees Fahrenheit.\n" +
            f"The temperature in {City} feels like: {feels_fahrenheit:.2f} degrees Fahrenheit.\n" +
            f"The lowest temperature in {City}: {low_temp_fahrenheit:.2f} degrees Fahrenheit.\n" +
            f"The highest temperature in {City}: {high_temp_fahrenheit:.2f} degrees Fahrenheit.\n" +
            f"The humidity in {City}: {humidity}%.\n" +
            f"The wind speed in {City}: {wind_speed} m/s.\n"+
            f"The general weather in {City} is {description}.")
    def cityLabelToResultsTextSaveFunction(widget):
        if cityInput.value != "":
            user_data["CityChoice"] = cityInput.value
        user_data["subtitle"] = user_data["CityChoice"]
        weatherData = fetchCityData(user_data["CityChoice"])
        cityLabel.text = updateCityText()
        cityInput.clear()

    ### Activity components
    activityInput = toga.TextInput(placeholder = "Soccer, hiking, running, picnic, etc...")
    activityInput.style.update(width = 450, padding_left = 10, padding_bottom = 10)
    activityLabel = toga.Label('Add an activity:', style=Pack(text_align=LEFT))
    activityLabel.style.update(padding_left = 10, padding_right = 10, padding_top = 20)
    def activityLabelSaveFunction(widget):
        user_data["ActivityChoice"] = activityInput.value
        user_data["title"] = user_data["ActivityChoice"]
        activityInput.clear()

    ### Acivity detailed list handling
    def selection_handler(widget, row):
        #print('Row {} of widget {} was selected.'.format(row, widget))
        return row
    activityList = toga.DetailedList(
        data = data["activities"],
        on_select = selection_handler)
    activityList.style.update(width = 450, padding_left = 20, padding_bottom = 10)

    ### Delete buttons
    specifyRowDelete = selection_handler(activityList, 2)
    def deleteActivitiesFunction(widget):
        #print(f"Activity: {activityList.selection.ActivityChoice}. | City: {activityList.selection.CityChoice}.")
        data["activities"].pop(2)
        activityList.data = data["activities"]

    deleteActivitiesButton = toga.Button("Delete", on_press = deleteActivitiesFunction)
    deleteActivitiesButton.style.update(width = 150, padding_left = 10, padding_bottom = 10)

    ### Name components
    userNameChangeBox = toga.Box()
    userNameChangeBox.style.update(direction=COLUMN, padding=10, flex = 1)

    nameInput = toga.TextInput(placeholder = "James Alan, John Smith, etc...")
    nameInput.style.update(width = 450, padding_left = 10)
    def updateNameText():
        name = user_name
        data["user"] = user_name
        return(f'Hi {user_name}.\nChange your name:')
    nameLabel = toga.Label(f'Hi {user_name}.\nChange your name:', style=Pack(text_align=LEFT))
    nameLabel.style.update(padding_left = 10, padding_right = 10)
    def nameLabelSaveFunction(widget):
        user_name = nameInput.value
        nameLabel.text = updateNameText()
        nameInput.clear()
    nameLabelSaveButton = toga.Button("Save", on_press = nameLabelSaveFunction)
    nameLabelSaveButton.style.update(width = 200, padding_left = 10)

    def changeUserFunction(widget):
        if (len(BlockCreationBox.children) == 0):
            userNameChangeBox.add(nameLabel)
            userNameChangeBox.add(nameInput)
            userNameChangeBox.add(nameLabelSaveButton)
        changeUserButton.enabled = False
        main_box.add(userNameChangeBox)
    changeUserButton = toga.Button("Change User", on_press = changeUserFunction)
    changeUserButton.style.update(width = 200, padding = 10)

    ### Uniqueness
    def activityUniqueness(activities, key):
        for blocks in activities:
            #print(key, blocks["ActivityChoice"] + blocks["CityChoice"])
            if key == blocks["ActivityChoice"] + blocks["CityChoice"]:
                return True

    ### Centralized Save Button
    def mainBlockSaveFunction(widget):
        nameLabelSaveFunction(widget)
        activityLabelSaveFunction(widget)
        cityLabelToResultsTextSaveFunction(widget)

        ### Open and append the file
        f = open("AllActivities.json", "r")
        data = json.load(f)
        f.close()
        neededKey = user_data["ActivityChoice"] + user_data["CityChoice"]

        ### Checking uniqueness
        if(not(activityUniqueness(data["activities"], neededKey))):
            with open("AllActivities.json", "w") as fp:
                data["activities"].append(user_data)
                json.dump(data, fp, indent = 4)
                activityList.data = data["activities"]
        else:
            uniqueErrorLabel = toga.Label("Try again, you have entered the same combination of city and activity.")
            uniqueErrorLabel.style.update(padding = 100)
            uniqueErrorWindow = toga.Window()
            uniqueErrorWindow.app = toga.App('Hello', 'org.SanjayMukhyala.PerfectDay', startup = build)
            #uniqueErrorWindow.confirm_dialog(title = "Activity Error", message = "Try again, you have entered the same combination of city and activity.", on_result = None)
            uniqueErrorWindow.content = uniqueErrorLabel
            uniqueErrorWindow.show()

    ### Displaying all active components
    main_box.add(activityList)
    main_box.add(deleteActivitiesButton)
    main_box.add(BlockCreationBox)
    #main_box.add(changeUserButton)
    #main_box.add(resultsLabel)

    def createNewActivityView(widget):
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
    mainBlockSave.style.update(width = 250, padding_left = 10, padding_right = 10, padding_top = 15)


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

    allActivities = []
    for activity in data["activities"]:
        #print(f"Calling judgeWeather on {activity['CityChoice']}")
        goodDays = ', '.join(judgeWeather(activity))
        weatherEvaluation = "Your PerfectDays are {}.{}".format(goodDays, "\n")
        allActivities.append({'title':f"{activity['ActivityChoice']} in {activity['CityChoice']}",'subtitle':goodDays,'icon':''})
        #verdictLabel.text = verdictLabel.text + weatherEvaluation
        #print(goodDays)

    verdictLabel = toga.DetailedList(
        data = allActivities)
    verdictLabel.style.update(width = 1250, height = 500, padding_left = 10, padding_right = 10, padding_top = 10)

    ### Bottom-most verdict message
    main_box.add(verdictLabel)

    ### SCROLL CONTAINER DO NOT DELETE
    mainContainer = toga.ScrollContainer(content = main_box, horizontal = False, vertical = True)
    return mainContainer

### Toga running main function + setup
def main():
    return toga.App('Hello', 'org.SanjayMukhyala.PerfectDay', startup = build)
if __name__ == '__main__':
    main().main_loop()
