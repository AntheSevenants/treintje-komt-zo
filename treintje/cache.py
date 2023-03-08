import json
import time

def create_cache_filename(from_station, to_station):
    return f"cache_{from_station}_{to_station}.json"

def save_cache(from_station, to_station, events):
    cache = {"time": str(time.time()), "events": events}

    cache_filename = create_cache_filename(from_station, to_station)
    with open(cache_filename, "wt") as writer:
        writer.write(json.dumps(cache))