import "./App.css";
import React, { useEffect, useState } from "react";
// import { useDispatch, useSelector } from "react-redux";
import { Switch, BrowserRouter as Router } from "react-router-dom";
import { Route } from "react-router-dom";
import HomeRoute from "../components/routes/homeRoute";
import LoginRoute from "../components/routes/loginRoute";
import ProtectedRoute from "../components/routes/protectedRoute";
import RegisterRoute from "../components/routes/registerRoute";

import Home from "./home";
import Login from "./login";
import SearchBar from "./searchBar";
import Register from "./register";
import { useNMLab } from "./hooks/useNMLab";
function App() {
  const { status, login, keyIn, setKeyIn, setStatus, setLogin } = useNMLab();
  return (
    <div className="App">
      <SearchBar keyIn={keyIn} setKeyIn={setKeyIn} />
      <Router>
        <Switch>
          <HomeRoute exact path="/">
            <Home login={login} setLogin={setLogin} />
          </HomeRoute>
          <LoginRoute exact path="/login">
            <Login />
          </LoginRoute>
          <RegisterRoute exact path="/register">
            <Register />
          </RegisterRoute>
          {/* <ProtectedRoute login={login}>
            <Login />
          </ProtectedRoute> */}
        </Switch>
      </Router>
    </div>
  );
}

export default App;
