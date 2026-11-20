from app.algorithms.attraction_ranking import (
    rank_attractions
)

from app.algorithms.budget_optimizer import (
    optimize_budget
)

from app.algorithms.graph import (
    build_graph
)

from app.algorithms.route_optimizer import (
    optimize_route
)


def generate_itinerary(
    attractions,
    days,
    travelers,
    total_budget,
    interests,
    optimization_mode,
    fixed_budget=0
):
    days = max(
        1,
        int(days)
    )

    travelers = max(
        1,
        int(travelers)
    )

    ranked = rank_attractions(
        attractions,
        interests
    )

    activity_budget = max(
        0,
        float(total_budget or 0)
        - float(fixed_budget or 0)
    )

    budget_result = optimize_budget(
        ranked,
        activity_budget,
        travelers
    )

    selected = budget_result[
        "selected"
    ]

    selected_ids = {
        item["id"]
        for item in selected
    }

    selected = [
        item
        for item in ranked
        if item["id"] in selected_ids
    ]

    graph = build_graph(
        selected,
        transport_mode="car"
    )

    routed = optimize_route(
        selected,
        graph,
        optimization_mode
    )

    day_buckets = [
        []
        for _ in range(days)
    ]

    for index, attraction in enumerate(
        routed
    ):
        day_buckets[
            index % days
        ].append(
            attraction
        )

    return {
        "days": day_buckets,
        "total_cost": budget_result[
            "total_cost"
        ],
        "remaining_budget": max(
            0,
            float(total_budget or 0)
            - float(fixed_budget or 0)
            - budget_result["total_cost"]
        ),
        "total_experience_value":
            budget_result["total_value"],
        "ranked_attractions": ranked
    }