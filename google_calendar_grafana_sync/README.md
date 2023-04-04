### Sync Google Calendar events to Grafana annotations API

When you create, update or delete an event in Google Calendar, this app will do the same in Grafana (create, update or delete annotation with event title)


## Usage
1. Setup project that has access to Google Calendar API, but do not bother with OAuth credentials -> https://developers.google.com/calendar/api/quickstart/python
2. Setup service account on Google Cloud Console, steps can be found here https://developers.google.com/analytics/devguides/config/mgmt/v3/quickstart/service-py
3. Just inject to the app the following env variables:

```
export GOOGLE_PROJECT_ID=google-calendar-grafana-sync
export GOOGLE_PRIVATE_KEY_ID=asdfasdfasdfgsdfgc
export GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n......\n-----END PRIVATE KEY-----\n"
export GOOGLE_CLIENT_EMAIL=google-service-account-email@google-project-id-email.iam.gserviceaccount.com
export GOOGLE_CLIENT_ID=11111111111
export GOOGLE_SERVICE_ACCOUNT_ID=my-service-account-id
export GOOGLE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/my-service-account-id%blablabla-381912.iam.gserviceaccount.com
export GOOGLE_CALENDAR_ID=c_71asdfasdfasdfasfasdfasdfasdfasdfasdfasdfasdfasdfasdf@group.calendar.google.com
export GRAFANA_URL=https://grafana.internal.mywebsite.com
export GRAFANA_API_KEY=eyJrasdfasdfasdfasdfasfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfMX0=
```

4. Create virtual environment, ie. `pipenv install`, then `pipenv shell`, then `python__main__.py`