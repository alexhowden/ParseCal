# ParseCal

ParseCal is an application that allows you to automatically create Google Calendar events by simply copying and pasting a chunk of text into a window and hitting submit.
For example, if you received an email with details for an event, you could simply copy and paste the entire email (or just the relevant part), and it will instantly pop up in your calendar.
This project is designed to save time and energy, especially in situations where you have to create a series of events. It also reduces human error when creating such events.
The application is based around MacOS and runs in the menu bar at the top of the screen.

## Requirements

- You have the latest version of Python installed (will likely work if a few versions behind)
- You are using MacOS
- Helpful to have an Integrated Development Environment (VSCode, PyCharm, etc.)
- Helpful to be running in a virtual environment for package installations

## Installation

Download the source files either through GitHub (Code > Download ZIP) and then extract them,
or through the CLI with the following command:

```bash
git clone https://github.com/alexhowden/ParseCal.git
```

## Configuration

### Phase 1 - Creating a Google Cloud Project

This is necessary for getting the credentials required to automatically make Google calendar events.

Google has created a guide for this. Follow the directions in each step, and refer back to this documentation during the process for additional details.
After clicking the blue button in each step, ensure that you are logged into the correct Google account (top right) with the right project selected (top left).
[Get Started](https://developers.google.com/workspace/guides/get-started)

**[Step 1](https://developers.google.com/workspace/guides/create-project)**
Answer all of the fields. The specifics do not matter.

**[Step 2](https://developers.google.com/workspace/guides/enable-apis)**
Select "Google Calendar API" from the list, or type it in the search bar.
Click the blue "enable" button

**Skip step 3**

**[Step 4](https://developers.google.com/workspace/guides/configure-oauth-consent)**
User Type - External

1. App name does not matter. Use your email in both required parts.
2. Add Scopes
   - first three (ones without API field)
   - Type in "Google Calendar API" into the filter and select all. Note that there are two pages of them.
   - Update
3. Nothing to do here
4. Nothing to do here

**[Step 5](https://developers.google.com/workspace/guides/create-credentials)**
Follow the steps to create API key credentials and OAuth client ID credentials.
For the OAuth client ID credentials, select "Desktop app" for the application type.
Download the JSON file for the OAuth client credentials.
Rename this file as "client_secret.json" and move it to the project directory.

### Phase 2 - AI API Key

Go [here](https://aistudio.google.com/app/apikey) and sign in with your Google account.
Select Create API Key > Create API key in new project
Copy the API key

Back in your CLI, navigate to your project directory and run the following command:

```bash
echo "GEMINI_API_KEY='your_api_key_here'" >> .env
```

To verify that the API key was saved correctly, run:

```bash
cat .env
```

### Phase 3 - Calendar Selection

If your desired calendar loads when you visit [your calendar](https://calendar.google.com/calendar/), disregard this phase.

If your desired account is not the default account:

1. Visit [your calendar](https://calendar.google.com/calendar/) and switch to the desired account.
2. In the URL, take note of the number towards the end, which is your user number.
   - For example: my user number is 3, indicated by the "/u/3/r" in the url: https://calendar.google.com/calendar/u/3/r

If you have multiple calendars on the desired account and the desired calendar is not the default:

1. Visit [your calendar](https://calendar.google.com/calendar/) and switch to the desired account.
2. On the left side of the screen, find the calendar you want and hover over it.
3. Select the three dots > Settings and sharing
4. Select the "Get shareable link" button. It should be roughly a third of the way down the page.
5. Copy the string of letters and numbers at the end of the link after the "cid=". This is your Calendar ID.
6. Navigate back to the project directory. Open the "user_config.json" file. Modify the values as needed, otherwise leave them as they are.

### Phase 4 - Installing Packages

In the CLI, run this command:

```bash
pip install -r requirements.txt
```

**Congratulations! The hard part is over.**

## Usage

To use the application, run the `main.py` file. The first time you use the application, you will be prompted to authenticate with your Google account in a browser window.

Upon successful authentication, a calendar icon will appear in the Menu Bar at the top of your screen.

### Creating an Event

1. Copy the text containing the details for the event. This could be an email, paragraph, etc., as long as it contains all the necessary details to make a calendar event.
2. Click on the calendar icon in the Menu Bar and select "Create Event" from the dropdown.
3. The first time you create an event, the window may be hidden. Select the 'Python' application in your dock to bring it to the foreground.
4. Paste the text into the window and hit the "Enter" button.

The event will be created instantly.

### Viewing Recent Events

1. Click on the calendar icon in the Menu Bar and choose 'View Recent Event' from the dropdown.

This will open a link to the calendar event in your browser.

## Notes

Any and all feedback is greatly appreciated.

I will continue to make improvements to this project, so check back from time to time to see what's new.

Future Implementations:

- Support for event colors
