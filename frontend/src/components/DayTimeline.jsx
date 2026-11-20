import AttractionCard from "./AttractionCard";


function formatMinutes(minutes) {
  if (!minutes) {
    return "";
  }

  const hours =
    Math.floor(minutes / 60);

  const mins =
    minutes % 60;

  if (hours === 0) {
    return `${mins} min`;
  }

  if (mins === 0) {
    return `${hours} hr`;
  }

  return `${hours} hr ${mins} min`;
}


function DayTimeline({
  activities
}) {

  if (
    !activities ||
    activities.length === 0
  ) {
    return (
      <div className="day-timeline">
        <p>
          No activities planned for this day.
        </p>
      </div>
    );
  }


  return (
    <div className="day-timeline">

      {activities.map(
        (activity, index) => {

          const type =
            activity.item_type;


          if (type === "travel") {

            return (
              <div
                key={
                  activity.id ||
                  `travel-${index}`
                }
                className="timeline-item"
              >

                <div className="travel-card">

                  <div className="travel-time">
                    {activity.time}
                  </div>

                  <h4>
                    🚗 Travel
                  </h4>

                  <p>
                    {activity.from_name
                      ? `${activity.from_name} → ${activity.to_name}`
                      : "Travel to next location"}
                  </p>

                  <div className="travel-details">

                    <span>
                      📍 {activity.distance_km} km
                    </span>

                    <span>
                      ⏱️ {formatMinutes(
                        activity.travel_time_minutes
                      )}
                    </span>

                    <span>
                      ₹{Number(
                        activity.travel_cost || 0
                      ).toLocaleString()}
                    </span>

                  </div>

                </div>

                {index !== activities.length - 1 && (
                  <div className="timeline-line">
                    ↓
                  </div>
                )}

              </div>
            );
          }


          if (type === "buffer") {

            return (
              <div
                key={
                  activity.id ||
                  `buffer-${index}`
                }
                className="timeline-item"
              >

                <div className="buffer-card">

                  <div className="buffer-time">
                    {activity.time}
                  </div>

                  <h4>
                    ⏳ Travel Buffer
                  </h4>

                  <p>
                    {activity.notes ||
                      "Transition / settling time"}
                  </p>

                </div>

                {index !== activities.length - 1 && (
                  <div className="timeline-line">
                    ↓
                  </div>
                )}

              </div>
            );
          }


          if (type === "meal") {

            return (
              <div
                key={
                  activity.id ||
                  `meal-${index}`
                }
                className="timeline-item"
              >

                <div className="meal-card">

                  <div className="meal-time">
                    {activity.time}
                  </div>

                  <h4>
                    🍽️ {activity.meal_type || "Meal"}
                  </h4>

                  <p>
                    Food budget included in daily food allocation.
                  </p>

                </div>

                {index !== activities.length - 1 && (
                  <div className="timeline-line">
                    ↓
                  </div>
                )}

              </div>
            );
          }


          if (type === "shopping") {

            return (
              <div
                key={
                  activity.id ||
                  `shopping-${index}`
                }
                className="timeline-item"
              >

                <div className="shopping-card">

                  <div className="shopping-time">
                    {activity.time}
                  </div>

                  <h4>
                    🛍️ {activity.name}
                  </h4>

                  <p>
                    Shopping activity
                  </p>

                  <small>
                    Shopping cost is not included in trip budget.
                  </small>

                </div>

                {index !== activities.length - 1 && (
                  <div className="timeline-line">
                    ↓
                  </div>
                )}

              </div>
            );
          }


          return (
            <div
              key={
                activity.id ||
                activity.attraction_id ||
                `attraction-${index}`
              }
              className="timeline-item"
            >

              <AttractionCard

                time={
                  activity.time || ""
                }

                name={
                  activity.name ||
                  "Unknown attraction"
                }

                rating={
                  activity.rating || ""
                }

                category={
                  activity.category || ""
                }

                price={
                  Number(activity.price || 0) === 0
                    ? "FREE"
                    : `₹${Number(
                        activity.price
                      ).toLocaleString()} / person`
                }

                duration={
                  activity.duration
                    ? `${activity.duration} hours`
                    : ""
                }

              />

              {index !== activities.length - 1 && (
                <div className="timeline-line">
                  ↓
                </div>
              )}

            </div>
          );
        }
      )}

    </div>
  );
}


export default DayTimeline;