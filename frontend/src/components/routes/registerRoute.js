import React from "react";
import { Route } from "react-router-dom";

export default function HomeRoute({ children, path }) {
  return (
    <Route
      exact
      path={path}
      render={() => {
        return children;
      }}
    />
  );
}