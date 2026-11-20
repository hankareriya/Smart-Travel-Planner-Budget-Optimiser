def optimize_budget(
    attractions,
    activity_budget,
    travelers=1
):
    """
    0/1 Knapsack budget optimizer.

    Each attraction can be selected at most once.
    Attraction price is treated as per-person.
    """

    activity_budget = max(
        0,
        int(activity_budget)
    )

    travelers = max(
        1,
        int(travelers)
    )

    items = []

    for attraction in attractions:

        # Your database uses place_type for categories such as:
        # beach, food, adventure, nature, culture, history,
        # shopping, nightlife.
        #
        # Therefore we should NOT require:
        # place_type == "ATTRACTION"

        price = float(
            attraction.get("price", 0) or 0
        )

        total_price = int(
            round(price * travelers)
        )

        # Skip attractions that individually exceed
        # the available activity budget.
        if total_price > activity_budget:
            continue

        value = float(
            attraction.get(
                "value",
                attraction.get("score", 0)
            )
        )

        items.append(
            {
                "attraction": attraction,
                "cost": total_price,
                "value": value
            }
        )

    n = len(items)

    # If there are no usable attractions,
    # return an empty result safely.
    if n == 0:
        return {
            "selected": [],
            "total_cost": 0,
            "remaining_budget": activity_budget,
            "total_value": 0
        }

    # -----------------------------------------
    # 0/1 KNAPSACK
    # -----------------------------------------

    dp = [
        [0.0] * (activity_budget + 1)
        for _ in range(n + 1)
    ]

    selected = [
        [False] * (activity_budget + 1)
        for _ in range(n + 1)
    ]

    for i in range(1, n + 1):

        item = items[i - 1]

        cost = item["cost"]
        value = item["value"]

        for budget in range(
            activity_budget + 1
        ):

            # Do not select current attraction
            dp[i][budget] = dp[
                i - 1
            ][budget]

            # Select current attraction if affordable
            if cost <= budget:

                candidate = (
                    dp[i - 1][budget - cost]
                    + value
                )

                if candidate > dp[i][budget]:

                    dp[i][budget] = candidate

                    selected[i][budget] = True

    # -----------------------------------------
    # BACKTRACK
    # -----------------------------------------

    chosen = []

    current_budget = activity_budget

    for i in range(n, 0, -1):

        if selected[i][current_budget]:

            item = items[i - 1]

            chosen.append(
                item["attraction"]
            )

            current_budget -= item["cost"]

    chosen.reverse()

    # -----------------------------------------
    # FINAL COST
    # -----------------------------------------

    total_cost = sum(
        int(
            round(
                float(
                    item.get("price", 0) or 0
                ) * travelers
            )
        )
        for item in chosen
    )

    return {
        "selected": chosen,

        "total_cost":
            total_cost,

        "remaining_budget":
            max(
                0,
                activity_budget - total_cost
            ),

        "total_value":
            round(
                dp[n][activity_budget],
                2
            )
    }