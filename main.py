from gui import *
from gmail_api import fetch_and_create_events
import json
import threading

if __name__ == "__main__":
    cid = ""
    with open('user_config.json', 'r') as file:
        data = json.load(file)
        
        try:
            if int(data["USER_NUMBER"]) >= 0:
                user_num = int(data["USER_NUMBER"])
        except:
            print("Please enter a valid user number in user_config.json.")
            exit()

        if data["CALENDAR_ID"] != "":
            cid = data["CALENDAR_ID"]

        event_color = data.get("EVENT_COLOR", "1")

    app = ParseCalApp(user_num, cid, event_color)
    
    email_thread = threading.Thread(target=fetch_and_create_events, args=(cid,event_color,))
    email_thread.daemon = True
    email_thread.start()
    
    app.run()