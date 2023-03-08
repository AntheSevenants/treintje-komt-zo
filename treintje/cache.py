import json
import time


def save_cache(from_station, to_station, events):
    cache = {"time": str(time.time()), "events": events}

    with open(f"cache_{from_station}_{to_station}.json", "wt") as writer:
        writer.write(json.dumps(cache))
