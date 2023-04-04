import os
from datetime import datetime

from urllib.parse import urlparse
import aiohttp


class GrafanaAnnotations:
    headers = None
    base_url = None

    def __init__(self) -> None:
        self.headers = {
            "Authorization": f"Bearer {os.environ['GRAFANA_API_KEY']}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        u = urlparse(os.environ["GRAFANA_URL"])
        self.base_url = f"{u.scheme}://{u.netloc}"

    async def the_latest_annotation_date_time(self):
        params = {"limit": 1, "tags": "google-calendar"}

        async with aiohttp.ClientSession(
            base_url=self.base_url, headers=self.headers
        ) as session:
            async with session.get(
                "/api/annotations", params=params, ssl=False
            ) as response:
                print("Status:", response.status)

                annotations = await response.json()

                if annotations and len(annotations) > 0:
                    latest = annotations[0]
                    created_epoch_datetime_in_ms = int(latest["created"])
                    created_epoch = created_epoch_datetime_in_ms / 1000
                    latest_date_time = datetime.fromtimestamp(created_epoch)

                    print(f"The latest annotation is from {latest_date_time}")

                    return latest_date_time

    async def get_annotation(self, event_id):
        params = {"limit": 1, "tags": event_id}

        async with aiohttp.ClientSession(
            base_url=self.base_url, headers=self.headers
        ) as session:
            async with session.get(
                "/api/annotations", params=params, ssl=False
            ) as response:
                print(f"Getting annotations with tag {event_id}. {response.status}")

                annotations = await response.json()

                if annotations and len(annotations) > 0:
                    latest = annotations[0]

                    return latest
                else:
                    print(f"Annotation with tag {event_id} not found.")

    async def update_annotation(self, annotation, event):
        annotation_id = annotation["id"]

        if event["status"] == "cancelled":
            async with aiohttp.ClientSession(
                base_url=self.base_url, headers=self.headers
            ) as session:
                async with session.delete(
                    f"/api/annotations/{annotation_id}", ssl=False
                ) as response:
                    print(
                        f"Deleting annotation {annotation_id}. Status: {response.status}"
                    )
        else:
            updated_annotation = self._create_annotation_from_event(event)

            if (
                annotation["time"] == updated_annotation["time"]
                and annotation["timeEnd"] == updated_annotation["timeEnd"]
                and annotation["text"] == updated_annotation["text"]
                and annotation["tags"] == updated_annotation["tags"]
            ):
                print(f"Annotation {annotation_id} has not changed.")
                return

            async with aiohttp.ClientSession(
                base_url=self.base_url, headers=self.headers
            ) as session:
                async with session.put(
                    f"/api/annotations/{annotation_id}",
                    json=updated_annotation,
                    ssl=False,
                ) as response:
                    print(
                        f"Updating annotation {annotation_id} with {updated_annotation}. Status: {response.status}"
                    )

    async def add_annotation(self, event):
        annotation = self._create_annotation_from_event(event)
        async with aiohttp.ClientSession(
            base_url=self.base_url, headers=self.headers
        ) as session:
            async with session.post(
                "/api/annotations", json=annotation, ssl=False
            ) as response:
                print(f"Creating annotation {annotation}. Status: {response.status}")

    def _create_annotation_from_event(self, event):
        start = int(
            datetime.fromisoformat(event["start"]["dateTime"]).timestamp() * 1000
        )
        end = int(datetime.fromisoformat(event["end"]["dateTime"]).timestamp() * 1000)

        return {
            "time": start,
            "timeEnd": end,
            "text": f"{event['summary']} by {event['creator']['email']}",
            "tags": ["google-calendar", event["id"]],
        }
