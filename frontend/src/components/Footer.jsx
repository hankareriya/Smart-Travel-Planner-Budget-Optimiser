import { Link } from "react-router-dom";
import "./Footer.css"
function Footer() {
  return (
    <footer className="footer">

      <div className="footer-content">

        <div className="footer-brand">

          <h2>
            TripWise
          </h2>

          <p>
            Plan Less. Explore More.
          </p>

        </div>


        <div className="footer-links">

          <a href="#reviews">
            Reviews
          </a>

          <Link to="/discover">
            Destinations
          </Link>

          <Link to="/about">
            About
          </Link>

          <a href="#contact">
            Contact
          </a>

        </div>

      </div>


      <div className="footer-bottom">

        <p>
          © 2026 TripWise. All rights reserved.
        </p>

      </div>

    </footer>
  );
}

export default Footer;