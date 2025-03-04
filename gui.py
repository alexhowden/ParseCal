import rumps
import webbrowser
import json
from AppKit import NSApp
from parsing import *
from cal_api import *

class ParseCalApp(rumps.App):
    def __init__(self, user_num, cid, event_color):
        super(ParseCalApp, self).__init__("ParseCal")
        self.menu = ["Create Event", "View Recent Event"]
        self.icon = "./images/icon.png"
        self.template = None
        self.recent_event_id = None
        self.user_num = user_num
        self.cid = cid
        self.event_color = event_color

        self.view_button = self.menu['View Recent Event']
        self.view_button.set_callback(None)

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
            event_list = parse_data(response.text)

            if event_list != None:
                for event in event_list:
                    event_status = add_event(event, self.cid, self.event_color)

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