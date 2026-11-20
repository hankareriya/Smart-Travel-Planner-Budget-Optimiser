from datetime import time

from sqlalchemy.orm import Session

from app.models.trips import Trip
from app.models.destinations import Destination
from app.models.attractions import Attraction
from app.models.itinerary_items import ItineraryItem

from app.algorithms.attraction_ranking import (
    rank_attractions
)

from app.algorithms.graph import (
    haversine_distance,
    get_transport_details
)

from app.algorithms.dijkstra import (
    dijkstra,
    get_path
)

from app.algorithms.budget_optimizer import (
    optimize_budget
)


# =========================================================
# DAY / TIME SETTINGS
# =========================================================

DAY_START = time(9, 0)
DAY_END = time(20, 0)

# 30 minutes are added directly to actual travel time.
# There is NO separate buffer item.
TRAVEL_MARGIN_MINUTES = 30

LUNCH_START = 13 * 60
LUNCH_END = 14 * 60

DINNER_START = 19 * 60
DINNER_END = 20 * 60

LUNCH_DURATION_MINUTES = 60
DINNER_DURATION_MINUTES = 60

MAX_ATTRACTIONS_PER_DAY = 3


# =========================================================
# TIME HELPERS
# =========================================================

def time_to_minutes(value):

    if value is None:
        return None

    return (
        value.hour * 60
        + value.minute
    )


def minutes_to_time(value):

    value = int(value)

    hours = value // 60
    minutes = value % 60

    # Keep time inside a 24-hour clock.
    hours = hours % 24

    return time(
        hours,
        minutes
    )


def attraction_duration_minutes(
    attraction
):

    duration = float(
        attraction.get(
            "duration",
            1
        )
        or 1
    )

    # Minimum visit duration = 30 minutes.
    return max(
        30,
        round(
            duration * 60
        )
    )


# =========================================================
# OPENING / CLOSING
# =========================================================

def is_open_for_visit(
    attraction,
    start_minute,
    duration_minutes
):

    opening = attraction.get(
        "opening_time"
    )

    closing = attraction.get(
        "closing_time"
    )

    # -----------------------------------------------------
    # Opening time
    # -----------------------------------------------------

    if opening is not None:

        opening_minute = (
            time_to_minutes(
                opening
            )
        )

        if start_minute < opening_minute:

            return False

    # -----------------------------------------------------
    # Closing time
    # -----------------------------------------------------

    if closing is not None:

        closing_minute = (
            time_to_minutes(
                closing
            )
        )

        # Handle attractions that close after midnight.
        if (
            opening is not None
            and closing_minute
            < time_to_minutes(
                opening
            )
        ):

            closing_minute += 1440

            check_start = (
                start_minute
            )

            if (
                check_start
                < time_to_minutes(
                    opening
                )
            ):

                check_start += 1440

            return (
                check_start
                + duration_minutes
                <= closing_minute
            )

        return (
            start_minute
            + duration_minutes
            <= closing_minute
        )

    return True


# =========================================================
# FIXED BUDGET
# =========================================================

def calculate_fixed_budget(
    trip,
    days
):

    food = (
        float(
            trip.food_budget_per_person
            or 0
        )
        * trip.travelers
        * days
    )

    accommodation = (
        float(
            trip.accommodation_per_night
            or 0
        )
        * max(
            0,
            days - 1
        )
    )

    intercity = float(
        trip.intercity_transportation_cost
        or 0
    )

    miscellaneous = float(
        trip.miscellaneous_budget
        or 0
    )

    return {

        "food":
            round(
                food,
                2
            ),

        "accommodation":
            round(
                accommodation,
                2
            ),

        "intercity_transportation":
            round(
                intercity,
                2
            ),

        "miscellaneous":
            round(
                miscellaneous,
                2
            )
    }


# =========================================================
# GRAPH
# =========================================================

def build_graph_for_attractions(
    attractions,
    transport_mode
):

    graph = {
        attraction["id"]: {}
        for attraction in attractions
    }

    for source in attractions:

        for destination in attractions:

            # NEVER create A -> A.
            if (
                source["id"]
                == destination["id"]
            ):

                continue

            source_lat = source.get(
                "latitude"
            )

            source_lon = source.get(
                "longitude"
            )

            destination_lat = (
                destination.get(
                    "latitude"
                )
            )

            destination_lon = (
                destination.get(
                    "longitude"
                )
            )

            # Skip attractions without coordinates.
            if (
                source_lat is None
                or source_lon is None
                or destination_lat is None
                or destination_lon is None
            ):

                continue

            distance = haversine_distance(
                source_lat,
                source_lon,
                destination_lat,
                destination_lon
            )

            travel = get_transport_details(
                distance,
                transport_mode
            )

            graph[
                source["id"]
            ][
                destination["id"]
            ] = {

                "distance":
                    round(
                        distance,
                        2
                    ),

                "time":
                    int(
                        travel["time"]
                    ),

                "cost":
                    round(
                        travel["cost"],
                        2
                    )
            }

    return graph


# =========================================================
# ROUTE
# =========================================================

def get_route_between(
    graph,
    source,
    destination,
    optimization_mode
):

    # NEVER route from an attraction to itself.
    if source == destination:

        return {
            "distance": 0,
            "time": 0,
            "cost": 0
        }

    # -----------------------------------------------------
    # Determine Dijkstra weight.
    # -----------------------------------------------------

    if optimization_mode == "fastest":

        weight = "time"

    elif optimization_mode == "cheapest":

        weight = "cost"

    else:

        # Best experience uses shortest distance
        # as the routing weight.
        weight = "distance"

    distances, previous = dijkstra(
        graph,
        source,
        weight=weight
    )

    path = get_path(
        previous,
        source,
        destination
    )

    # -----------------------------------------------------
    # If no Dijkstra path exists, use direct edge.
    # -----------------------------------------------------

    if not path:

        edge = graph.get(
            source,
            {}
        ).get(
            destination,
            {}
        )

        return {

            "distance":
                edge.get(
                    "distance",
                    0
                ),

            "time":
                edge.get(
                    "time",
                    0
                ),

            "cost":
                edge.get(
                    "cost",
                    0
                )
        }

    # -----------------------------------------------------
    # Calculate total path values.
    # -----------------------------------------------------

    total_distance = 0
    total_time = 0
    total_cost = 0

    for index in range(
        len(path) - 1
    ):

        edge = graph[
            path[index]
        ][
            path[index + 1]
        ]

        total_distance += (
            edge["distance"]
        )

        total_time += (
            edge["time"]
        )

        total_cost += (
            edge["cost"]
        )

    return {

        "distance":
            round(
                total_distance,
                2
            ),

        "time":
            int(
                total_time
            ),

        "cost":
            round(
                total_cost,
                2
            )
    }


# =========================================================
# CHOOSE NEXT ATTRACTION
# =========================================================

def choose_next_attraction(
    candidates,
    current_attraction,
    graph,
    optimization_mode,
    day_categories
):

    if not candidates:

        return None

    # -----------------------------------------------------
    # Prefer categories that have NOT already appeared
    # on the current day.
    # -----------------------------------------------------

    unused_category_candidates = [

        item

        for item in candidates

        if str(
            item.get(
                "category",
                ""
            )
        )
        .strip()
        .lower()
        not in day_categories

    ]

    if unused_category_candidates:

        candidates_to_use = (
            unused_category_candidates
        )

    else:

        candidates_to_use = candidates

    # -----------------------------------------------------
    # First attraction of the day.
    # -----------------------------------------------------

    if current_attraction is None:

        return max(
            candidates_to_use,
            key=lambda item:
                item.get(
                    "score",
                    0
                )
        )

    current_id = (
        current_attraction["id"]
    )

    best = None
    best_key = None

    # -----------------------------------------------------
    # Find best next attraction.
    # -----------------------------------------------------

    for candidate in candidates_to_use:

        # NEVER select the current attraction.
        if (
            candidate["id"]
            == current_id
        ):

            continue

        route = get_route_between(
            graph,
            current_id,
            candidate["id"],
            optimization_mode
        )

        # No route available.
        if (
            route["time"] <= 0
        ):

            continue

        # -------------------------------------------------
        # Optimization
        # -------------------------------------------------

        if optimization_mode == "fastest":

            key = (

                route["time"],

                -candidate.get(
                    "score",
                    0
                )

            )

        elif optimization_mode == "cheapest":

            key = (

                route["cost"],

                route["time"],

                -candidate.get(
                    "score",
                    0
                )

            )

        else:

            key = (

                route["time"],

                -candidate.get(
                    "score",
                    0
                )

            )

        if (
            best is None
            or key < best_key
        ):

            best = candidate
            best_key = key

    return best


# =========================================================
# MEAL ITEM
# =========================================================

def create_meal_item(
    trip_id,
    day,
    start_minute,
    duration,
    meal_type,
    order_number
):

    return {

        "item_type":
            "meal",

        "attraction_id":
            None,

        "from_attraction_id":
            None,

        "to_attraction_id":
            None,

        "start_time":
            minutes_to_time(
                start_minute
            ),

        "end_time":
            minutes_to_time(
                start_minute
                + duration
            ),

        "order_number":
            order_number,

        "distance_km":
            0,

        "travel_time_minutes":
            0,

        "travel_cost":
            0,

        "transport_mode":
            None,

        "meal_type":
            meal_type,

        "notes":
            f"{meal_type} break"
    }


# =========================================================
# TRAVEL ITEM
# =========================================================

def create_travel_item(
    trip,
    current_attraction,
    next_attraction,
    start_minute,
    route
):

    # NEVER create A -> A.
    if (
        current_attraction["id"]
        == next_attraction["id"]
    ):

        return None

    # -----------------------------------------------------
    # Actual travel time + 30-minute margin.
    # -----------------------------------------------------

    actual_travel_time = (
        int(
            route["time"]
        )
        + TRAVEL_MARGIN_MINUTES
    )

    # Never create zero-minute travel.
    if actual_travel_time <= 0:

        return None

    end_minute = (
        start_minute
        + actual_travel_time
    )

    return {

        "item_type":
            "travel",

        "attraction_id":
            None,

        "from_attraction_id":
            current_attraction["id"],

        "to_attraction_id":
            next_attraction["id"],

        "start_time":
            minutes_to_time(
                start_minute
            ),

        "end_time":
            minutes_to_time(
                end_minute
            ),

        "order_number":
            0,

        "distance_km":
            route["distance"],

        # Route time + 30 minutes.
        "travel_time_minutes":
            actual_travel_time,

        "travel_cost":
            route["cost"],

        "transport_mode":
            trip.transport_mode,

        "meal_type":
            None,

        "notes":
            f"Travel to "
            f"{next_attraction['name']}"
    }


# =========================================================
# GENERATE ONE DAY
# =========================================================

def generate_day(
    trip,
    day_number,
    candidates,
    graph,
    optimization_mode
):

    current_minute = (
        DAY_START.hour * 60
        + DAY_START.minute
    )

    items = []

    current_attraction = None

    attraction_count = 0

    day_categories = set()

    lunch_added = False

    dinner_added = False

    used_ids = set()

    # =====================================================
    # SELECT ATTRACTIONS
    # =====================================================

    while (
        candidates
        and attraction_count
        < MAX_ATTRACTIONS_PER_DAY
    ):

        candidate_pool = [

            attraction

            for attraction in candidates

            if (
                attraction["id"]
                not in used_ids
            )

        ]

        if not candidate_pool:

            break

        next_attraction = (
            choose_next_attraction(
                candidate_pool,
                current_attraction,
                graph,
                optimization_mode,
                day_categories
            )
        )

        if next_attraction is None:

            break

        # =================================================
        # ROUTE TO NEXT ATTRACTION
        # =================================================

        route = {
            "distance": 0,
            "time": 0,
            "cost": 0
        }

        travel_item = None

        if current_attraction is not None:

            # -------------------------------------------------
            # NEVER A -> A
            # -------------------------------------------------

            if (
                current_attraction["id"]
                == next_attraction["id"]
            ):

                candidates.remove(
                    next_attraction
                )

                continue

            route = get_route_between(
                graph,
                current_attraction["id"],
                next_attraction["id"],
                optimization_mode
            )

            actual_travel_time = (
                route["time"]
                + TRAVEL_MARGIN_MINUTES
            )

            # -------------------------------------------------
            # If route is unavailable, try another attraction.
            # -------------------------------------------------

            if actual_travel_time <= 0:

                candidates.remove(
                    next_attraction
                )

                continue

            arrival_minute = (
                current_minute
                + actual_travel_time
            )

            # -------------------------------------------------
            # Travel crossing lunch.
            #
            # Put lunch before travel.
            # -------------------------------------------------

            if (
                not lunch_added
                and current_minute < LUNCH_START
                and arrival_minute > LUNCH_START
            ):

                items.append(
                    create_meal_item(
                        trip.id,
                        day_number,
                        LUNCH_START,
                        LUNCH_DURATION_MINUTES,
                        "Lunch",
                        0
                    )
                )

                lunch_added = True

                current_minute = LUNCH_END

                arrival_minute = (
                    current_minute
                    + actual_travel_time
                )

            # -------------------------------------------------
            # Travel cannot cross dinner.
            # -------------------------------------------------

            if (
                current_minute < DINNER_START
                and arrival_minute > DINNER_START
            ):

                candidates.remove(
                    next_attraction
                )

                continue

            if (
                current_minute >= DINNER_START
            ):

                break

            travel_item = (
                create_travel_item(
                    trip,
                    current_attraction,
                    next_attraction,
                    current_minute,
                    route
                )
            )

            if travel_item is None:

                candidates.remove(
                    next_attraction
                )

                continue

            items.append(
                travel_item
            )

            current_minute = (
                arrival_minute
            )

        # =================================================
        # ATTRACTION DURATION
        # =================================================

        duration = (
            attraction_duration_minutes(
                next_attraction
            )
        )

        # =================================================
        # OPENING TIME
        # =================================================

        opening = (
            next_attraction.get(
                "opening_time"
            )
        )

        if opening is not None:

            opening_minute = (
                time_to_minutes(
                    opening
                )
            )

            if (
                current_minute
                < opening_minute
            ):

                current_minute = (
                    opening_minute
                )

        # =================================================
        # LUNCH
        # =================================================

        if not lunch_added:

            # Current time has reached lunch.
            if (
                current_minute
                >= LUNCH_START
            ):

                if (
                    current_minute
                    < LUNCH_END
                ):

                    items.append(
                        create_meal_item(
                            trip.id,
                            day_number,
                            current_minute,
                            LUNCH_END
                            - current_minute,
                            "Lunch",
                            0
                        )
                    )

                    lunch_added = True

                    current_minute = (
                        LUNCH_END
                    )

                elif (
                    current_minute
                    >= LUNCH_END
                ):

                    # Lunch window has passed.
                    # Add a late lunch if possible.
                    late_lunch_end = (
                        current_minute
                        + LUNCH_DURATION_MINUTES
                    )

                    if (
                        late_lunch_end
                        <= DINNER_START
                    ):

                        items.append(
                            create_meal_item(
                                trip.id,
                                day_number,
                                current_minute,
                                LUNCH_DURATION_MINUTES,
                                "Lunch",
                                0
                            )
                        )

                        lunch_added = True

                        current_minute = (
                            late_lunch_end
                        )

            # Attraction would cross lunch.
            elif (
                current_minute
                < LUNCH_START
                and (
                    current_minute
                    + duration
                    > LUNCH_START
                )
            ):

                items.append(
                    create_meal_item(
                        trip.id,
                        day_number,
                        LUNCH_START,
                        LUNCH_DURATION_MINUTES,
                        "Lunch",
                        0
                    )
                )

                lunch_added = True

                current_minute = LUNCH_END

        # =================================================
        # DINNER
        # =================================================

        if (
            current_minute
            >= DINNER_START
        ):

            break

        # Attraction must finish before dinner.
        if (
            current_minute
            < DINNER_START
            and (
                current_minute
                + duration
                > DINNER_START
            )
        ):

            break

        # =================================================
        # CLOSING TIME
        # =================================================

        if not is_open_for_visit(
            next_attraction,
            current_minute,
            duration
        ):

            closing = (
                next_attraction.get(
                    "closing_time"
                )
            )

            if closing is not None:

                closing_minute = (
                    time_to_minutes(
                        closing
                    )
                )

                if (
                    current_minute
                    + duration
                    > closing_minute
                ):

                    candidates.remove(
                        next_attraction
                    )

                    continue

        # =================================================
        # FINAL DAY-END CHECK
        # =================================================

        attraction_start = (
            current_minute
        )

        attraction_end = (
            attraction_start
            + duration
        )

        if (
            attraction_end
            > DINNER_START
        ):

            break

        # =================================================
        # ADD ATTRACTION
        # =================================================

        items.append(
            {

                "item_type":
                    "attraction",

                "attraction_id":
                    next_attraction["id"],

                "from_attraction_id":
                    None,

                "to_attraction_id":
                    None,

                "start_time":
                    minutes_to_time(
                        attraction_start
                    ),

                "end_time":
                    minutes_to_time(
                        attraction_end
                    ),

                "order_number":
                    0,

                "distance_km":
                    0,

                "travel_time_minutes":
                    0,

                "travel_cost":
                    0,

                "transport_mode":
                    None,

                "meal_type":
                    None,

                "notes":
                    None
            }
        )

        current_minute = (
            attraction_end
        )

        current_attraction = (
            next_attraction
        )

        used_ids.add(
            next_attraction["id"]
        )

        category = str(
            next_attraction.get(
                "category",
                ""
            )
        ).strip().lower()

        if category:

            day_categories.add(
                category
            )

        # Remove selected attraction from remaining pool.
        candidates.remove(
            next_attraction
        )

        attraction_count += 1

    # =====================================================
    # GUARANTEE LUNCH
    # =====================================================

    if not lunch_added:

        items.append(
            create_meal_item(
                trip.id,
                day_number,
                LUNCH_START,
                LUNCH_DURATION_MINUTES,
                "Lunch",
                0
            )
        )

        lunch_added = True

    # =====================================================
    # GUARANTEE DINNER
    # =====================================================

    if not dinner_added:

        items.append(
            create_meal_item(
                trip.id,
                day_number,
                DINNER_START,
                DINNER_DURATION_MINUTES,
                "Dinner",
                0
            )
        )

        dinner_added = True

    # =====================================================
    # SORT ITEMS BY TIME
    # =====================================================

    items.sort(
        key=lambda item:
            time_to_minutes(
                item["start_time"]
            )
    )

    # =====================================================
    # REASSIGN ORDER NUMBERS
    # =====================================================

    for index, item in enumerate(
        items,
        start=1
    ):

        item["order_number"] = index

    return items


# =========================================================
# COMPLETE ITINERARY
# =========================================================

def generate_trip_itinerary(
    db: Session,
    trip_id: int
):

    # =====================================================
    # TRIP
    # =====================================================

    trip = db.query(
        Trip
    ).filter(
        Trip.id == trip_id
    ).first()

    if not trip:

        raise ValueError(
            "Trip not found."
        )

    # =====================================================
    # DESTINATION
    # =====================================================

    destination = db.query(
        Destination
    ).filter(
        Destination.id
        == trip.destination_id
    ).first()

    if not destination:

        raise ValueError(
            "Destination not found."
        )

    # =====================================================
    # ATTRACTIONS
    # =====================================================

    attractions_db = db.query(
        Attraction
    ).filter(
        Attraction.destination_id
        == trip.destination_id
    ).all()

    attractions = []

    for attraction in attractions_db:

        attractions.append(
            {

                "id":
                    attraction.id,

                "name":
                    attraction.name,

                "category":
                    attraction.category,

                "place_type":
                    attraction.place_type,

                "rating":
                    attraction.rating or 0,

                "price":
                    attraction.price or 0,

                "duration":
                    attraction.duration or 1,

                "popularity":
                    attraction.popularity or 0,

                "latitude":
                    float(
                        attraction.latitude
                    )
                    if attraction.latitude
                    is not None
                    else None,

                "longitude":
                    float(
                        attraction.longitude
                    )
                    if attraction.longitude
                    is not None
                    else None,

                "opening_time":
                    attraction.opening_time,

                "closing_time":
                    attraction.closing_time
            }
        )

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    unique_attractions = []

    seen_names = set()

    for attraction in attractions:

        normalized_name = (
            str(
                attraction["name"]
            )
            .strip()
            .lower()
        )

        if normalized_name in seen_names:

            continue

        seen_names.add(
            normalized_name
        )

        unique_attractions.append(
            attraction
        )

    attractions = (
        unique_attractions
    )

    # =====================================================
    # NUMBER OF DAYS
    # =====================================================

    days = (
        trip.end_date
        - trip.start_date
    ).days + 1

    days = max(
        1,
        days
    )

    # =====================================================
    # FIXED BUDGET
    # =====================================================

    fixed_budget = (
        calculate_fixed_budget(
            trip,
            days
        )
    )

    fixed_total = sum(
        fixed_budget.values()
    )

    # =====================================================
    # RANK ATTRACTIONS
    # =====================================================

    ranked = rank_attractions(
        attractions,
        trip.interests or []
    )

    # =====================================================
    # ACTIVITY BUDGET
    # =====================================================

    activity_budget = max(
        0,
        float(
            trip.budget or 0
        )
        - fixed_total
    )

    # =====================================================
    # BUDGET OPTIMIZER
    # =====================================================

    budget_result = (
        optimize_budget(
            ranked,
            activity_budget,
            trip.travelers
        )
    )

    # =====================================================
    # SELECTED ATTRACTIONS
    # =====================================================

    selected_ids = {

        item["id"]

        for item in budget_result.get(
            "selected",
            []
        )

    }

    selected = [

        item

        for item in ranked

        if item["id"]
        in selected_ids

    ]

    # =====================================================
    # FALLBACK
    # =====================================================

    # If the optimizer cannot select anything,
    # choose affordable highly-ranked attractions.

    if not selected:

        affordable = [

            item

            for item in ranked

            if (
                float(
                    item.get(
                        "price",
                        0
                    )
                    or 0
                )
                * trip.travelers
                <= activity_budget
            )

        ]

        selected = affordable[
            :max(
                1,
                min(
                    3,
                    len(affordable)
                )
            )
        ]

    # =====================================================
    # GRAPH
    # =====================================================

    graph = (
        build_graph_for_attractions(
            attractions,
            trip.transport_mode
        )
    )

    # =====================================================
    # GENERATE DAYS
    # =====================================================

    remaining = selected.copy()

    all_items = []

    for day_number in range(
        1,
        days + 1
    ):

        # -------------------------------------------------
        # If attractions have finished, still add lunch
        # and dinner for the remaining days.
        # -------------------------------------------------

        if not remaining:

            meal_items = [

                create_meal_item(
                    trip.id,
                    day_number,
                    LUNCH_START,
                    LUNCH_DURATION_MINUTES,
                    "Lunch",
                    1
                ),

                create_meal_item(
                    trip.id,
                    day_number,
                    DINNER_START,
                    DINNER_DURATION_MINUTES,
                    "Dinner",
                    2
                )

            ]

            all_items.extend(
                [
                    (
                        day_number,
                        item
                    )

                    for item in meal_items
                ]
            )

            continue

        day_items = generate_day(
            trip,
            day_number,
            remaining,
            graph,
            trip.optimization_mode
            or "best experience"
        )

        all_items.extend(
            [
                (
                    day_number,
                    item
                )

                for item in day_items
            ]
        )

    # =====================================================
    # DELETE OLD ITINERARY
    # =====================================================

    db.query(
        ItineraryItem
    ).filter(
        ItineraryItem.trip_id
        == trip.id
    ).delete(
        synchronize_session=False
    )

    db.commit()

    # =====================================================
    # INSERT NEW ITINERARY ITEMS
    # =====================================================

    for day_number, item in all_items:

        db_item = ItineraryItem(
            trip_id=trip.id,
            day=day_number,
            item_type=item["item_type"],
            attraction_id=item["attraction_id"],
            from_attraction_id=item["from_attraction_id"],
            to_attraction_id=item["to_attraction_id"],
            start_time=item["start_time"],
            end_time=item["end_time"],
            order_number=item["order_number"],
            distance_km=item["distance_km"],
            travel_time_minutes=item["travel_time_minutes"],
            travel_cost=item["travel_cost"],
            transport_mode=item["transport_mode"],
            meal_type=item["meal_type"],
            notes=item["notes"]
        )

        db.add(
            db_item
        )

    db.commit()

    # =====================================================
    # LOCAL TRANSPORTATION COST
    # =====================================================

    saved_items = (
        db.query(
            ItineraryItem
        ).filter(
            ItineraryItem.trip_id
            == trip.id
        ).all()
    )

    local_transportation = round(
        sum(
            float(
                item.travel_cost
                or 0
            )

            for item in saved_items

            if item.item_type
            == "travel"

        ),
        2
    )

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "message":
            "Itinerary generated successfully.",

        "trip_id":
            trip.id,

        "destination":
            destination.name,

        "days":
            days,

        "budget":
            {

                "total_budget":
                    float(
                        trip.budget
                        or 0
                    ),

                "accommodation":
                    fixed_budget[
                        "accommodation"
                    ],

                "intercity_transportation":
                    fixed_budget[
                        "intercity_transportation"
                    ],

                "food":
                    fixed_budget[
                        "food"
                    ],

                "activities":
                    budget_result.get(
                        "total_cost",
                        0
                    ),

                "local_transportation":
                    local_transportation,

                "miscellaneous":
                    fixed_budget[
                        "miscellaneous"
                    ]
            }
    }