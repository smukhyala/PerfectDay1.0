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
#from deamon import Deamon
from os.path import exists

"""
PerfectDay, IOS app by Sanjay Mukhyala 2023.
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
"""

dirpath = tempfile.gettempdir()
user_name = "Default"
user_email = "default@example.com"




def hello(msg):
    print(msg + ", world")
    #replace with class from deamon.py

t = Timer(5, hello)
t.start()

class RepeatTimer(Timer):  
    def run(self):  
        while not self.finished.wait(self.interval):  
            self.function(*self.args,**self.kwargs)  
            print(' ')  

timer = RepeatTimer(1,hello,['Repeating'])  
timer.start()  
print('Threading started')  
time.sleep(20) #instances
print('Threading finishing')  
timer.cancel()
#tier runs then program runs - fix this




### TOGA CREATING UI
def buildUI():
    main_box = toga.Box(id = 'box', style = Pack(direction = "column"))
    mainContainer = toga.ScrollContainer(content = main_box, horizontal = False, vertical = True)
    return mainContainer

class DemoApp(toga.App):
    main_box = None
    mainData = None
    activitySelection = None

    def existingActivities(self):
        ### Open and append the file
        dirpath = tempfile.gettempdir()
        file_exists = exists(dirpath + "AllActivities.json")
        if file_exists:
            f = open(dirpath + "AllActivities.json", "r")
            dataP = json.load(f)
            f.close()
        else:
            dataP = {
                "user": "Person",
                "email": "smukhyala@gmail.com",
                "activities": [
                    {
                        "title": "EmailTestingOct11",
                        "subtitle": "Houston",
                        "icon": "",
                        "HighTemp": 100,
                        "LowTemp": 0.0,
                        "HighWind": 100,
                        "LowWind": 0.0,
                        "HighHumidity": 100,
                        "LowHumidity": 0.0,
                        "ActivityChoice": "EmailTestoct11",
                        "CityChoice": "Houston",
                        "user_name": "Default"
                    },
                    {
                        "title": "10/19/22",
                        "subtitle": "Brooklyn",
                        "icon": "",
                        "HighTemp": 91.00000262260437,
                        "LowTemp": 0.0,
                        "HighWind": 97.00000286102295,
                        "LowWind": 0.0,
                        "HighHumidity": 87.00000047683716,
                        "LowHumidity": 11.999999731779099,
                        "ActivityChoice": "10/19/22",
                        "CityChoice": "Brooklyn",
                        "user_name": "Default"
                    },
                    {
                        "title": "Nov7",
                        "subtitle": "Caracas",
                        "icon": "",
                        "HighTemp": 92.00000166893005,
                        "LowTemp": 15.000000596046448,
                        "HighWind": 89.99999761581421,
                        "LowWind": 10.000000149011612,
                        "HighHumidity": 85.00000238418579,
                        "LowHumidity": 18.000000715255737,
                        "ActivityChoice": "Nov7",
                        "CityChoice": "Caracas"
                    }
                ]
            }
        self.mainData = dataP

    def startup(self):
        #daemonLog = subprocess.Popen(["python", "src/hello/daemon.py"], close_fds = True)
        self.existingActivities()
        self.main_window = toga.MainWindow(title="PerfectDay")
        self.box = toga.Box()
        self.box.style.update(width = 500, height = 1000)
        box = self.mainPage()
        self.main_window.content = buildUI()
        self.box.add(box)
        self.main_window.content = self.box
        self.main_window.show()

    def mainPage (self):
        box = toga.Box(style=Pack(direction=COLUMN))
        label = toga.Label('PerfectDay')
        label.style.update(width = 300, padding = 10, alignment = 'center', font_size = 60)
        box.add(label)
        button = toga.Button("Go to activity maker", on_press=self.handle_btn_goto_Activity)
        button.style.update(width = 300, padding = 20, alignment = 'center', font_size = 18)
        box.add(button)
        button1 = toga.Button("Go to activity list", on_press=self.handle_btn_goto_ActivityList)
        button1.style.update(width = 300, padding = 20, alignment = 'center', font_size = 18)
        box.add(button1)
        button2 = toga.Button("Go to name/email", on_press=self.handle_btn_goto_NameEmail)
        button2.style.update(width = 300, padding = 20, alignment = 'center', font_size = 18)
        box.add(button2)
        button3 = toga.Button("Go to error log", on_press=self.handle_btn_goto_ErrorLog)
        button3.style.update(width = 300, padding = 20, alignment = 'center', font_size = 18)
        box.add(button3)
        return box

    def errorLog(self):
        file_exists_log = exists(dirpath + "DaemonErrors.log")
        if file_exists_log:
            f = open(dirpath + "DaemonErrors.log", "r")
            ErrorLogs = f.read()
            f.close()
        else:
            ErrorLogs = "All good!"
        box = toga.Box(style=Pack(direction=COLUMN))
        ErrorLabel = toga.Label('Current Error Log:')
        ErrorLabel.style.update(width = 300, padding = 10, alignment = 'center')
        ErrorLogText = toga.Label(ErrorLogs)
        ErrorLogText.style.update(width = 300, padding = 10, alignment = 'center')
        box.add(ErrorLabel)
        buttonBack = toga.Button("Go back home", on_press=self.handle_btn_goto_Main)
        buttonBack.style.update(width = 300, padding_left = 10, padding_right = 10, padding_top = 15)
        box.add(ErrorLogText)
        box.add(buttonBack)
        return(box)

    def yesNoDeletePerfect (self):
        box = toga.Box(style=Pack(direction=COLUMN))
        def deleteActivitiesFunction(widget):
            sel = self.activitySelection.value
            d = 0
            for myobj in self.mainData["activities"]:
                if myobj["title"] == sel:
                    self.mainData["activities"].pop(d)
                d += 1
            self.activitySelection.data = self.mainData["activities"]
            with open(dirpath + "AllActivities.json", "w") as fp:
                json.dump(self.mainData, fp, indent = 4)
            self.handle_btn_goto_Main(self.mainPage)
        label = toga.Label('Delete ' + self.activitySelection.value + '?')
        label.style.update(width = 300, padding = 10, alignment = 'center')
        yesButton = toga.Button("Yes", on_press=deleteActivitiesFunction)
        yesButton.style.update(width = 300, padding_left = 10, padding_right = 10, padding_top = 15)
        noButton = toga.Button("No", on_press=self.handle_btn_goto_Main)
        noButton.style.update(width = 300, padding_left = 10, padding_right = 10, padding_top = 15)
        box.add(label)
        box.add(yesButton)
        box.add(noButton)
        return(box)

    def totalActivitiesList (self):
        #data = self.data
        box = toga.Box(style=Pack(direction=COLUMN))
        deleteLabel = toga.Label('Select to delete:')
        deleteLabel.style.update(width = 300, padding = 10, alignment = 'center')
        activityList = toga.Selection(items = [d["title"] for d in self.mainData["activities"]], on_select = self.handle_btn_goto_DeletePerfect)
        activityList.style.update(width = 300, height = 100, padding_left = 20, padding_bottom = 10)
        self.activitySelection = activityList
        buttonBack = toga.Button("Go back home", on_press=self.handle_btn_goto_Main)
        buttonBack.style.update(width = 300, padding_left = 10, padding_right = 10, padding_top = 15)
        box.add(deleteLabel)
        box.add(activityList)
        box.add(buttonBack)
        #PerfectList = toga.Selection(items = )
        return(box)
    
    def editNameAndEmail (self):
        data = self.mainData
        box = toga.Box(style=Pack(direction=COLUMN))
        nameInput = toga.TextInput(placeholder = "James Alan, John Smith, etc...")
        nameInput.style.update(width = 300, padding_left = 10)
        def updateNameText():
            user_name = nameInput.value
            data["user"] = user_name
            with open(dirpath + "AllActivities.json", "w") as fp:
                json.dump(data, fp, indent = 4)
            return(f'Hi {user_name}.\nChange your name:')
        nameLabel = toga.Label(f'Hi {user_name}. Change your name:', style=Pack(text_align = "left"))
        nameLabel.style.update(padding_left = 10, padding_right = 10)
        emailInput = toga.TextInput(placeholder = "james.alan99@gmail.com, JohnSmith123@hotmail.com, etc...")
        emailInput.style.update(width = 300, padding_left = 10)
        def changeEmailFunction(widget):
            user_email = emailInput.value
            data["email"] = user_email
            with open(dirpath + "AllActivities.json", "w") as fp:
                json.dump(data, fp, indent = 4)
            return(f'Change your email:')
        emailLabel = toga.Label(f'Change your email:', style=Pack(text_align = "left"))
        emailLabel.style.update(padding_top = 10, padding_left = 10, padding_right = 10)
        def nameEmailLabelSaveFunction(widget):
            nameLabel.text = updateNameText()
            self.mainData["user"] = user_name
            nameInput.clear()
            emailLabel.text = changeEmailFunction(widget)
            self.mainData["email"] = user_email
            emailInput.clear()
        nameEmailLabelSaveButton = toga.Button("Save", on_press = nameEmailLabelSaveFunction)
        nameEmailLabelSaveButton.style.update(width = 300, padding_left = 10)
        box.add(nameLabel)
        box.add(nameInput)
        box.add(emailLabel)
        box.add(emailInput)
        box.add(nameEmailLabelSaveButton)
        buttonBack = toga.Button("Go back home", on_press=self.handle_btn_goto_Main)
        buttonBack.style.update(width = 300, padding_left = 10, padding_right = 10, padding_top = 15)
        box.add(buttonBack)
        return(box)

    def ActivityMakerPage (self):
        data = self.mainData
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
        highTempSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 10, padding_left = 10, width = 200)
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
        lowTempSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 10, padding_left = 10, width = 200)
        lowTempSlider.tick_count = 101
        lowTempSlider.value = 0.0
        box.add(lowTempLabel)
        box.add(lowTempSlider)
        highWindLabel = toga.Label("Your highest wind speed (m/s): " + str(int(0)))
        highWindLabel.style.update(flex = 1, padding_bottom = 5, padding_left = 10)
        def highWindSliderFunction(widget):
            user_data["HighWind"] = widget.value*100
            highWindLabel.text = "Your highest wind speed (m/s): " + str(int(widget.value*100))
        highWindSlider = toga.Slider(on_change = highWindSliderFunction)
        highWindSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 10, padding_left = 10, width = 200)
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
        lowWindSlider.style.update(flex = 1, padding_top = 10, padding_bottom = 10, padding_left = 10, width = 200)
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
        highHumiditySlider.style.update(flex = 1, padding_top = 10, padding_bottom = 10, padding_left = 10, width = 200)
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
        lowHumiditySlider.style.update(flex = 1, padding_top = 10, padding_bottom = 10, padding_left = 10, width = 200)
        lowHumiditySlider.tick_count = 101
        lowHumiditySlider.value = 0.0
        box.add(lowHumidityLabel)
        box.add(lowHumiditySlider)
        def activityUniqueness(activities, key):
            for blocks in activities:
                if key == blocks["ActivityChoice"] + blocks["CityChoice"]:
                    return True
        def selection_handler(widget, row):
            return row
        activityList = toga.DetailedList(
        data = data["activities"],
        on_select = selection_handler)
        activityList.style.update(width = 300, height = 100, padding_left = 20, padding_bottom = 5)
        cityInput = toga.TextInput(placeholder = "Brooklyn, Houston, etc...")
        cityInput.style.update(width = 300, padding_left = 10, padding_bottom = 5)
        def updateCityText():
            return(f'Your current city is {user_data["CityChoice"]}. Change your city:')
        cityLabel = toga.Label(f'Your current city is {user_data["CityChoice"]}. Change your city:', style=Pack(text_align = "left"))
        cityLabel.style.update(padding_left = 10, padding_right = 10, padding_top = 5)
        def cityLabelToResultsTextSaveFunction(widget):
            if cityInput.value != "":
                user_data["CityChoice"] = cityInput.value
            user_data["subtitle"] = user_data["CityChoice"]
            cityLabel.text = updateCityText()
            cityInput.clear()
        box.add(cityLabel)
        box.add(cityInput)
        activityInput = toga.TextInput(placeholder = "Soccer, hiking, running, picnic, etc...")
        activityInput.style.update(width = 300, padding_left = 10, padding_bottom = 10)
        activityLabel = toga.Label('Add an activity:', style=Pack(text_align = "left"))
        activityLabel.style.update(padding_left = 10, padding_right = 10, padding_top = 5)
        def activityLabelSaveFunction(widget):
            user_data["ActivityChoice"] = activityInput.value
            user_data["title"] = user_data["ActivityChoice"]
            activityInput.clear()        
        box.add(activityLabel)
        box.add(activityInput)
        def mainBlockSaveFunction(widget):
            activityLabelSaveFunction(widget)
            cityLabelToResultsTextSaveFunction(widget)
            neededKey = user_data["ActivityChoice"] + user_data["CityChoice"]
            if(not(activityUniqueness(data["activities"], neededKey))):
                with open(dirpath + "AllActivities.json", "w") as fp:
                    data["activities"].append(user_data)
                    json.dump(data, fp, indent = 4)
                    activityList.data = data["activities"]
            else:
                uniqueErrorLabel = toga.Label("Try again, you have entered the same combination of city and activity.")
                uniqueErrorLabel.style.update(padding = 100)
                uniqueErrorWindow = toga.Window()
                uniqueErrorWindow.app = toga.App('Hello', 'org.SanjayMukhyala.PerfectDay', startup = buildUI)
                uniqueErrorWindow.content = uniqueErrorLabel
                uniqueErrorWindow.show()
        def resetSliders(widget):
            mainBlockSaveFunction(widget)
            #showSliderButton.enabled = True
        mainBlockSave = toga.Button("Save Preferences", on_press = resetSliders)
        mainBlockSave.style.update(width = 300, padding_left = 10, padding_right = 10, padding_top = 5)
        buttonBack = toga.Button("Go back home", on_press=self.handle_btn_goto_Main)
        buttonBack.style.update(width = 300, padding = 10, padding_right = 10, padding_top = 5)
        box.add(mainBlockSave)
        box.add(buttonBack)
        return(box)
    
    def handle_btn_goto_Activity(self, widget):
        box = self.ActivityMakerPage()
        self.box.remove(self.box.children[0])
        self.box.add(box)
    
    def handle_btn_goto_ActivityList(self, widget):
        box = self.totalActivitiesList()
        self.box.remove(self.box.children[0])
        self.box.add(box)

    def handle_btn_goto_DeletePerfect(self, widget):
        box = self.yesNoDeletePerfect()
        self.box.remove(self.box.children[0])
        self.box.add(box)

    def handle_btn_goto_NameEmail(self, widget):
        box = self.editNameAndEmail()
        self.box.remove(self.box.children[0])
        self.box.add(box)

    def handle_btn_goto_ErrorLog(self, widget):
        box = self.errorLog()
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