"""
My testing facility.
"""
from __future__ import print_function, unicode_literals, absolute_import

import toga
from toga.style import Pack
from toga.style.pack import *

import random as ran
import math as math
import requests as req
import time as time
import datetime as dt

user_data = {
"HighTemp": 0,
"LowTemp": 0,
"HighWind": 0,
"LowWind": 0,
"HighHumidity": 0,
"LowHumidity": 0,
"ActivityChoice": "nothing",
"OriginalName": "nameless",
"CityChoice": "San Francisco",
"WeatherEvaluation": "nothing.",
"Preference": "fahrenheit"
}

#### Universally defined variables
goodConditionCount = 0
badConditionCount = 0
weatherEvaluation = ""

# Temperature
def kelvin_to_celcius_fahrenheit(kelvin):
    celcius = kelvin - 273.15
    fahrenheit = celcius * (9/5) + 32
    return celcius, fahrenheit

# Important
BaseURL = "http://api.openweathermap.org/data/2.5/weather?"
OpenMainKey = "b12c5e04c89021d40208a84f66ebd3bb"

name = user_data["OriginalName"]




def fetchCityData(City):
    NewURL = BaseURL + "appid=" + OpenMainKey + "&q=" + City
    return(req.get(NewURL).json())

weatherData = fetchCityData(user_data["CityChoice"])
# Defining and sorting through the dictionary
temp_kelvin = weatherData['main']['temp']
low_temp_kelvin = weatherData['main']['temp_min']
high_temp_kelvin = weatherData['main']['temp_max']
feels_temp_kelvin = weatherData['main']['feels_like']
humidity = weatherData['main']['humidity']
description = weatherData['weather'][0]['description']
sunrise = dt.datetime.utcfromtimestamp(weatherData['sys']['sunrise'] + weatherData['timezone'])
sunset = dt.datetime.utcfromtimestamp(weatherData['sys']['sunset'] + weatherData['timezone'])
wind_speed = weatherData['wind']['speed']

# Using the temperature conversion
temp_celcius, temp_fahrenheit = kelvin_to_celcius_fahrenheit(temp_kelvin)
feels_celcius, feels_fahrenheit = kelvin_to_celcius_fahrenheit(feels_temp_kelvin)
low_temp_celcius, low_temp_fahrenheit = kelvin_to_celcius_fahrenheit(low_temp_kelvin)
high_temp_celcius, high_temp_fahrenheit = kelvin_to_celcius_fahrenheit(high_temp_kelvin)


def build(app):

    ########### LOCATION AND BASIC WEATHER OUTPUT
    left_box = toga.Box()
    left_box.style.update(direction=COLUMN, padding=10, flex = 1)

    cityInput = toga.TextInput(placeholder = "Brooklyn, Houston, etc...")
    cityInput.style.update(width = 450, padding_left = 10, padding_bottom = 10)

    def updateCityText(user_data):
        return(f'Your current city is {user_data["CityChoice"]} (default San Francisco).\nChange your city:')

    cityLabel = toga.Label(f'Your current city is {user_data["CityChoice"]} (default San Francisco).\nChange your city:', style=Pack(text_align=LEFT))
    cityLabel.style.update(padding_left = 10, padding_right = 10, padding_top = 20)



    def updateResultsText(weatherData):
        City = user_data["CityChoice"]
        return(f"Weather Results:\n\nThe temperature in {City}: {temp_celcius:.2f} degrees Celcius or {temp_fahrenheit:.2f} degrees Fahrenheit.\n" +
            f"The temperature in {City} feels like: {feels_celcius:.2f} degrees Celcius or {feels_fahrenheit:.2f} degrees Fahrenheit.\n" +
            f"The lowest temperature in {City}: {low_temp_celcius:.2f} degrees Celcius or {low_temp_fahrenheit:.2f} degrees Fahrenheit.\n" +
            f"The highest temperature in {City}: {high_temp_celcius:.2f} degrees Celcius or {high_temp_fahrenheit:.2f} degrees Fahrenheit.\n" +
            f"The humidity in {City}: {weatherData['main']['humidity']}%.\n" +
            f"The wind Speed in {City}: {wind_speed} m/s.\n"+
            f"The general weather in {City} is {description}.\n" +
            f"The sun rises in {City} at {sunrise} AM local time.\n" +
            f"The sun sets in {City} at {sunset} PM local time.")

    resultstext = updateResultsText(weatherData)
    resultsLabel = toga.Label(resultstext)
    resultsLabel.style.update(direction = COLUMN, flex=1, padding = 10)

    def cityLabelToResultsTextSaveFunction(widget):
        user_data["CityChoice"] = cityInput.value
        weatherData = fetchCityData(cityInput.value)
        resultstext = updateResultsText(weatherData)
        resultsLabel.text = resultstext
        cityText = updateCityText(user_data)
        cityLabel.text = cityText

    searchButtonCity = toga.Button('Search', on_press = cityLabelToResultsTextSaveFunction)
    searchButtonCity.style.update(width = 100, padding_left = 10, padding_right = 10)





    activityInput = toga.TextInput(placeholder = "Soccer, hiking, running, picnic, etc...")
    activityInput.style.update(width = 450, padding_left = 10, padding_bottom = 10)

    def updateActivityText(user_data):
        return(f'Your current activity is {user_data["ActivityChoice"]}.\nChange your activity:')

    activityLabel = toga.Label(f'Your current activity is {user_data["ActivityChoice"]}.\nChange your activity:', style=Pack(text_align=LEFT))
    activityLabel.style.update(padding_left = 10, padding_right = 10, padding_top = 20)

    def activityLabelSaveFunction(widget):
        user_data["ActivityChoice"] = activityInput.value
        activityText = updateActivityText(user_data)
        activityLabel.text = activityText

    saveButtonActivity = toga.Button('Save', on_press = activityLabelSaveFunction)
    saveButtonActivity.style.update(width = 100, padding_left = 10, padding_right = 10)




    nameInput = toga.TextInput(placeholder = "James Alan, Johm Smith, etc...")
    nameInput.style.update(width = 450, padding_left = 10, padding_bottom = 10)

    def updateNameText(user_data):
        return(f'Welcome to PerfectDay. \nThis is a tool created to optimize your outdoor scheduling needs.\n\nYour current name is {user_data["OriginalName"]}.\nChange your name:')

    nameLabel = toga.Label(f'Welcome to PerfectDay. \nThis is a tool created to optimize your outdoor scheduling needs.\n\n' +
    f'Your current name is {user_data["OriginalName"]}.\nChange your name:', style=Pack(text_align=LEFT))
    nameLabel.style.update(padding_left = 10, padding_right = 10, padding_top = 0)

    def nameLabelSaveFunction(widget):
        user_data["OriginalName"] = nameInput.value
        nameText = updateNameText(user_data)
        nameLabel.text = nameText

    saveButtonName = toga.Button('Save', on_press = nameLabelSaveFunction)
    saveButtonName.style.update(width = 100, padding_left = 10, padding_right = 10)



    def celciusSaveFunction(widget):
        user_data["preference"] = "Celcius"

    def fahrenheitSaveFunction(widget):
        user_data["preference"] = "Fahrenheit"

    celciusButton = toga.Button('Celcius', on_press = celciusSaveFunction)
    celciusButton.style.update(padding_left = 10, width = 150, padding_top = 20)

    fahrenheitButton = toga.Button('Fahrenheit', on_press = fahrenheitSaveFunction)
    fahrenheitButton.style.update(padding_bottom = 20, width = 150, padding_left = 10)

    left_box.add(nameLabel)
    left_box.add(nameInput)
    left_box.add(saveButtonName)
    left_box.add(activityLabel)
    left_box.add(activityInput)
    left_box.add(saveButtonActivity)
    left_box.add(cityLabel)
    left_box.add(cityInput)
    left_box.add(searchButtonCity)
    left_box.add(celciusButton)
    left_box.add(fahrenheitButton)

    def locationFunction(widget):
        print("Location selection...")
    def conditionsFunction(widget):
        print("Conditions selection...")
    def settingsFunction(widget):
        print("Settings selection...")

    location = toga.Group("Location")
    conditions = toga.Group("Conditions")
    settings = toga.Group("Settings")

    executeLocationFunction = toga.Command(locationFunction, label = "Local Weather", icon = "/Users/sanjay/projects/python_coding/beeware/hello/src/hello/Icons/Weather.png", group = location)
    executeConditionsFunction = toga.Command(conditionsFunction, label = "Conditions", icon = "/Users/sanjay/projects/python_coding/beeware/hello/src/hello/Icons/QuestionMark.png", group = conditions)
    executeSettingsFunction = toga.Command(settingsFunction, label = "Settings", icon = "/Users/sanjay/projects/python_coding/beeware/hello/src/hello/Icons/Settings.png", group = settings)

    #####Displays
    main_box = toga.Box(id = 'box', style = Pack(direction = COLUMN))
    main_box.add(left_box)
    main_box.add(resultsLabel)
    app.commands.add(executeLocationFunction, executeConditionsFunction, executeSettingsFunction)
    #app.main_window.toolbar.add(executeLocationFunction, executeConditionsFunction, executeSettingsFunction)






    ############# CONDITIONS WITH SLIDERS
    highTempLabel = toga.Label("Your highest temperature: " + str(int(0)))
    highTempLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10, padding_top = 20)
    def highTempSliderFunction(widget):
        #print(int(widget.value*100))
        user_data["HighTemp"] = widget.value*100
        highTempLabel.text = "Your highest temperature: " + str(int(widget.value*100))
    highTempSlider = toga.Slider(on_change = highTempSliderFunction)
    highTempSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
    highTempSlider.tick_count = 101
    highTempSlider.value = 0.0
    main_box.add(highTempLabel)
    main_box.add(highTempSlider)

    lowTempLabel = toga.Label("Your lowest temperature: " + str(int(0)))
    lowTempLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)
    def lowTempSliderFunction(widget):
        #print(int(widget.value*100))
        user_data["LowTemp"] = widget.value*100
        lowTempLabel.text = "Your lowest temperature: " + str(int(widget.value*100))
    lowTempSlider = toga.Slider(on_change = lowTempSliderFunction)
    lowTempSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
    lowTempSlider.tick_count = 101
    lowTempSlider.value = 0.0
    main_box.add(lowTempLabel)
    main_box.add(lowTempSlider)

    highWindLabel = toga.Label("Your highest wind speed (m/s): " + str(int(0)))
    highWindLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)
    def highWindSliderFunction(widget):
        #print(int(widget.value*100))
        highWindLabel.text = "Your highest wind speed (m/s): " + str(int(widget.value*100))
    highWindSlider = toga.Slider(on_change = highWindSliderFunction)
    highWindSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
    highWindSlider.tick_count = 101
    highWindSlider.value = 0.0
    main_box.add(highWindLabel)
    main_box.add(highWindSlider)

    lowWindLabel = toga.Label("Your lowest wind speed (m/s): " + str(int(0)))
    lowWindLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)
    def lowWindSliderFunction(widget):
        #print(int(widget.value*100))
        lowWindLabel.text = "Your lowest wind speed (m/s): " + str(int(widget.value*100))
    lowWindSlider = toga.Slider(on_change = lowWindSliderFunction)
    lowWindSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
    lowWindSlider.tick_count = 101
    lowWindSlider.value = 0.0
    main_box.add(lowWindLabel)
    main_box.add(lowWindSlider)

    highHumidityLabel = toga.Label("Your highest temperature: " + str(int(0)))
    highHumidityLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)
    def highHumiditySliderFunction(widget):
        #print(int(widget.value*100))
        highHumidityLabel.text = "Your highest humidity (%): " + str(int(widget.value*100))
    highHumiditySlider = toga.Slider(on_change = highHumiditySliderFunction)
    highHumiditySlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
    highHumiditySlider.tick_count = 101
    highHumiditySlider.value = 0.0
    main_box.add(highHumidityLabel)
    main_box.add(highHumiditySlider)

    lowHumidityLabel = toga.Label("Your lowest temperature: " + str(int(0)))
    lowHumidityLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)
    def lowHumiditySliderFunction(widget):
        #print(int(widget.value*100))
        lowHumidityLabel.text = "Your lowest humidity (%): " + str(int(widget.value*100))
    lowHumiditySlider = toga.Slider(on_change = lowHumiditySliderFunction)
    lowHumiditySlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
    lowHumiditySlider.tick_count = 101
    lowHumiditySlider.value = 0.0
    main_box.add(lowHumidityLabel)
    main_box.add(lowHumiditySlider)


    saveButton = toga.Button("Save", on_press = judgeWeather(build))
    saveButton.style.update(width = 100, padding_left = 10, padding_right = 10, padding_top = 10)

    verdictLabel = toga.Label("Our verdict is" + weatherEvaluation)

    main_box.add(saveButton)












    ###################    CONTAINERS
    mainContainer = toga.ScrollContainer(content=main_box, horizontal = False, vertical = True)

    #mainContainer.add('Location', main_box)
    #mainContainer.add('Conditions', cbox)
    return mainContainer

    """
    Construct and show the Toga application.

    Usually, you would add your application to a main content box.
    We then create a main window (with a name matching the app), and
    show the main window.
    """



def main():
    return toga.App('Hello', 'org.SanjayMukhyala.PerfectDay', startup = build)

if __name__ == '__main__':
    main().main_loop()


#### Main function
def judgeWeather(build):
    # Intro
    #ok = req.response
    print("we are in!")
    # Counts
    goodConditionCount = 0
    badConditionCount = 0

    #### Acheiving criteria through user input
    activity = user_data["ActivityChoice"]
    idealLowTemp = user_data["LowTemp"]
    idealHighTemp = user_data["HighTemp"]
    idealLowWindSpeed = user_data["LowWind"]
    idealHighWindSpeed = user_data["HighWind"]
    idealLowHumidity = user_data["LowHumidity"]
    idealHighHumidity = user_data["HighHumidity"]

    #### Defining good and bad weather occurences for the specifed user-criteria (chosen above)
    preference = user_data["Preference"]#input("\nWould you like fahrenheit or celcius? Please enter in lowecase text only with the provided spelling: ")


    # Temperature
    if preference == "fahrenheit":
        if (int(idealLowTemp) <= low_temp_fahrenheit) and (high_temp_fahrenheit <= int(idealHighTemp)):
            goodConditionCount = goodConditionCount + 2
            #badConditionCount = badConditionCount
        elif (int(idealLowTemp) <= low_temp_fahrenheit) and (int(idealHighTemp) < high_temp_fahrenheit):
            goodConditionCount = goodConditionCount + 1
            badConditionCount = badConditionCount + 1
        elif (low_temp_fahrenheit < int(idealLowTemp)) and (high_temp_fahrenheit <= int(idealHighTemp)):
            goodConditionCount = goodConditionCount + 1
            badConditionCount = badConditionCount + 1
        elif (low_temp_fahrenheit < int(idealLowTemp)) and (int(idealHighTemp) < high_temp_fahrenheit):
            #goodConditionCount = goodConditionCount
            badConditionCount = badConditionCount + 2

    elif preference == "celcius":
        if (int(idealLowTemp) <= low_temp_celcius) and (high_temp_celcius <= int(idealHighTemp)):
            goodConditionCount = goodConditionCount + 2
            #badConditionCount = badConditionCount
        elif (int(idealLowTemp) <= low_temp_celcius) and (int(idealHighTemp) < high_temp_celcius):
            goodConditionCount = goodConditionCount + 1
            badConditionCount = badConditionCount + 1
        elif (low_temp_celcius < int(idealLowTemp)) and (high_temp_celcius <= int(idealHighTemp)):
            goodConditionCount = goodConditionCount + 1
            badConditionCount = badConditionCount + 1
        elif (low_temp_celcius < int(idealLowTemp)) and (int(idealHighTemp) < high_temp_celcius):
            #goodConditionCount = goodConditionCount
            badConditionCount = badConditionCount + 2

    else:
        print("Incorrect input, we will use measurements in fahrenheit.")
        preference = "fahrenheit"

    # Other forecasts
    if (int(idealLowWindSpeed)) <= wind_speed <= (int(idealHighWindSpeed)):
        goodConditionCount = goodConditionCount + 1
        #badConditionCount = badConditionCount
    elif (wind_speed < (int(idealLowWindSpeed))) or ((int(idealHighWindSpeed)) < wind_speed):
        #goodConditionCount = goodConditionCount
        badConditionCount = badConditionCount + 1

    if (int(idealLowHumidity)) <= humidity <= (int(idealHighHumidity)):
        goodConditionCount = goodConditionCount + 1
        #badConditionCount = badConditionCount
    elif (humidity < (int(idealLowHumidity))) or ((int(idealHighHumidity)) < humidity):
        #goodConditionCount = goodConditionCount
        badConditionCount = badConditionCount + 1

    # Determining optimality of the conditions
    if goodConditionCount - badConditionCount >= 3:
        weatherEvaluation = "optimal!"
    elif goodConditionCount - badConditionCount == 2:
        weatherEvaluation = "decent."
    elif goodConditionCount - badConditionCount == 1:
        weatherEvaluation = "viable."
    elif goodConditionCount - badConditionCount < 1:
        weatherEvaluation = "suboptimal, see another day's forecast or a different location."

    print(f"Our verdict is {weatherEvaluation}")
