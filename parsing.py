import os
from dotenv import load_dotenv
import google.generativeai as genai
import re
import ast

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


def parse_data(data):
    prompt = """
    Take this data and extract event data in the following format as shown in the example below. 
    in any part of the user's inputted text, make sure to replace double quotes with single quotes. return only the text in this format, nothing more:
    event = {
        "summary": "Meeting with GPT",
        "location": "123 AI Lane",
        "description": "Discuss project details.",
        "start": {"dateTime": "2024-09-30T10:00:00", "timeZone": "America/New_York"},
        "end": {"dateTime": "2024-09-30T11:00:00", "timeZone": "America/New_York"},
    }
    If any of the fields are missing, just say which ones, and if the data has nothing to do with an event, 
    just say something like "please pass in the event data you would like to create an event for" or something
    here is the data: \n
    """ + data
    response = model.generate_content(prompt)

    dict_match = re.search(r'event\s*=\s*({.*})', response.text, re.DOTALL)

    if dict_match:
        event_dict_str = dict_match.group(1)
        event = ast.literal_eval(event_dict_str)
        return event
        
    else:
        return None
    