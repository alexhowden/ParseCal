import os
from dotenv import load_dotenv
import google.generativeai as genai
import re
import ast

load_dotenv()
genai.configure()
model = genai.GenerativeModel("gemini-2.0-flash")

def parse_data(data):
    prompt = """
    Take this data and extract event data in the following format as shown in the example below. 
    in any part of the user's inputted text, make sure to replace double quotes with single quotes. return only the text in this format, nothing more:
    events = [
        {
            "summary": "Meeting with GPT",
            "location": "123 AI Lane",
            "description": "Discuss project details.",
            "start": {"dateTime": "2024-09-30T10:00:00", "timeZone": "America/New_York"},
            "end": {"dateTime": "2024-09-30T11:00:00", "timeZone": "America/New_York"},
        },
        {
            "summary": "Lunch with AI",
            "location": "456 ML Road",
            "description": "Discuss AI advancements.",
            "start": {"dateTime": "2024-09-30T12:00:00", "timeZone": "America/New_York"},
            "end": {"dateTime": "2024-09-30T13:00:00", "timeZone": "America/New_York"},
        }
    ]
    If any of the fields are missing, just say which ones, and if the data has nothing to do with an event, 
    just say "please pass in the event data you would like to create an event for".
    Also, if the date of the event is in the past, just say that the event is expired and don't return an events dictionary.
    Here is the data: \n
    """ + data

    response = model.generate_content(prompt).text

    list_match = re.search(r'events\s*=\s*(\[.*\])', response, re.DOTALL)

    if list_match:
        events_list_str = list_match.group(1)
        events = ast.literal_eval(events_list_str)
        return events
    else:
        return None