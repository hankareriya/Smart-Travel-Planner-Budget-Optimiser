import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

import "./Navbar.css";

import logo from "../assets/logo.png";

function Navbar() {
  const navigate = useNavigate();

  const [isLoggedIn, setIsLoggedIn] = useState(
    localStorage.getItem("isLoggedIn") === "true"
  );

  useEffect(() => {
    const updateLoginState = () => {
      setIsLoggedIn(
        localStorage.getItem("isLoggedIn") === "true"
      );
    };

    window.addEventListener(
      "loginStateChanged",
      updateLoginState
    );

    return () => {
      window.removeEventListener(
        "loginStateChanged",
        updateLoginState
      );
    };
  }, []);

  const handleLogout = () => {
    // Only log out.
    // Do NOT remove saved trips.
    localStorage.removeItem("isLoggedIn");

    window.dispatchEvent(
      new Event("loginStateChanged")
    );

    navigate("/");
  };

  return (
    <nav className="navbar">

      <div className="navbar-container">

        {/* Logo */}

        <Link
          to="/"
          className="navbar-logo"
        >

          <img
            src={logo}
            alt="TripWise logo"
            className="navbar-logo-image"
          />

          <span className="logo-text">
            TripWise
          </span>

        </Link>


        {/* Navigation */}

        <div className="navbar-right">

          <div className="navbar-links">

            <Link to="/">
              Home
            </Link>

            <Link to="/discover">
              Discover
            </Link>

            <Link to="/about">
              About Us
            </Link>

            {isLoggedIn && (
              <Link to="/dashboard">
                My Trips
              </Link>
            )}

          </div>


          {/* Login / Logout */}

          {!isLoggedIn ? (

            <Link
              to="/login"
              className="login-button"
            >
              Login / Sign In
            </Link>

          ) : (

            <button
              onClick={handleLogout}
              className="logout-button"
            >
              Logout
            </button>

          )}

        </div>

      </div>

    </nav>
  );
}

export default Navbar;