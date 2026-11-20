import { Link } from "react-router-dom";
import { useEffect, useState } from "react";

import api from "../services/api";

import goaImage from "../assets/goa.png";
import jaipurImage from "../assets/jaipur.png";
import mumbaiImage from "../assets/mumbai.png";

import "./Discover.css";

function Discover() {
  const [destinations, setDestinations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/destinations")
      .then((response) => {
        console.log("Destinations from backend:", response.data);

        setDestinations(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching destinations:", error);

        setError("Unable to load destinations.");
        setLoading(false);
      });
  }, []);

  const destinationImages = {
    Goa: goaImage,
    Jaipur: jaipurImage,
    Mumbai: mumbaiImage,
  };

  const destinationDescriptions = {
    Goa: "Beaches, nightlife and coastal adventures.",
    Jaipur: "Forts, palaces and vibrant culture.",
    Mumbai: "Iconic landmarks, beaches and city experiences.",
  };

  return (
    <main className="discover-page">

      <section className="discover-header">
        <h1>Discover Your Next Adventure</h1>

        <p>
          Explore destinations and find inspiration for your next trip.
        </p>
      </section>

      {loading && (
        <p className="status-message">
          Loading destinations...
        </p>
      )}

      {error && (
        <p className="status-message error">
          {error}
        </p>
      )}

      {!loading && !error && destinations.length === 0 && (
        <p className="status-message">
          No destinations found.
        </p>
      )}

      {!loading && !error && destinations.length > 0 && (
        <section className="discover-grid">

          {destinations.map((destination) => (
            <div
              className="discover-card"
              key={destination.id}
            >

              <img
                src={
                  destinationImages[destination.name] ||
                  goaImage
                }
                alt={destination.name}
              />

              <div className="discover-card-content">

                <h2>
                  {destination.name}
                </h2>

                <p>
                  {destinationDescriptions[destination.name] ||
                    "Discover amazing places and create unforgettable memories."}
                </p>

                <Link
                  to="/create-trip"
                  className="explore-itinerary-btn"
                >
                  Explore Itinerary
                </Link>

              </div>

            </div>
          ))}

        </section>
      )}

    </main>
  );
}

export default Discover;