import React from "react";

import styled from "styled-components";
const Wrapper = styled.div`
  width: 70%;
  height: 65vh;
  margin: 5px 5px 5px 5px; // top right bottom left
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: start;
  justify-content: center;
`;
// overflow-y: scroll;

export default function Register() {
  return <Wrapper>register</Wrapper>;
}
