import rumps
import webbrowser
import json
from AppKit import NSApp
from parsing import *
from cal_api import *


class ParseCalApp(rumps.App):
    def __init__(self):
        super(ParseCalApp, self).__init__("ParseCal")
        self.menu = ["Create Event", "View Recent Event"]
        self.icon = "./images/icon.png"
        self.template = None
        self.recent_event_id = None
        self.user_num = "0"
        self.cid = "primary"

        self.view_button = self.menu['View Recent Event']
        self.view_button.set_callback(None)

        self.user_config()

    def user_config(self):
        with open('user_config.json', 'r') as file:
            data = json.load(file)
        
        try:
            if int(data["USER_NUMBER"]) >= 0:
                self.user_num = int(data["USER_NUMBER"])
        except:
            print("Please enter a valid user number in user_config.json.")
            exit

        if data["CALENDAR_ID"] != "":
            self.cid = data["CALENDAR_ID"]

    @rumps.clicked("Create Event")
    def get_event_data(self, _):
        NSApp.activateIgnoringOtherApps_(True)

        window = rumps.Window(
            "Enter the event data in the textbox below", 
            "Create Event", 
            "", 
            "Enter", 
            "Cancel", 
            (400, 200),
            False
            )
        response = window.run()
        
        if int(response.clicked) == 1:
            event = parse_data(response.text)

            if event != None:
                event_status = add_event(event, self.cid)

                if event_status != "Error":
                    self.recent_event_id = event_status.strip("https://www.google.com/calendar/")

                    if self.view_button.callback is None:
                       self.view_button.set_callback(self.open_recent_event)
            else:
                window = rumps.Window(
                    "Event creation failed. Please try again.", 
                    "Create Event", 
                    "", 
                    "Enter", 
                    "Cancel", 
                    (400, 200),
                    False
                )

    def open_recent_event(self, _):
        if (self.recent_event_id != None):
            url = f"https://www.google.com/calendar/u/{self.user_num}/r/{self.recent_event_id}"
            webbrowser.open_new_tab(url)