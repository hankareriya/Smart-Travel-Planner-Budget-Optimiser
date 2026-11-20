import { Link } from "react-router-dom";


function TripCard({
  image,
  name,
  description,
  showButton = false,
  tripId,
  onViewTrip,
}) {

  return (

    <div className="trip-card">

      {/* IMAGE */}

      {image && (

        <img
          src={image}
          alt={name}
          className="trip-card-image"
        />

      )}


      {/* CONTENT */}

      <div className="trip-card-content">

        <h3>
          {name}
        </h3>


        <p>
          {description}
        </p>


        {/* VIEW TRIP */}

        {showButton && (

          <Link
            to={`/itinerary/${tripId}`}
            className="view-trip-btn"
            onClick={(event) => {

              if (onViewTrip) {

                event.preventDefault();

                onViewTrip();

              }

            }}
          >
            View Trip
          </Link>

        )}

      </div>

    </div>

  );

}


export default TripCard;