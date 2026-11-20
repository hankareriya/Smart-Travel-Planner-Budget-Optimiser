import heapq


def dijkstra(
    graph,
    source,
    weight="distance"
):
    distances = {
        node: float("inf")
        for node in graph
    }

    previous = {
        node: None
        for node in graph
    }

    if source not in graph:
        return distances, previous

    distances[source] = 0

    priority_queue = [
        (0, source)
    ]

    while priority_queue:

        current_distance, current_node = (
            heapq.heappop(priority_queue)
        )

        if current_distance > distances[
            current_node
        ]:
            continue

        for neighbour, edge_data in graph[
            current_node
        ].items():

            edge_weight = float(
                edge_data.get(
                    weight,
                    edge_data.get("distance", 0)
                )
            )

            new_distance = (
                current_distance
                + edge_weight
            )

            if new_distance < distances[
                neighbour
            ]:

                distances[neighbour] = (
                    new_distance
                )

                previous[neighbour] = (
                    current_node
                )

                heapq.heappush(
                    priority_queue,
                    (
                        new_distance,
                        neighbour
                    )
                )

    return distances, previous


def get_path(
    previous,
    source,
    destination
):
    path = []

    current = destination

    while current is not None:

        path.append(current)

        if current == source:
            break

        current = previous.get(
            current
        )

    path.reverse()

    if not path:
        return []

    if path[0] != source:
        return []

    return path