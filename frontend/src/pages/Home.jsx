import { Link } from "react-router-dom";
import { useState } from "react";

import heroImage from "../assets/hero.png";
import goaImage from "../assets/goa.png";
import jaipurImage from "../assets/jaipur.png";
import keralaImage from "../assets/kerala.png";
import manaliImage from "../assets/manali.png";

import "./Home.css";

function Home() {

  const [selectedDestination, setSelectedDestination] =
    useState(null);

  // Check whether the user is logged in
  const isLoggedIn =
    localStorage.getItem("isLoggedIn") === "true";


  const recentTrips = [
    {
      name: "Goa",
      image: goaImage,
      dates: "15–18 September",
      budget: "₹15,000 onwards",
    },

    {
      name: "Jaipur",
      image: jaipurImage,
      dates: "10–13 August",
      budget: "₹12,000 onwards",
    },

    {
      name: "Kerala",
      image: keralaImage,
      dates: "2–6 July",
      budget: "₹20,000 onwards",
    },
  ];


  const trendingDestinations = [
    {
      name: "Goa",
      image: goaImage,
      description:
        "Beaches, nightlife, food and unforgettable coastal experiences.",
    },

    {
      name: "Manali",
      image: manaliImage,
      description:
        "Mountains, adventure, scenic valleys and peaceful escapes.",
    },

    {
      name: "Jaipur",
      image: jaipurImage,
      description:
        "Royal palaces, forts, culture and authentic Rajasthani food.",
    },

    {
      name: "Kerala",
      image: keralaImage,
      description:
        "Backwaters, beaches, greenery and relaxing experiences.",
    },
  ];


  return (
    <main className="home">


      {/* ================= HERO ================= */}

      <section className="hero">

        <div className="hero-content">

          <h1>
            Plan Less.
            <br />
            Explore More.
          </h1>

          <p>
            Your smarter way to plan
            unforgettable trips.
          </p>

          {/* Show only when NOT logged in */}

          {!isLoggedIn && (
            <Link
              to="/login"
              className="start-planning-btn"
            >
              Start Planning
            </Link>
          )}

        </div>


        <div className="hero-image">

          <img
            src={heroImage}
            alt="Travel destination"
          />

        </div>

      </section>


      {/* ================= RECENTLY VISITED ================= */}

      <section className="recent-trips">

        <div className="section-header">

          <h2>
            Most Recently Visited
          </h2>

          <p>
            Get inspired by destinations
            travelers are exploring.
          </p>

        </div>


        <div className="recent-trips-grid">

          {recentTrips.map(
            (trip, index) => (

              <div
                className="recent-trip-card"
                key={index}
              >

                <img
                  src={trip.image}
                  alt={trip.name}
                />

                <div className="recent-trip-content">

                  <h3>
                    {trip.name}
                  </h3>

                  <p>
                    {trip.dates}
                  </p>

                  <strong>
                    {trip.budget}
                  </strong>

                </div>

              </div>

            )
          )}

        </div>

      </section>


      {/* ================= TRENDING ================= */}

      <section className="trending-picks">

        <div className="section-header">

          <h2>
            Top Trending Picks
          </h2>

          <p>
            Explore destinations travelers
            are loving right now.
          </p>

        </div>


        <div className="trending-grid">

          {trendingDestinations.map(
            (destination, index) => (

              <button
                key={index}
                className="trending-card"
                onClick={() =>
                  setSelectedDestination(destination)
                }
              >

                <img
                  src={destination.image}
                  alt={destination.name}
                />

                <div className="trending-card-overlay">

                  <h3>
                    {destination.name}
                  </h3>

                  <span>
                    Explore →
                  </span>

                </div>

              </button>

            )
          )}

        </div>

      </section>


      {/* ================= DESTINATION POPUP ================= */}

      {selectedDestination && (

        <div
          className="destination-modal"
          onClick={() =>
            setSelectedDestination(null)
          }
        >

          <div
            className="destination-modal-content"
            onClick={(e) =>
              e.stopPropagation()
            }
          >

            <button
              className="modal-close"
              onClick={() =>
                setSelectedDestination(null)
              }
            >
              ×
            </button>


            <img
              src={selectedDestination.image}
              alt={selectedDestination.name}
            />


            <div className="destination-modal-info">

              <h2>
                {selectedDestination.name}
              </h2>

              <p>
                {selectedDestination.description}
              </p>

              <Link
                to="/create-trip"
                className="explore-itinerary-btn"
              >
                Explore Itinerary
              </Link>

            </div>

          </div>

        </div>

      )}


      {/* ================= WHY TRIPWISE ================= */}

      <section className="why-tripwise">

        <div className="section-header">

          <h2>
            Why TripWise?
          </h2>

          <p>
            Everything you need to plan
            a better trip.
          </p>

        </div>


        <div className="why-grid">

          <div className="why-card">

            <div className="why-icon">
              🗺️
            </div>

            <h3>
              Smart Itineraries
            </h3>

            <p>
              Get personalised day-wise
              travel plans based on your
              interests.
            </p>

          </div>


          <div className="why-card">

            <div className="why-icon">
              ₹
            </div>

            <h3>
              Budget Friendly
            </h3>

            <p>
              Plan your entire trip around
              the budget you choose.
            </p>

          </div>


          <div className="why-card">

            <div className="why-icon">
              ⏱
            </div>

            <h3>
              Save Time
            </h3>

            <p>
              Spend less time researching
              and more time exploring.
            </p>

          </div>


          <div className="why-card">

            <div className="why-icon">
              ✦
            </div>

            <h3>
              Personalised
            </h3>

            <p>
              Build trips around your
              preferences and travel style.
            </p>

          </div>

        </div>

      </section>


      {/* ================= REVIEWS ================= */}

      <section
        className="reviews"
        id="reviews"
      >

        <div className="section-header">

          <h2>
            What Travelers Say
          </h2>

          <p>
            Experiences from the TripWise community.
          </p>

        </div>


        <div className="reviews-grid">

          <div className="review-card">

            <div className="review-stars">
              ★★★★★
            </div>

            <p>
              "TripWise made planning our
              Goa trip so much easier."
            </p>

            <span>
              — Ananya
            </span>

          </div>


          <div className="review-card">

            <div className="review-stars">
              ★★★★★
            </div>

            <p>
              "I loved how the itinerary
              was organised day by day."
            </p>

            <span>
              — Rahul
            </span>

          </div>


          <div className="review-card">

            <div className="review-stars">
              ★★★★★
            </div>

            <p>
              "The budget planning made
              our trip much easier."
            </p>

            <span>
              — Sneha
            </span>

          </div>

        </div>

      </section>


      {/* ================= ABOUT ON HOME ================= */}

      <section
        className="home-about"
        id="about-tripwise"
      >

        <div className="home-about-content">

          <h2>
            About TripWise
          </h2>

          <p>
            TripWise helps travelers plan
            smarter, personalised trips
            without spending hours researching
            destinations, budgets and routes.
          </p>

          <p className="home-about-slogan">
            Plan Less. Explore More.
          </p>

          <Link
            to="/about"
            className="learn-more-btn"
          >
            Learn More
          </Link>

        </div>

      </section>

    </main>
  );
}

export default Home;