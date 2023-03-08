import treintje.events
import json
import argparse
import os.path

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
    trajectory_events = treintje.events.check(
        trajectory["from"], trajectory["to"], trajectory["departure_times"])
    print(trajectory_events)
