import json
import urllib.request


def send_webhook(webhook_url, content, payload):
    data = {**payload,
            "content": content}

    print("Sending webhook to " + webhook_url)

    params = json.dumps(data).encode('UTF-8')
    req = urllib.request.Request(webhook_url, data=params,
                                 headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)


def handle_events(events, trajectory):
    for event in events:
        connection = event['connection']

        # Message basis
        message = f"{connection['departure']['station']} ({event['departure_time']}) > {connection['arrival']['station']}"

        if "vias" in connection:
            vias = list(
                map(lambda via: f"{via['station']} ({via['arrival']['direction']['name']})",
                    connection["vias"]["via"]))
            message = message + "\nvia " + ", ".join(vias)

        if event["type"] == "delay":
            message = message + f"\n{event['value']} minuten vertraging"
        elif event["type"] == "cancellation":
            message = message + "\ntrein geschrapt"
        elif event["type"] == "alert":
            message = message + f"\nmededeling:\n{event['value']}"

        if "notifications" not in trajectory:
            continue

        if trajectory["notifications"]["type"] == "webhook":
            send_webhook(trajectory["notifications"]["endpoint"],
                         message, trajectory["notifications"]["payload"])
