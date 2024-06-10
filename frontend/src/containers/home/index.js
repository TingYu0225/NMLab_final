import React from "react";
import NestedCard from "../../components/card";
import styled from "styled-components";
import Box from "@mui/material/Box";
import { useNMLab } from "../hooks/useNMLab";
import { useNavigate } from "react-router";
import AdCard from "../../components/adCard";
const Wrapper = styled.div`
  width: 70%;
  height: 100%;
  margin: 5px 5px 5px 5px; // top right bottom left
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: start;
  justify-content: center;
`;
// overflow-y: scroll;

const title = [
  "註冊帳號",
  "儲值/繳費",
  "好康/紅利",
  "訂票/取票/訂房",
  "寄件/購物",
  "列印/掃描",
];
const description = [
  "註冊以通行所有服務",
  "遊戲點數、停車費",
  "K-POINT、銀行",
  "電影票、火車票",
  "門市預購、交貨便",
  "雲端列印、文件列印",
];

const description2 = [
  "你的臉就是密碼",
  "ETC、罰單、信用卡",
  "證券保險、高鐵",
  "飯店、機票、租車",
  "把你啊罵賣掉、網購、快遞",
  "圖片列印、4x6相片列印",
];

const ad = ["Javascript從入門到入土"];
export default function Home(props) {
  const { login, setLogin } = useNMLab();
  const navigate = useNavigate();
  const selectCard = (title) => {
    if (title === "註冊帳號") navigate("/register");
    else if (title === "列印/掃描") navigate("/login");
  };
  return (
    <Box display="flex">
      <Wrapper>
        {title.map((t, i) => (
          <Box width="50%" height="30%">
            <NestedCard title={t} description={description[i]} selectCard={selectCard} />
          </Box>
        ))}
      </Wrapper>
      <Box width="30%" sx={{ m: "5px", mt: "25px" }}>
        <AdCard />
      </Box>
    </Box>
  );
}
