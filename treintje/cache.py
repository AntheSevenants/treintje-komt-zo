import json
import time
import json
import os.path


def create_cache_filename(from_station, to_station):
    return f"cache_{from_station}_{to_station}.json"


def save_cache(from_station, to_station, events):
    cache = {"time": int(time.time()), "events": events}

    cache_filename = create_cache_filename(from_station, to_station)
    with open(cache_filename, "wt") as writer:
        writer.write(json.dumps(cache))


def diff_cache(from_station, to_station, new_events):
    old_event_ids = []

    cache_filename = create_cache_filename(from_station, to_station)
    # Check cache if it exists
    if os.path.exists(cache_filename):
        with open(cache_filename, "rt") as reader:
            old_cache = json.loads(reader.read())

        old_event_ids = list(
            map(lambda event: event["id"], old_cache["events"]))
        
    # This list holds all new events which are different from the old events
    truly_new_events = []

    for new_event in new_events:
        if new_event["id"] in old_event_ids:
            # This is not new information
            continue

        truly_new_events.append(new_event)

    return truly_new_events
