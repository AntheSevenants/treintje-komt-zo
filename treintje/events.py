from datetime import datetime
import pytz
import math
import zlib

import irail.api

timezone = pytz.timezone('Europe/Brussels')


def create_event(departure_time, connection, event_type, event_value=""):
    # Event ID will be used to check for new events in the cache
    event_id = zlib.crc32(
        f"{departure_time}{event_type}{event_value}".encode("UTF-8"))

    return {"departure_time": departure_time,
            "type": event_type,
            "value": event_value,
            "connection": connection,
            "id": event_id}


def check(from_station, to_station, checked_departure_times=[]):
    connections = irail.api.make_request(
        "connections", {"from": from_station, "to": to_station})

    if not "connection" in connections:
        raise KeyError("Required 'connection' key not found in iRail response")

    connections = connections["connection"]
    # This list holds all events for this connection
    events = []

    for connection in connections:
        departure_epoch = int(connection["departure"]["time"])
        timestamp = datetime.fromtimestamp(departure_epoch, timezone)
        departure_time = timestamp.strftime('%H:%M')

        if departure_time not in checked_departure_times:
            print("Skipping the", departure_time,
                  "train; not in checked departures")
            # continue

        delay = math.ceil(int(connection["departure"]["delay"]) / 60)
        if delay > 0:
            events.append(create_event(
                departure_time, connection, "delay", delay))

        cancelled = int(connection["departure"]["canceled"])
        if cancelled > 1:
            events.append(create_event(
                departure_time, connection, "cancelled"))

        if int(connection["alerts"]["number"]) > 0:
            for alert in connection["alerts"]["alert"]:
                alert_string = alert['lead']
                if "link" in alert:
                    alert_string += f"\n{alert['link']}"

                events.append(create_event(
                    departure_time, connection, "alert", alert_string))

    return events
