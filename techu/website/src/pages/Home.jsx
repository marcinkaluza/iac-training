import React from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home">
      <div className="hero">
        <h3>Welcome to</h3>
        <h1>Lanscape Photo of the Year</h1>
        <button className="btn" onClick={() => navigate("/galery")}>
          Enter the galery
        </button>
      </div>
    </div>
  );
}

export default Home;
