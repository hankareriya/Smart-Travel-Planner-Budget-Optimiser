from math import radians, sin, cos, sqrt, atan2


TRANSPORT_CONFIG = {
    "walk": {
        "speed_kmh": 5,
        "cost_per_km": 0
    },

    "bike": {
        "speed_kmh": 30,
        "cost_per_km": 8
    },

    "car": {
        "speed_kmh": 30,
        "cost_per_km": 20
    },

    "cab": {
        "speed_kmh": 28,
        "cost_per_km": 25
    },

    "auto": {
        "speed_kmh": 25,
        "cost_per_km": 18
    }
}


def haversine_distance(
    lat1,
    lon1,
    lat2,
    lon2
):
    if None in (
        lat1,
        lon1,
        lat2,
        lon2
    ):
        return 0

    earth_radius = 6371

    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return earth_radius * c


def get_transport_details(
    distance_km,
    transport_mode
):
    mode = str(
        transport_mode or "car"
    ).lower()

    config = TRANSPORT_CONFIG.get(
        mode,
        TRANSPORT_CONFIG["car"]
    )

    speed = config["speed_kmh"]

    if distance_km <= 0:
        return {
            "time": 0,
            "cost": 0
        }

    time_minutes = max(
        5,
        round(
            (distance_km / speed) * 60
        )
    )

    cost = round(
        distance_km
        * config["cost_per_km"]
    )

    return {
        "time": time_minutes,
        "cost": cost
    }


def add_edge(
    graph,
    source,
    destination,
    distance,
    time,
    cost
):
    graph[source][destination] = {
        "distance": distance,
        "time": time,
        "cost": cost
    }

    graph[destination][source] = {
        "distance": distance,
        "time": time,
        "cost": cost
    }


def build_graph(
    attractions,
    transport_mode="car"
):
    graph = {
        attraction["id"]: {}
        for attraction in attractions
        if attraction.get("id") is not None
    }

    valid = [
        attraction
        for attraction in attractions
        if attraction.get("latitude") is not None
        and attraction.get("longitude") is not None
    ]

    for source in valid:

        for destination in valid:

            if source["id"] == destination["id"]:
                continue

            distance = haversine_distance(
                source["latitude"],
                source["longitude"],
                destination["latitude"],
                destination["longitude"]
            )

            travel = get_transport_details(
                distance,
                transport_mode
            )

            add_edge(
                graph,
                source["id"],
                destination["id"],
                round(distance, 2),
                travel["time"],
                travel["cost"]
            )

    return graph