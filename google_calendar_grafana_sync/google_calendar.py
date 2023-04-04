from __future__ import print_function

import datetime
import os
import json

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


class GoogleCalendar:
    credentials = None
    calendar_id = None

    def __init__(self) -> None:
        self.calendar_id = os.environ["GOOGLE_CALENDAR_ID"]
        self.credentials = {
            "type": "service_account",
            "project_id": os.environ["GOOGLE_PROJECT_ID"],
            "private_key_id": os.environ["GOOGLE_PRIVATE_KEY_ID"],
            "private_key": os.environ["GOOGLE_PRIVATE_KEY"].replace("\\n", "\n"),
            "client_email": os.environ["GOOGLE_CLIENT_EMAIL"],
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.environ["GOOGLE_CLIENT_X509_CERT_URL"],
        }

        f = open("credentials.json", "w")
        f.write(json.dumps(self.credentials))
        f.close()

    def get_events(
        self, datetime_from: datetime.datetime, datetime_to: datetime.datetime
    ):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """

        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json", scopes=SCOPES
        )

        try:
            service = build("calendar", "v3", credentials=self.credentials)

            # Call the Calendar API
            print(f"Getting the events between {datetime_from} and {datetime_to}")

            x = service.calendarList().list().execute()
            print(x)

            events_result = (
                service.events()
                .list(
                    calendarId=self.calendar_id,
                    timeMin=datetime_from.isoformat() + "Z",
                    timeMax=datetime_to.isoformat() + "Z",
                    maxResults=100,
                    showDeleted=True,
                    singleEvents=False,
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return

            # Prints the start and name of the next 10 events
            return events

        except HttpError as error:
            print("An error occurred: %s" % error)
