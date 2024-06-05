import React from "react";

import { Route, Redirect } from "react-router-dom";
// slices

export default function LoginRoute({ children, path }) {
  //const { isLogin } = useSelector(selectSession);
  return (
    <Route
      path={path}
      render={() => {
        // return isLogin ? <Redirect to="/" /> : children;
        return children;
      }}
    />
  );
}
