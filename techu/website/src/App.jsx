import { useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.css";
import Home from "./pages/Home";
import Galery from "./pages/Galery";
import { Amplify } from "aws-amplify";
import "@aws-amplify/ui-react/styles.css";
import { withAuthenticator } from "@aws-amplify/ui-react";
import amplifyConfig from "./authconfig";
import React from "react";
Amplify.configure(amplifyConfig);

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/galery" element={<Galery />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
