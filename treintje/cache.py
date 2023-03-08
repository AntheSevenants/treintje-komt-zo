import json
import time
import json


def create_cache_filename(from_station, to_station):
    return f"cache_{from_station}_{to_station}.json"


def save_cache(from_station, to_station, events):
    cache = {"time": str(time.time()), "events": events}

    cache_filename = create_cache_filename(from_station, to_station)
    with open(cache_filename, "wt") as writer:
        writer.write(json.dumps(cache))


def diff_cache(from_station, to_station, new_events):
    cache_filename = create_cache_filename(from_station, to_station)
    with open(cache_filename, "rt") as reader:
        old_cache = json.loads(reader.read())

    # This list holds all new events which are different from the old events
    truly_new_events = []

    old_event_ids = list(map(lambda event: event["id"], old_cache["events"]))

    for new_event in new_events:
        if new_event["id"] in old_event_ids:
            # This is not new information
            continue

        truly_new_events.append(new_event)

    return truly_new_events