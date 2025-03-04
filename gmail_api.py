import os.path
import base64
import re
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from cal_api import add_event, authenticate
from parsing import parse_data
from googleapiclient.errors import HttpError
import json

TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'client_secret.json'
HISTORY_ID_FILE = 'history_id.json'

def load_history_id():
    if os.path.exists(HISTORY_ID_FILE):
        with open(HISTORY_ID_FILE, 'r') as file:
            return json.load(file).get('historyId')
    return None

def save_history_id(history_id):
    with open(HISTORY_ID_FILE, 'w') as file:
        json.dump({'historyId': history_id}, file)

def fetch_new_emails(service, start_history_id):
    try:
        response = service.users().history().list(userId='me', startHistoryId=start_history_id).execute()
        history_records = response.get('history', [])
        messages = []
        for record in history_records:
            if 'messagesAdded' in record:
                for message in record['messagesAdded']:
                    messages.append(message['message'])
        return messages, response.get('historyId')
    except HttpError as error:
        if error.resp.status == 404:
            print("History ID is too old, resetting.")
            return [], None
        else:
            raise

def extract_email_content(msg):
    if 'data' in msg['payload']['body']:
        return base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
    elif 'parts' in msg['payload']:
        for part in msg['payload']['parts']:
            if 'data' in part['body']:
                return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
    return ""

def fetch_and_create_events(cid, event_color):
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    start_history_id = load_history_id()

    while True:
        try:
            if start_history_id:
                messages, new_history_id = fetch_new_emails(service, start_history_id)
                if new_history_id:
                    save_history_id(new_history_id)
                    start_history_id = new_history_id
            else:
                messages = service.users().messages().list(userId='me', labelIds=['INBOX'], q='').execute().get('messages', [])
                if messages:
                    latest_message = messages[0]
                    msg = service.users().messages().get(userId='me', id=latest_message['id']).execute()
                    start_history_id = msg['historyId']
                    save_history_id(start_history_id)

            for msg in messages:
                try:
                    msg = service.users().messages().get(userId='me', id=msg['id']).execute()
                    email_content = extract_email_content(msg)
                    event_details_list = parse_data(email_content)
                    if event_details_list:
                        for event_details in event_details_list:
                            add_event(event_details, cid, event_color)
                except HttpError as error:
                    if error.resp.status == 429:
                        print("Rate limit exceeded. Waiting until the next minute...")
                        time.sleep(60)
                        continue
                    else:
                        print(f"An error occurred: {error}")
                        time.sleep(300)
                        continue

            time.sleep(10)

        except HttpError as error:
            print(f"An error occurred: {error}")
            time.sleep(300)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(300)