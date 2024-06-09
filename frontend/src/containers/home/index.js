import React from "react";
import NestedCard from "../../components/card";
import styled from "styled-components";
import Box from "@mui/material/Box";
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

const title = ["註冊帳號", "儲值/繳費", "好康/紅利", "訂票/取票/訂房", "寄件/購物", "列印/掃描"];
const description = [
  "把你的臉拍下來",
  "遊戲點數, 停車費, ETC, 罰單, 信用卡, 保險",
  "OPEN POINT, 小7集點卡, 銀行, 證券保險, 高鐵",
  "電影票, 火車票, 飯店, 機票, 租車",
  "門市預購, 交貨便, 把你啊罵吃掉, 網購, 國際快遞",
  "雲端列印, 文件/圖片/海報列印, 4x6相片列印,",
];
export default function Home(props) {
  const { login, setLogin } = props;
  const selectCard = (title) => {
    if (title === "註冊帳號") window.location.href = "/register";
    else if (title === "列印/掃描") window.location.href = "/login";
  };
  return (
    <Wrapper>
      {title.map((t, i) => (
        <Box width="50%" height="30%">
          <NestedCard title={t} description={description[i]} selectCard={selectCard} />
        </Box>
      ))}
    </Wrapper>
  );
}
