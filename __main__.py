from google_calendar_grafana_sync.grafana_annotations import GrafanaAnnotations
from google_calendar_grafana_sync.google_calendar import GoogleCalendar
import asyncio
import datetime


async def main():
    grafana = GrafanaAnnotations()
    calendar = GoogleCalendar()

    the_latest_annotation_date_time = await grafana.the_latest_annotation_date_time()

    if not the_latest_annotation_date_time:
        the_latest_annotation_date_time = datetime.datetime.now() - datetime.timedelta(
            days=3
        )

    events = calendar.get_events(
        the_latest_annotation_date_time,
        datetime.datetime.now() + datetime.timedelta(days=30),
    )

    if not events:
        return

    for event in events:
        annotation = await grafana.get_annotation(event["id"])

        if annotation:
            await grafana.update_annotation(annotation, event)
        elif event["status"] == "confirmed":
            await grafana.add_annotation(event)


if __name__ == "__main__":
    asyncio.run(main())
