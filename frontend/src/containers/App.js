import "./App.css";
import React, { useEffect, useState } from "react";
// import { useDispatch, useSelector } from "react-redux";
import { Switch, BrowserRouter as Router } from "react-router-dom";
import HomeRoute from "../components/routes/homeRoute";
import LoginRoute from "../components/routes/loginRoute";
import Home from "./home";
import Login from "./login";
function App() {
  const [hasLogin, setLogin] = useState(false);
  const [hasWon, setHasWon] = useState(false);
  const [number, setNumber] = useState("");
  const [status, setStatus] = useState({});
  const [winner, setWinner] = useState("");
  return (
    <div className="App">
      <Router>
        <Switch>
          <HomeRoute exact path="/">
            <Home />
          </HomeRoute>
          <LoginRoute exact path="/login">
            <Login />
          </LoginRoute>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
