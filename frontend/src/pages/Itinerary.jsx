import {
  useEffect,
  useState
} from "react";

import {
  useNavigate,
  useParams,
  useLocation
} from "react-router-dom";

import DayTimeline from "../components/DayTimeline";
import BudgetCard from "../components/BudgetCard";

import "./Itinerary.css";


const API_URL =
  "http://127.0.0.1:8000";


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
        String(interest)
          .charAt(0)
          .toUpperCase()
        +
        String(interest)
          .slice(1)
    }
  );
}


function Itinerary() {

  const {
    tripId
  } = useParams();


  const navigate =
    useNavigate();


  const location =
    useLocation();


  const [
    itinerary,
    setItinerary
  ] = useState(null);


  const [
    loading,
    setLoading
  ] = useState(true);


  const [
    error,
    setError
  ] = useState("");


  const newlyGenerated =
    location.state?.newlyGenerated
    === true;


  useEffect(() => {

    fetchItinerary();

  }, [tripId]);


  const fetchItinerary =
    async () => {

      try {

        setLoading(true);
        setError("");

        const token =
          localStorage.getItem(
            "access_token"
          );

        if (!token) {

          throw new Error(
            "You are not logged in."
          );
        }


        const response =
          await fetch(
            `${API_URL}/trips/${tripId}/itinerary`,
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
            "Failed to load itinerary."
          );
        }


        setItinerary(data);

      } catch (error) {

        console.error(error);

        setError(
          error.message ||
          "Unable to load itinerary."
        );

      } finally {

        setLoading(false);
      }
    };


  const handleSaveTrip =
    () => {

      localStorage.setItem(
        "hasTrips",
        "true"
      );


      window.dispatchEvent(
        new Event("tripSaved")
      );


      navigate(
        "/dashboard",
        {
          replace: true
        }
      );
    };


  const handleEditTrip =
    () => {

      navigate(
        `/create-trip?edit=${tripId}`
      );
    };


  if (loading) {

    return (
      <div className="itinerary-page">

        <div className="itinerary-container">

          <h1>
            Building Your Itinerary...
          </h1>

          <p>
            Finding attractions,
            routes, meals and
            travel timings.
          </p>

        </div>

      </div>
    );
  }


  if (error) {

    return (
      <div className="itinerary-page">

        <div className="itinerary-container">

          <h1>
            Unable to Load Itinerary
          </h1>

          <p>
            {error}
          </p>

          <button
            className="primary-button"
            onClick={() =>
              navigate(
                "/dashboard"
              )
            }
          >
            Back to Dashboard
          </button>

        </div>

      </div>
    );
  }


  if (!itinerary) {
    return null;
  }


  const budget =
    itinerary.budget || {};


  return (
    <div className="itinerary-page">

      <div
        className="itinerary-container"
      >

        {/* =========================================
            HEADER
        ========================================= */}

        <div
          className="itinerary-header"
        >

          <p
            className="itinerary-eyebrow"
          >
            YOUR TRAVEL PLAN
          </p>

          <h1>
            {itinerary.destination}
          </h1>

          <p>
            📅{" "}
            {itinerary.start_date}
            {" → "}
            {itinerary.end_date}
          </p>

          <p>
            👥 {itinerary.travelers}
            {" "}
            {itinerary.travelers === 1
              ? "traveler"
              : "travelers"}
          </p>

          <p>
            ⚡{" "}
            {itinerary.optimization}
          </p>

        </div>


        {/* =========================================
            INTERESTS
        ========================================= */}

        {itinerary.interests?.length > 0 && (

          <div
            className="itinerary-interests"
          >

            <strong>
              Your interests
            </strong>

            <div
              className="interest-badges"
            >

              {itinerary.interests.map(
                interest => {

                  const info =
                    getInterestInfo(
                      interest
                    );

                  return (
                    <span
                      key={interest}
                      className="interest-badge"
                    >

                      {info.icon}

                      {info.label}

                    </span>
                  );
                }
              )}

            </div>

          </div>

        )}


        {/* =========================================
            BUDGET
        ========================================= */}

        <BudgetCard

          totalBudget={
            budget.total_budget
          }

          planned={
            budget.planned
          }

          remaining={
            budget.remaining
          }

          percentage={
            budget.percentage
          }

          overBudget={
            budget.over_budget
          }

          breakdown={
            budget
          }

        />


        {/* =========================================
            DAYS
        ========================================= */}

        <div
          className="itinerary-days"
        >

          {itinerary.days.map(
            day => {

              /*
              -----------------------------------------
              PROTECT AGAINST OLD BUFFER RECORDS
              -----------------------------------------
              */

              const activities =
                (
                  day.activities || []
                ).filter(
                  activity =>
                    activity.item_type
                    !== "buffer"
                );


              return (
                <section
                  key={day.day}
                  className="itinerary-day"
                >

                  <div
                    className="day-header"
                  >

                    <div>

                      <p
                        className="day-label"
                      >
                        DAY
                        {" "}
                        {day.day}
                      </p>

                      <h2>
                        Day {day.day}
                      </h2>

                    </div>


                    <div
                      className="day-costs"
                    >

                      <span>
                        Activities: ₹
                        {Number(
                          day.activities_cost
                          || 0
                        ).toLocaleString()}
                      </span>

                      <span>
                        Local Travel: ₹
                        {Number(
                          day.local_transportation
                          || 0
                        ).toLocaleString()}
                      </span>

                    </div>

                  </div>


                  <DayTimeline
                    activities={
                      activities
                    }
                  />

                </section>
              );

            }
          )}

        </div>


        {/* =========================================
            ACTIONS
        ========================================= */}

        <div
          className="itinerary-actions"
        >

          <button
            className="secondary-button"
            onClick={() =>
              navigate(
                "/dashboard"
              )
            }
          >
            Back to Dashboard
          </button>


          <button
            className="secondary-button"
            onClick={handleEditTrip}
          >
            Edit Trip
          </button>


          {newlyGenerated && (

            <button
              className="primary-button"
              onClick={
                handleSaveTrip
              }
            >
              Save Trip
            </button>

          )}

        </div>

      </div>

    </div>
  );
}


export default Itinerary;