from app.algorithms.dijkstra import dijkstra


def optimize_route(
    attractions,
    graph,
    optimization_mode="best experience"
):
    if not attractions:
        return []

    attraction_map = {
        attraction["id"]: attraction
        for attraction in attractions
    }

    remaining = set(
        attraction_map.keys()
    )

    current = max(
        attractions,
        key=lambda item: item.get("score", 0)
    )["id"]

    ordered = [
        attraction_map[current]
    ]

    remaining.discard(current)

    if optimization_mode == "fastest":
        weight = "time"

    elif optimization_mode == "cheapest":
        weight = "cost"

    else:
        weight = "distance"

    while remaining:

        distances, _ = dijkstra(
            graph,
            current,
            weight=weight
        )

        reachable = [
            node
            for node in remaining
            if distances.get(
                node,
                float("inf")
            ) != float("inf")
        ]

        if not reachable:
            break

        if optimization_mode == "best experience":

            next_node = max(
                reachable,
                key=lambda node: (
                    attraction_map[node].get(
                        "score",
                        0
                    )
                    / (
                        1
                        + distances.get(
                            node,
                            0
                        )
                    )
                )
            )

        else:

            next_node = min(
                reachable,
                key=lambda node:
                    distances.get(
                        node,
                        float("inf")
                    )
            )

        ordered.append(
            attraction_map[next_node]
        )

        remaining.discard(
            next_node
        )

        current = next_node

    return ordered