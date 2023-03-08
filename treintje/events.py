import irail.api



def check(from_station, to_station):
    connections = irail.api.make_request(
        "connections", {"from": from_station, "to": to_station})
    
    if not "connection" in connections:
        raise KeyError("Required 'connection' key not found in iRail response")
    
    connections = connections["connection"]

    for connection in connections:
        if int(connection["departure"]["delay"]) > 0:
            print("Delay")
            # TODO: an event

        if int(connection["departure"]["canceled"]) > 1:
            print("Cancellation")
            # TODO: an event