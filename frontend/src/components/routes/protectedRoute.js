import React from "react";
import { useNMLab } from "../../containers/hooks/useNMLab";
import { Route, Redirect } from "react-router-dom";
export default function ProtectedRoute({ children, path }) {
  const { login } = useNMLab();
  return (
    <Route
      path={path}
      render={() => {
        return login ? <Redirect to="/" /> : children;
      }}
    />
  );
}
