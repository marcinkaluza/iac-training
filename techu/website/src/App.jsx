import { useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.css";
import Home from "./pages/Home";
import Galery from "./pages/Galery";

function App() {
  return (
    <>
      <div className="container">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/galery" element={<Galery />} />
          </Routes>
        </BrowserRouter>
      </div>
    </>
  );
}

export default App;
