import treintje.events
import treintje.cache
import treintje.messaging
import json
import argparse
import os.path
import time

parser = argparse.ArgumentParser(
    description='treintje-komt-zo - Get automatic notifications on NMBS/SNCB delays and cancelled trains')
parser.add_argument('trajectories_path', type=str,
                    help='Path to the JSON file containing the trajectories to be checked')
args = parser.parse_args()

if not os.path.exists(args.trajectories_path):
    raise FileNotFoundError("Trajectories file not found")

with open(args.trajectories_path, "rt") as reader:
    trajectories = json.loads(reader.read())

for trajectory in trajectories:
    from_station = trajectory["from"]
    to_station = trajectory["to"]

    trajectory_events = treintje.events.check(
        from_station, to_station, trajectory["departure_times"])

    time.sleep(1)

    different_events = treintje.cache.diff_cache(
        from_station, to_station, trajectory_events)
    
    treintje.messaging.handle_events(different_events, trajectory)

    treintje.cache.save_cache(
        from_station, to_station, trajectory_events)
