import { Routes, Route } from "react-router-dom";

import "./App.css";
import Signup from "./pages/Signup";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import CreateTrip from "./pages/CreateTrip";
import Itinerary from "./pages/Itinerary";
import Discover from "./pages/Discover";
import About from "./pages/About";

function App() {
  return (
    <>
      <Navbar />

      <Routes>

        <Route path="/"element={<Home />}/>
        <Route path="/login"element={<Login />}/>
        <Route path="/dashboard"element={<Dashboard />}/>
        <Route path="/create-trip"element={<CreateTrip />}/>
        <Route path="/itinerary/:tripId"element={<Itinerary />}/>
        <Route path="/discover"element={<Discover />}/>
        <Route path="/about"element={<About />}/>
        <Route path="/signup" element={<Signup />} />

      </Routes>

      <Footer />
    </>
  );
}

export default App;