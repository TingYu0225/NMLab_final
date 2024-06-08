import React, { useEffect } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import styled from "styled-components";

import { useNMLab, NMLabProvider } from "./hooks/useNMLab";
import Kb from "../components/keyboard/keyboard";

const Wrapper = styled.div`
  height: 89vh;
  margin: 0; // top right bottom left
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  position: fixed;
  z-index: 1;
  top: 40px;
  left: 20px;
`;
// overflow-y: scroll;
// background-color: #becbd3;
export default function DisplayKB() {
  const { name, setName } = useNMLab();
  const [password, setPassword] = React.useState("");
  const [phone_number, setPhoneNumber] = React.useState("");
  const test = () => {
    console.log(name);
  };
  console.log("pass", setName);
  return (
    <Wrapper>
      <Kb />
    </Wrapper>
  );
}
