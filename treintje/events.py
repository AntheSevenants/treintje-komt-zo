from datetime import datetime
import pytz

import irail.api

timezone = pytz.timezone('Europe/Brussels')

def check(from_station, to_station, checked_departure_times=[]):
    connections = irail.api.make_request(
        "connections", {"from": from_station, "to": to_station})

    if not "connection" in connections:
        raise KeyError("Required 'connection' key not found in iRail response")

    connections = connections["connection"]

    for connection in connections:
        departure_epoch = int(connection["departure"]["time"])
        timestamp = datetime.fromtimestamp(departure_epoch, timezone)
        departure_time = timestamp.strftime('%H:%M')

        if departure_time not in checked_departure_times:
            print("Skipping the", departure_time, "train; not in checked departures")
            continue

        if int(connection["departure"]["delay"]) > 0:
            print("Delay")
            # TODO: an event

        if int(connection["departure"]["canceled"]) > 1:
            print("Cancellation")
            # TODO: an event
