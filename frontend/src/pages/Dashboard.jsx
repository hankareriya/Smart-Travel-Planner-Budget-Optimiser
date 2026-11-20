import {
  Link,
  useNavigate
} from "react-router-dom";

import {
  useEffect,
  useState
} from "react";

import "./Dashboard.css";


// =========================================================
// CITY IMAGES
// =========================================================

import goaImage from "../assets/goa.png";
import mumbaiImage from "../assets/mumbai.png";
import jaipurImage from "../assets/jaipur.png";


// =========================================================
// API
// =========================================================

const API_URL =
  "http://127.0.0.1:8000";


// =========================================================
// CITY IMAGES
// =========================================================

const CITY_IMAGES = {

  goa: goaImage,

  mumbai: mumbaiImage,

  jaipur: jaipurImage

};


// =========================================================
// INTEREST DISPLAY
// =========================================================

const INTEREST_INFO = {

  beach: {
    icon: "🏖️",
    label: "Beach"
  },

  food: {
    icon: "🍴",
    label: "Food"
  },

  adventure: {
    icon: "🧗",
    label: "Adventure"
  },

  nature: {
    icon: "🌿",
    label: "Nature"
  },

  culture: {
    icon: "🏛️",
    label: "Culture"
  },

  history: {
    icon: "🏰",
    label: "History"
  },

  shopping: {
    icon: "🛍️",
    label: "Shopping"
  },

  nightlife: {
    icon: "🌙",
    label: "Nightlife"
  }

};


// =========================================================
// GET CITY IMAGE
// =========================================================

function getCityImage(
  destination
) {

  const city =
    String(
      destination || ""
    )
      .trim()
      .toLowerCase();


  if (
    city.includes("goa")
  ) {

    return CITY_IMAGES.goa;

  }


  if (
    city.includes("mumbai") ||
    city.includes("bombay")
  ) {

    return CITY_IMAGES.mumbai;

  }


  if (
    city.includes("jaipur")
  ) {

    return CITY_IMAGES.jaipur;

  }


  return null;

}


// =========================================================
// GET INTEREST INFORMATION
// =========================================================

function getInterestInfo(
  interest
) {

  const key =
    String(
      interest || ""
    )
      .trim()
      .toLowerCase();


  return (
    INTEREST_INFO[key] || {

      icon: "✨",

      label:
        String(
          interest
        )
          .charAt(0)
          .toUpperCase()
        +
        String(
          interest
        )
          .slice(1)

    }
  );

}


// =========================================================
// DASHBOARD
// =========================================================

function Dashboard() {

  const navigate =
    useNavigate();


  const [
    trips,
    setTrips
  ] = useState([]);


  const [
    loading,
    setLoading
  ] = useState(true);


  const [
    error,
    setError
  ] = useState("");


  const [
    generatingTripId,
    setGeneratingTripId
  ] = useState(null);


  // =======================================================
  // FETCH TRIPS
  // =======================================================

  useEffect(() => {

    fetchTrips();


    const handleTripChange =
      () => {

        fetchTrips();

      };


    window.addEventListener(
      "tripSaved",
      handleTripChange
    );


    window.addEventListener(
      "tripGenerated",
      handleTripChange
    );


    return () => {

      window.removeEventListener(
        "tripSaved",
        handleTripChange
      );


      window.removeEventListener(
        "tripGenerated",
        handleTripChange
      );

    };

  }, []);


  // =======================================================
  // FETCH TRIPS
  // =======================================================

  const fetchTrips =
    async () => {

      try {

        setLoading(true);

        setError("");


        const token =
          localStorage.getItem(
            "access_token"
          );


        if (!token) {

          navigate("/login");

          return;

        }


        const response =
          await fetch(
            `${API_URL}/trips`,
            {

              headers: {

                Authorization:
                  `Bearer ${token}`

              }

            }
          );


        const data =
          await response.json();


        if (!response.ok) {

          throw new Error(
            data.detail ||
            "Failed to load trips."
          );

        }


        setTrips(
          Array.isArray(data)
            ? data
            : []
        );


      } catch (error) {

        console.error(error);


        setError(
          error.message ||
          "Unable to load trips."
        );


      } finally {

        setLoading(false);

      }

    };


  // =======================================================
  // GENERATE ITINERARY
  // =======================================================

  const handleGenerate =
    async tripId => {

      try {

        setGeneratingTripId(
          tripId
        );

        setError("");


        const token =
          localStorage.getItem(
            "access_token"
          );


        if (!token) {

          navigate("/login");

          return;

        }


        const response =
          await fetch(
            `${API_URL}/trips/${tripId}/generate`,
            {

              method: "POST",

              headers: {

                Authorization:
                  `Bearer ${token}`,

                "Content-Type":
                  "application/json"

              }

            }
          );


        const data =
          await response.json();


        if (!response.ok) {

          throw new Error(
            data.detail ||
            "Failed to generate itinerary."
          );

        }


        // Tell Dashboard that
        // itinerary generation succeeded.

        window.dispatchEvent(
          new Event(
            "tripGenerated"
          )
        );


        // Open generated itinerary.

        navigate(
          `/itinerary/${tripId}`,
          {

            state: {

              newlyGenerated:
                true

            }

          }
        );


      } catch (error) {

        console.error(error);


        setError(
          error.message ||
          "Unable to generate itinerary."
        );


      } finally {

        setGeneratingTripId(
          null
        );

      }

    };


  // =======================================================
  // VIEW ITINERARY
  // =======================================================

  const handleViewTrip =
    tripId => {

      navigate(
        `/itinerary/${tripId}`,
        {

          state: {

            newlyGenerated:
              false

          }

        }
      );

    };


  // =======================================================
  // LOADING
  // =======================================================

  if (loading) {

    return (

      <div
        className="dashboard-page"
      >

        <div
          className="dashboard-container"
        >

          <h1>
            Dashboard
          </h1>


          <p>
            Loading your trips...
          </p>

        </div>

      </div>

    );

  }


  // =======================================================
  // TODAY
  // =======================================================

  const today =
    new Date();


  today.setHours(
    0,
    0,
    0,
    0
  );


  // =======================================================
  // UPCOMING TRIPS
  // =======================================================

  const upcomingTrips =
    trips.filter(
      trip => {

        const tripDate =
          new Date(
            trip.start_date
          );


        return (
          tripDate >= today
        );

      }
    );


  // =======================================================
  // PREVIOUS TRIPS
  // =======================================================

  const previousTrips =
    trips.filter(
      trip => {

        const tripDate =
          new Date(
            trip.start_date
          );


        return (
          tripDate < today
        );

      }
    );


  // =======================================================
  // TRIP CARD
  // =======================================================

  const TripCard =
    ({ trip }) => {


      // ---------------------------------------------------
      // DOES ITINERARY EXIST?
      // ---------------------------------------------------

      const hasItinerary =
        Boolean(
          trip.has_itinerary ||
          trip.itinerary_generated
        );


      // ---------------------------------------------------
      // IS THIS AN UPCOMING TRIP?
      // ---------------------------------------------------

      const isUpcoming =
        upcomingTrips.some(
          upcomingTrip =>
            upcomingTrip.id ===
            trip.id
        );


      // ---------------------------------------------------
      // CITY IMAGE
      // ---------------------------------------------------

      const cityImage =
        getCityImage(
          trip.destination_name
        );


      return (

        <article
          className="trip-card"
        >

          {/* =================================================
              CITY IMAGE
          ================================================= */}

          <div
            className="trip-image-wrapper"
          >

            {cityImage ? (

              <img
                src={cityImage}

                alt={
                  trip.destination_name ||
                  "Travel destination"
                }

                className="trip-city-image"

                onError={
                  event => {

                    event.currentTarget.style.display =
                      "none";


                    const fallback =
                      event.currentTarget
                        .parentElement
                        .querySelector(
                          ".trip-image-fallback"
                        );


                    if (fallback) {

                      fallback.style.display =
                        "flex";

                    }

                  }
                }
              />

            ) : null}


            {/* =================================================
                IMAGE FALLBACK
            ================================================= */}

            <div
              className="trip-image-fallback"

              style={{
                display:
                  cityImage
                    ? "none"
                    : "flex"
              }}
            >

              <span>
                ✈️
              </span>


              <strong>
                {
                  trip.destination_name ||
                  "Unknown Destination"
                }
              </strong>

            </div>


            {/* =================================================
                IMAGE OVERLAY
            ================================================= */}

            <div
              className="trip-image-overlay"
            >

              <h3>
                {
                  trip.destination_name ||
                  "Unknown Destination"
                }
              </h3>

            </div>

          </div>


          {/* =================================================
              CARD CONTENT
          ================================================= */}

          <div
            className="trip-card-content"
          >

            {/* =================================================
                DATE
            ================================================= */}

            <div
              className="trip-date"
            >

              📅{" "}

              {trip.start_date}

              {" → "}

              {trip.end_date}

            </div>


            {/* =================================================
                BASIC INFORMATION
            ================================================= */}

            <div
              className="trip-basic-info"
            >

              <span>

                👥{" "}

                {trip.travelers}

                {" "}

                {
                  trip.travelers === 1
                    ? "traveler"
                    : "travelers"
                }

              </span>


              <span>

                💰 ₹

                {Number(
                  trip.budget || 0
                ).toLocaleString()}

              </span>

            </div>


            {/* =================================================
                INTERESTS
            ================================================= */}

            {
              trip.interests?.length > 0 &&
              (

                <div
                  className="trip-interests"
                >

                  {
                    trip.interests.map(
                      (
                        interest,
                        index
                      ) => {

                        const info =
                          getInterestInfo(
                            interest
                          );


                        return (

                          <span
                            key={
                              `${interest}-${index}`
                            }

                            className="interest-badge"
                          >

                            <span>
                              {info.icon}
                            </span>


                            <span>
                              {info.label}
                            </span>

                          </span>

                        );

                      }
                    )
                  }

                </div>

              )
            }


            {/* =================================================
                ACTION BUTTON
            ================================================= */}

            <div
              className="trip-actions"
            >

              {/* =================================================
                  PREVIOUS TRIP
                  
                  ALWAYS SHOW VIEW ITINERARY.
                  
                  We do NOT show Generate Itinerary here.
                  
                  routes/trips.py automatically makes sure that
                  previous trips get an itinerary.
              ================================================= */}

              {!isUpcoming ? (

                <button
                  type="button"

                  className="primary-button"

                  onClick={() =>
                    handleViewTrip(
                      trip.id
                    )
                  }
                >

                  View Itinerary

                </button>

              ) : hasItinerary ? (

                /* =================================================
                   UPCOMING + ITINERARY EXISTS
                ================================================= */

                <button
                  type="button"

                  className="primary-button"

                  onClick={() =>
                    handleViewTrip(
                      trip.id
                    )
                  }
                >

                  View Itinerary

                </button>

              ) : (

                /* =================================================
                   UPCOMING + NO ITINERARY
                ================================================= */

                <button
                  type="button"

                  className="primary-button"

                  disabled={
                    generatingTripId ===
                    trip.id
                  }

                  onClick={() =>
                    handleGenerate(
                      trip.id
                    )
                  }
                >

                  {
                    generatingTripId ===
                    trip.id

                      ? "Generating..."

                      : "Generate Itinerary"
                  }

                </button>

              )}

            </div>

          </div>

        </article>

      );

    };


  // =======================================================
  // PAGE
  // =======================================================

  return (

    <div
      className="dashboard-page"
    >

      <div
        className="dashboard-container"
      >

        {/* =================================================
            HEADER
        ================================================= */}

        <div
          className="dashboard-header"
        >

          <div>

            <p
              className="dashboard-eyebrow"
            >

              SMART TRAVEL PLANNER

            </p>


            <h1>
              My Trips
            </h1>


            <p>
              Plan, optimize and manage
              your journeys.
            </p>

          </div>


          <Link
            to="/create-trip"

            className=
              "primary-button create-trip-button"
          >

            + Create New Trip

          </Link>

        </div>


        {/* =================================================
            ERROR
        ================================================= */}

        {error && (

          <div
            className="error-message"
          >

            {error}

          </div>

        )}


        {/* =================================================
            UPCOMING TRIPS
        ================================================= */}

        <section
          className="trip-section"
        >

          <div
            className="section-title-row"
          >

            <div>

              <h2>
                Upcoming Trips
              </h2>


              <p>
                Your upcoming adventures
              </p>

            </div>

          </div>


          {upcomingTrips.length === 0 ? (

            <div
              className="empty-trips"
            >

              <span>
                ✈️
              </span>


              <h3>
                No upcoming trips
              </h3>


              <p>
                Create a trip and start
                planning your next adventure.
              </p>

            </div>

          ) : (

            <div
              className="trip-grid"
            >

              {
                upcomingTrips.map(
                  trip => (

                    <TripCard
                      key={trip.id}
                      trip={trip}
                    />

                  )
                )
              }

            </div>

          )}

        </section>


        {/* =================================================
            PREVIOUS TRIPS
        ================================================= */}

        <section
          className="trip-section"
        >

          <div
            className="section-title-row"
          >

            <div>

              <h2>
                Previous Trips
              </h2>


              <p>
                Your completed journeys
              </p>

            </div>

          </div>


          {previousTrips.length === 0 ? (

            <div
              className="empty-trips"
            >

              <span>
                🗺️
              </span>


              <h3>
                No previous trips
              </h3>


              <p>
                Your completed trips will
                appear here.
              </p>

            </div>

          ) : (

            <div
              className="trip-grid"
            >

              {
                previousTrips.map(
                  trip => (

                    <TripCard
                      key={trip.id}
                      trip={trip}
                    />

                  )
                )
              }

            </div>

          )}

        </section>

      </div>

    </div>

  );

}


export default Dashboard;