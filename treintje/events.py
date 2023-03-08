from datetime import datetime
import pytz
import math

import irail.api

timezone = pytz.timezone('Europe/Brussels')


def create_event(departure_time, event_type, event_value=None):
    return {"departure_time": departure_time, "type": event_type, "value": event_value}


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
            #continue

        delay = math.ceil(int(connection["departure"]["delay"]) / 60)
        if delay > 0:
            events.append(create_event(departure_time, "delay", delay))

        cancelled = int(connection["departure"]["canceled"])
        if cancelled > 1:
            events.append(create_event(departure_time, "cancelled"))

    return events
