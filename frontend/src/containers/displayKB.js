import React, { useEffect } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import styled from "styled-components";

import Switch from "@mui/material/Switch";
import Paper from "@mui/material/Paper";
import Slide from "@mui/material/Slide";
import FormControlLabel from "@mui/material/FormControlLabel";

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
// <Paper sx={{ m: 1 }} elevation={4}>
export default function DisplayKB() {
  const [checked, setChecked] = React.useState(false);
  const { keyIn } = useNMLab();

  return (
    <Box
      sx={{
        zIndex: 10,
        width: "100%",
        justifyContent: "center",
        display: "flex",
      }}
    >
      <Box
        sx={{
          zIndex: 10,
          width: "100%",
          justifyContent: "center",
          display: "flex",
        }}
      >
        <Kb />
      </Box>
    </Box>
  );
}
