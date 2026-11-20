import {
  useState,
  useEffect
} from "react";

import {
  useNavigate,
  useSearchParams
} from "react-router-dom";

import "./CreateTrip.css";


const API_URL =
  "http://127.0.0.1:8000";


function CreateTrip() {

  const navigate = useNavigate();

  const [searchParams] =
    useSearchParams();

  const editTripId =
    searchParams.get("edit");

  const isEditMode =
    Boolean(editTripId);


  const [destination, setDestination] =
    useState("");

  const [startDate, setStartDate] =
    useState("");

  const [endDate, setEndDate] =
    useState("");

  const [travelers, setTravelers] =
    useState(1);

  const [budget, setBudget] =
    useState("");

  const [interests, setInterests] =
    useState([]);

  const [
    optimizationMode,
    setOptimizationMode
  ] = useState(
    "best experience"
  );

  const [
    foodBudgetPerPerson,
    setFoodBudgetPerPerson
  ] = useState("");

  const [
    accommodationPerNight,
    setAccommodationPerNight
  ] = useState("");

  const [
    intercityTransportationCost,
    setIntercityTransportationCost
  ] = useState("");

  const [
    miscellaneousBudget,
    setMiscellaneousBudget
  ] = useState("");

  const [
    transportMode,
    setTransportMode
  ] = useState("car");

  const [
    destinations,
    setDestinations
  ] = useState([]);

  const [loading, setLoading] =
    useState(false);

  const [
    loadingTrip,
    setLoadingTrip
  ] = useState(false);

  const [error, setError] =
    useState("");


  const interestOptions = [
    "Beach",
    "Food",
    "Adventure",
    "Nature",
    "Culture",
    "History",
    "Shopping",
    "Nightlife"
  ];


  useEffect(() => {
    fetchDestinations();
  }, []);


  useEffect(() => {

    if (editTripId) {
      fetchTrip(editTripId);
    }

  }, [editTripId]);


  const fetchDestinations =
    async () => {

      try {

        const token =
          localStorage.getItem(
            "access_token"
          );

        if (!token) {
          setError(
            "You are not logged in."
          );
          return;
        }

        const response =
          await fetch(
            `${API_URL}/destinations`,
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
            "Failed to load destinations."
          );
        }

        setDestinations(data);

      } catch (error) {

        console.error(error);

        setError(
          "Unable to load destinations."
        );
      }
    };


  const fetchTrip =
    async (tripId) => {

      try {

        setLoadingTrip(true);
        setError("");

        const token =
          localStorage.getItem(
            "access_token"
          );

        if (!token) {
          setError(
            "You are not logged in."
          );
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
            "Failed to load trip."
          );
        }

        const trip =
          data.find(
            item =>
              item.id ===
              Number(tripId)
          );

        if (!trip) {
          throw new Error(
            "Trip not found."
          );
        }

        setDestination(
          String(trip.destination_id)
        );

        setStartDate(
          trip.start_date
        );

        setEndDate(
          trip.end_date
        );

        setTravelers(
          trip.travelers
        );

        setBudget(
          trip.budget || ""
        );

        setInterests(
          Array.isArray(trip.interests)
            ? trip.interests
            : []
        );

        setOptimizationMode(
          trip.optimization_mode ||
          "best experience"
        );

        setFoodBudgetPerPerson(
          trip.food_budget_per_person || ""
        );

        setAccommodationPerNight(
          trip.accommodation_per_night || ""
        );

        setIntercityTransportationCost(
          trip.intercity_transportation_cost || ""
        );

        setMiscellaneousBudget(
          trip.miscellaneous_budget || ""
        );

        setTransportMode(
          trip.transport_mode || "car"
        );

      } catch (error) {

        console.error(error);

        setError(
          error.message ||
          "Unable to load trip."
        );

      } finally {

        setLoadingTrip(false);

      }
    };


  const handleInterestChange =
    interest => {

      setInterests(previous => {

        if (
          previous.includes(interest)
        ) {
          return previous.filter(
            item => item !== interest
          );
        }

        return [
          ...previous,
          interest
        ];
      });
    };


  const handleSubmit =
    async event => {

      event.preventDefault();

      setError("");

      if (!destination) {
        setError(
          "Please select a destination."
        );
        return;
      }

      if (
        !startDate ||
        !endDate
      ) {
        setError(
          "Please select your travel dates."
        );
        return;
      }

      if (
        new Date(endDate) <
        new Date(startDate)
      ) {
        setError(
          "End date cannot be before start date."
        );
        return;
      }

      if (travelers < 1) {
        setError(
          "Number of travelers must be at least 1."
        );
        return;
      }

      if (
        !budget ||
        Number(budget) <= 0
      ) {
        setError(
          "Please enter a valid budget."
        );
        return;
      }

      if (interests.length === 0) {
        setError(
          "Please select at least one interest."
        );
        return;
      }

      if (
        foodBudgetPerPerson === "" ||
        Number(foodBudgetPerPerson) < 0
      ) {
        setError(
          "Please enter the daily food budget per person."
        );
        return;
      }

      if (
        accommodationPerNight === "" ||
        Number(accommodationPerNight) < 0
      ) {
        setError(
          "Please enter the accommodation cost per night."
        );
        return;
      }

      if (
        intercityTransportationCost === "" ||
        Number(intercityTransportationCost) < 0
      ) {
        setError(
          "Please enter the intercity transportation cost."
        );
        return;
      }

      try {

        setLoading(true);

        const token =
          localStorage.getItem(
            "access_token"
          );

        if (!token) {
          setError(
            "You are not logged in."
          );
          return;
        }

        const tripData = {

          destination_id:
            Number(destination),

          start_date:
            startDate,

          end_date:
            endDate,

          travelers:
            Number(travelers),

          budget:
            Number(budget),

          interests:
            interests,

          optimization_mode:
            optimizationMode,

          food_budget_per_person:
            Number(
              foodBudgetPerPerson
            ),

          accommodation_per_night:
            Number(
              accommodationPerNight
            ),

          intercity_transportation_cost:
            Number(
              intercityTransportationCost
            ),

          miscellaneous_budget:
            Number(
              miscellaneousBudget || 0
            ),

          transport_mode:
            transportMode
        };


        if (isEditMode) {

          const response =
            await fetch(
              `${API_URL}/trips/${editTripId}`,
              {
                method: "PUT",
                headers: {
                  "Content-Type":
                    "application/json",
                  Authorization:
                    `Bearer ${token}`
                },
                body:
                  JSON.stringify(
                    tripData
                  )
              }
            );

          const data =
            await response.json();

          if (!response.ok) {
            throw new Error(
              data.detail ||
              "Failed to update trip."
            );
          }

          const generateResponse =
            await fetch(
              `${API_URL}/trips/${editTripId}/generate`,
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

          const generatedData =
            await generateResponse.json();

          if (!generateResponse.ok) {
            throw new Error(
              generatedData.detail ||
              "Trip updated but itinerary regeneration failed."
            );
          }

          const selectedDestination =
            destinations.find(
              item =>
                item.id ===
                Number(destination)
            );

          const tripForFrontend = {
            id: data.id,

            destination:
              selectedDestination
                ? selectedDestination.name
                : "Unknown Destination",

            destinationId:
              data.destination_id,

            startDate:
              data.start_date,

            endDate:
              data.end_date,

            travelers:
              data.travelers,

            budget:
              data.budget,

            interests:
              data.interests || interests,

            optimization:
              data.optimization_mode ||
              optimizationMode
          };

          localStorage.setItem(
            "currentTrip",
            JSON.stringify(
              tripForFrontend
            )
          );

          navigate(
            `/itinerary/${editTripId}`,
            {
              replace: true,
              state: {
                newlyGenerated: false
              }
            }
          );

          return;
        }


        const response =
          await fetch(
            `${API_URL}/trips`,
            {
              method: "POST",
              headers: {
                "Content-Type":
                  "application/json",
                Authorization:
                  `Bearer ${token}`
              },
              body:
                JSON.stringify(
                  tripData
                )
            }
          );

        const data =
          await response.json();

        if (!response.ok) {
          throw new Error(
            data.detail ||
            "Failed to create trip."
          );
        }

        const selectedDestination =
          destinations.find(
            item =>
              item.id ===
              Number(destination)
          );

        const tripForFrontend = {
          id: data.id,

          destination:
            selectedDestination
              ? selectedDestination.name
              : "Unknown Destination",

          destinationId:
            data.destination_id,

          startDate:
            data.start_date,

          endDate:
            data.end_date,

          travelers:
            data.travelers,

          budget:
            data.budget,

          interests:
            data.interests ||
            interests,

          optimization:
            data.optimization_mode ||
            optimizationMode
        };

        localStorage.setItem(
          "currentTrip",
          JSON.stringify(
            tripForFrontend
          )
        );

        localStorage.setItem(
          "hasTrips",
          "true"
        );

        navigate(
          "/dashboard"
        );

      } catch (error) {

        console.error(error);

        setError(
          error.message ||
          "Failed to save trip."
        );

      } finally {

        setLoading(false);
      }
    };


  if (
    isEditMode &&
    loadingTrip
  ) {

    return (
      <div className="create-trip-page">
        <div className="create-trip-container">
          <h1>
            Edit Your Trip
          </h1>

          <p>
            Loading your trip...
          </p>
        </div>
      </div>
    );
  }


  return (
    <div className="create-trip-page">

      <div className="create-trip-container">

        <h1>
          {isEditMode
            ? "Edit Your Trip"
            : "Create Your Trip"}
        </h1>

        <p>
          {isEditMode
            ? "Update your trip details."
            : "Plan your perfect trip according to your interests and budget."}
        </p>


        {error && (
          <div className="error-message">
            {error}
          </div>
        )}


        <form onSubmit={handleSubmit}>

          <div className="form-group">
            <label>
              Destination
            </label>

            <select
              value={destination}
              onChange={e =>
                setDestination(
                  e.target.value
                )
              }
            >
              <option value="">
                Select destination
              </option>

              {destinations.map(item => (
                <option
                  key={item.id}
                  value={item.id}
                >
                  {item.name}
                </option>
              ))}
            </select>
          </div>


          <div className="form-group">
            <label>
              Start Date
            </label>

            <input
              type="date"
              value={startDate}
              onChange={e =>
                setStartDate(
                  e.target.value
                )
              }
            />
          </div>


          <div className="form-group">
            <label>
              End Date
            </label>

            <input
              type="date"
              value={endDate}
              onChange={e =>
                setEndDate(
                  e.target.value
                )
              }
            />
          </div>


          <div className="form-group">
            <label>
              Travelers
            </label>

            <input
              type="number"
              min="1"
              value={travelers}
              onChange={e =>
                setTravelers(
                  Number(e.target.value)
                )
              }
            />
          </div>


          <div className="form-group">
            <label>
              Total Budget (₹)
            </label>

            <input
              type="number"
              min="1"
              placeholder="Enter total trip budget"
              value={budget}
              onChange={e =>
                setBudget(
                  e.target.value
                )
              }
            />
          </div>


          <div className="form-group">
            <label>
              Food Budget Per Person / Day (₹)
            </label>

            <input
              type="number"
              min="0"
              placeholder="Example: 800"
              value={foodBudgetPerPerson}
              onChange={e =>
                setFoodBudgetPerPerson(
                  e.target.value
                )
              }
            />
          </div>


          <div className="form-group">
            <label>
              Accommodation Per Night (₹)
            </label>

            <input
              type="number"
              min="0"
              placeholder="Example: 2500"
              value={accommodationPerNight}
              onChange={e =>
                setAccommodationPerNight(
                  e.target.value
                )
              }
            />
          </div>


          <div className="form-group">
            <label>
              Intercity Transportation (₹)
            </label>

            <input
              type="number"
              min="0"
              placeholder="Enter round-trip/intercity cost"
              value={
                intercityTransportationCost
              }
              onChange={e =>
                setIntercityTransportationCost(
                  e.target.value
                )
              }
            />
          </div>


          <div className="form-group">
            <label>
              Miscellaneous Budget (₹)
            </label>

            <input
              type="number"
              min="0"
              placeholder="Optional"
              value={
                miscellaneousBudget
              }
              onChange={e =>
                setMiscellaneousBudget(
                  e.target.value
                )
              }
            />
          </div>


          <div className="form-group">
            <label>
              Local Transport
            </label>

            <select
              value={transportMode}
              onChange={e =>
                setTransportMode(
                  e.target.value
                )
              }
            >
              <option value="walk">
                Walking
              </option>

              <option value="bike">
                Bike
              </option>

              <option value="auto">
                Auto
              </option>

              <option value="car">
                Car
              </option>

              <option value="cab">
                Cab
              </option>
            </select>
          </div>


          <div className="form-group">

            <label>
              Your Interests
            </label>

            <div className="interest-options">

              {interestOptions.map(
                interest => (

                  <label
                    key={interest}
                    className="interest-option"
                  >

                    <input
                      type="checkbox"
                      checked={
                        interests.includes(
                          interest
                        )
                      }
                      onChange={() =>
                        handleInterestChange(
                          interest
                        )
                      }
                    />

                    <span>
                      {interest}
                    </span>

                  </label>
                )
              )}

            </div>

          </div>


          <div className="form-group">

            <label>
              Optimization Mode
            </label>

            <select
              value={optimizationMode}
              onChange={e =>
                setOptimizationMode(
                  e.target.value
                )
              }
            >

              <option value="fastest">
                Fastest
              </option>

              <option value="cheapest">
                Cheapest
              </option>

              <option value="best experience">
                Best Experience
              </option>

            </select>

          </div>


          <button
            type="submit"
            className="primary-button"
            disabled={loading}
          >
            {loading
              ? (
                isEditMode
                  ? "Saving Trip..."
                  : "Creating Trip..."
              )
              : (
                isEditMode
                  ? "Save Trip"
                  : "Create Trip"
              )}
          </button>

        </form>

      </div>

    </div>
  );
}


export default CreateTrip;