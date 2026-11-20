def calculate_interest_score(attraction, user_interests):
    category = str(
        attraction.get("category", "")
    ).strip().lower()

    interests = [
        str(item).strip().lower()
        for item in (user_interests or [])
    ]

    if category in interests:
        return 10

    return 0


def calculate_rating_score(rating):
    rating = float(rating or 0)

    return max(
        0,
        min(10, (rating / 5) * 10)
    )


def calculate_price_score(price):
    price = float(price or 0)

    score = 10 - (price / 100)

    return max(
        0,
        min(10, score)
    )


def calculate_distance_score(distance):
    distance = float(distance or 0)

    return max(
        0,
        10 - distance
    )


def calculate_popularity_score(popularity):
    popularity = float(popularity or 0)

    return max(
        0,
        min(10, popularity / 10)
    )


def calculate_score(
    attraction,
    user_interests
):
    rating_score = calculate_rating_score(
        attraction.get("rating", 0)
    )

    interest_score = calculate_interest_score(
        attraction,
        user_interests
    )

    price_score = calculate_price_score(
        attraction.get("price", 0)
    )

    distance_score = calculate_distance_score(
        attraction.get("distance", 5)
    )

    popularity_score = calculate_popularity_score(
        attraction.get("popularity", 0)
    )

    final_score = (
        0.30 * rating_score
        + 0.30 * interest_score
        + 0.15 * price_score
        + 0.15 * distance_score
        + 0.10 * popularity_score
    )

    return round(
        final_score,
        2
    )


def rank_attractions(
    attractions,
    user_interests
):
    ranked = []

    for attraction in attractions:
        attraction_copy = attraction.copy()

        attraction_copy["score"] = calculate_score(
            attraction_copy,
            user_interests
        )

        ranked.append(
            attraction_copy
        )

    ranked.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return ranked