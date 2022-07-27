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
import requests as req
import time as time
import datetime as dt

### Dictionary for reoccuring user defined data points
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
### Fixed value, do not interfere
"Preference": "Fahrenheit"
}

### Condition valuation counts + message string
goodConditionCount = 0
badConditionCount = 0
weatherEvaluation = ""

### Temperature conversion
def kelvin_to_fahrenheit(kelvin):
    fahrenheit = (kelvin - 273.15) * (9/5) + 32
    return fahrenheit

### API INFORMATION DO NOT DELETE + HIDE ME LATER
BaseURL = "http://api.openweathermap.org/data/2.5/weather?"
OpenMainKey = "b12c5e04c89021d40208a84f66ebd3bb"

def fetchCityData(City):
    NewURL = BaseURL + "appid=" + OpenMainKey + "&q=" + City
    return(req.get(NewURL).json())

weatherData = fetchCityData(user_data["CityChoice"])

### Defining and sorting through the dictionary values
temp_kelvin = weatherData['main']['temp']
low_temp_kelvin = weatherData['main']['temp_min']
high_temp_kelvin = weatherData['main']['temp_max']
feels_temp_kelvin = weatherData['main']['feels_like']
humidity = weatherData['main']['humidity']
description = weatherData['weather'][0]['description']
sunrise = dt.datetime.utcfromtimestamp(weatherData['sys']['sunrise'] + weatherData['timezone'])
sunset = dt.datetime.utcfromtimestamp(weatherData['sys']['sunset'] + weatherData['timezone'])
wind_speed = weatherData['wind']['speed']

### Using the temperature conversion
temp_fahrenheit = kelvin_to_fahrenheit(temp_kelvin)
feels_fahrenheit = kelvin_to_fahrenheit(feels_temp_kelvin)
low_temp_fahrenheit = kelvin_to_fahrenheit(low_temp_kelvin)
high_temp_fahrenheit = kelvin_to_fahrenheit(high_temp_kelvin)



















### TOGA CREATING UI
def build(app):
    ### Left box (main content)
    left_box = toga.Box()
    left_box.style.update(direction=COLUMN, padding=10, flex = 1)




    ### City components
    cityInput = toga.TextInput(placeholder = "Brooklyn, Houston, etc...")
    cityInput.style.update(width = 450, padding_left = 10, padding_bottom = 10)
    def updateCityText(user_data):
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




    ### Activity components
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




    ### Name components
    nameInput = toga.TextInput(placeholder = "James Alan, John Smith, etc...")
    nameInput.style.update(width = 450, padding_left = 10, padding_bottom = 10)
    def updateNameText(user_data):
        name = user_data["OriginalName"]
        return(f'Welcome to PerfectDay. \nThis is a tool created to optimize your outdoor scheduling needs.\n\nYour current name is {user_data["OriginalName"]}.\nChange your name:')
    nameLabel = toga.Label(f'Welcome to PerfectDay. \nThis is a tool created to optimize your outdoor scheduling needs.\n\n' +
    f'Your current name is {user_data["OriginalName"]}.\nChange your name:', style=Pack(text_align=LEFT))
    nameLabel.style.update(padding_left = 10, padding_right = 10, padding_top = 0)
    def nameLabelSaveFunction(widget):
        user_data["OriginalName"] = nameInput.value
        nameText = updateNameText(user_data)
        nameLabel.text = nameText




    ### Centralized Save Button
    def mainBlockSaveFunction(widget):
        nameLabelSaveFunction(widget)
        activityLabelSaveFunction(widget)
        cityLabelToResultsTextSaveFunction(widget)

    mainBlockSave = toga.Button("Final Save", on_press = mainBlockSaveFunction)
    mainBlockSave.style.update(width = 100, padding_left = 10, padding_right = 10, padding_top = 15)



    ### Adding each part to left box
    left_box.add(nameLabel)
    left_box.add(nameInput)
    left_box.add(activityLabel)
    left_box.add(activityInput)
    left_box.add(cityLabel)
    left_box.add(cityInput)

    left_box.add(mainBlockSave)

    ### Displaying all components
    main_box = toga.Box(id = 'box', style = Pack(direction = COLUMN))
    main_box.add(left_box)
    main_box.add(resultsLabel)









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
    main_box.add(highTempLabel)
    main_box.add(highTempSlider)




    lowTempLabel = toga.Label("Your lowest temperature: " + str(int(0)))
    lowTempLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)
    def lowTempSliderFunction(widget):
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
        user_data["HighWind"] = widget.value*100
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
        user_data["LowWind"] = widget.value*100
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
        user_data["HighHumidity"] = widget.value*100
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
        user_data["LowHumidity"] = widget.value*100
        lowHumidityLabel.text = "Your lowest humidity (%): " + str(int(widget.value*100))
    lowHumiditySlider = toga.Slider(on_change = lowHumiditySliderFunction)
    lowHumiditySlider.style.update(flex = 1, padding_top = 10, padding_bottom = 20, padding_left = 10)
    lowHumiditySlider.tick_count = 101
    lowHumiditySlider.value = 0.0
    main_box.add(lowHumidityLabel)
    main_box.add(lowHumiditySlider)


    def judgeWeather(dsfsdfsd):
        ### Intro (Just in case)
        print("We are in!")

        ### Counts
        goodConditionCount = 0
        badConditionCount = 0

        ### Assigning slider values to variables
        activity = user_data["ActivityChoice"]
        idealLowTemp = user_data["LowTemp"]
        idealHighTemp = user_data["HighTemp"]
        idealLowWindSpeed = user_data["LowWind"]
        idealHighWindSpeed = user_data["HighWind"]
        idealLowHumidity = user_data["LowHumidity"]
        idealHighHumidity = user_data["HighHumidity"]

        ### Open and append the file
        with open("PerfectDay.json", "a") as fp:
            json.dump(user_data, fp)

        ### Open and read the file after the appending
        f = open("PerfectDay.json", "r")

        ### Defining good and bad weather occurences for the specifed user-criteria (chosen above)
        ### Temperature
        preference = user_data["Preference"]
        if preference == "Fahrenheit":
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

        else:
            print("Incorrect input, we will use measurements in fahrenheit.")
            preference = "fahrenheit"

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
        elif goodConditionCount - badConditionCount == 2:
            weatherEvaluation = "decent, almost a PerfectDay."
        elif goodConditionCount - badConditionCount == 1:
            weatherEvaluation = "viable, somewhat a PerfectDay."
        elif goodConditionCount - badConditionCount < 1:
            weatherEvaluation = "suboptimal, not a PerfectDay. See another day's forecast or a different location."

        ### Just in case
        print(f"Our verdict is {weatherEvaluation}")
        user_data["WeatherEvaluation"] = f"Our verdict is {weatherEvaluation}"
        verdictLabel.text = user_data["WeatherEvaluation"]



    ############# FIX ME
    def updateVerdictText():
        weatherEvaluation = user_data["WeatherEvaluation"]
        return("Our verdict is " + weatherEvaluation)
    verdictText = updateVerdictText()
    verdictLabel = toga.Label(verdictText)
    verdictLabel.style.update(width = 1000, padding_left = 10, padding_right = 10, padding_top = 10)

    ### Saving criteria and displaying the verdict
    saveButton = toga.Button("Judge Weather", on_press = judgeWeather)
    saveButton.style.update(width = 150, padding_left = 10, padding_right = 10, padding_top = 10)

    main_box.add(saveButton)
    main_box.add(verdictLabel)




    ### SCROLL CONTAINER DO NOT DELETE
    mainContainer = toga.ScrollContainer(content = main_box, horizontal = False, vertical = True)
    return mainContainer

### Toga running main function + setup
def main():
    return toga.App('Hello', 'org.SanjayMukhyala.PerfectDay', startup = build)
if __name__ == '__main__':
    main().main_loop()



















### Main function and logic
