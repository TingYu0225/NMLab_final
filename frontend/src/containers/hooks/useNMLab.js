import { useContext, createContext, useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router";
import axios from "axios";
import { apiClient } from "../api";
var XMLHttpRequest = require("xhr2");

var client = new XMLHttpRequest();

const NMLabContext = createContext({
  login: false,
  name: "",
  num: 0,
  keyIn: false,
  input: "",
  reset: false,
  inputStatus: "",
  phone_number: "",
  password: "",
  search: "",
  saveFace: "false",
  countDown: 0,
  takephoto: () => {},
  sendphoto: () => {},
});
const NMLabProvider = (props) => {
  const [login, setLogin] = useState(false);
  const [name, setName] = useState("");
  const [num, setNum] = useState(0);
  const [keyIn, setKeyIn] = useState(false);
  const [input, setInput] = useState("");
  const [inputStatus, setInputStatus] = useState("");
  const [phone_number, setPhoneNumber] = useState("");
  const [password, setPassword] = useState("");
  const [search, setSearch] = useState("");
  const [saveFace, setSaveFace] = useState("false");
  const [countDown, setCountDown] = useState(5);
  const navigate = useNavigate();
  const [reset, setReset] = useState(false);
  let timer = useRef();
  const takephoto = () => {
    setSaveFace("processing");
    navigate("/camera");
  };
  useEffect(() => {
    apiClient.uploadProfilePicture();
  }, [keyIn]);
  const sendphoto = ({ url }) => {
    setSaveFace("pending");
    console.log("hi setSaveFace");
    navigate("/register");
  };
  useEffect(() => {
    client.open("POST", "http://localhost:5500/set_mode", true);
    client.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    if (keyIn) client.send("mode=keyboard");
    else client.send("mode=normal");
  }, [keyIn]);
  useEffect(() => {
    console.log("hi saveFace", saveFace);
    setCountDown(5);
    if (saveFace === "processing" || saveFace === "retry") {
      timer.current = setInterval(() => {
        console.log("hi count", countDown);
        setCountDown((prevCount) => {
          return prevCount - 1;
        });
      }, 1000);
    }
  }, [saveFace]);
  useEffect(() => {
    if (countDown <= 0) clearInterval(timer.current);
  }, [countDown]);

  useEffect(() => {
    if (reset) {
      setReset(false);
      setLogin(false);
      setSaveFace("false");
      setSearch("");
      setInputStatus("");
      setInput("");
      setName("");
      setNum(0);
      setKeyIn(false);
    }
  }, [reset]);

  // init input
  useEffect(() => {
    if (!keyIn) {
      setInput("");
      setInputStatus("");
    }
    if (keyIn) {
      switch (inputStatus) {
        case "name":
          console.log("name:", name);
          if (name.length > 0) setInput(name);
          else setInput("");
          break;
        case "password":
          if (password.length > 0) setInput(password);
          else setInput("");
          break;
        case "phone_number":
          if (phone_number.length > 0) setInput(phone_number);
          else setInput("");
          break;
        case "search":
          if (search.length > 0) setInput(search);
          else setInput("");
          break;
      }
    }
  }, [keyIn, inputStatus]);
  //keyboard input display
  useEffect(() => {
    // This effect will run after every render
    if (keyIn) {
      switch (inputStatus) {
        case "name":
          setName(input);
          break;
        case "password":
          console.log("password:", input);
          setPassword(input);
          break;
        case "phone_number":
          setPhoneNumber(input);
          break;
        case "search":
          setSearch(input);
          break;
      }
    }
  }, [input]);

  return (
    <NMLabContext.Provider
      value={{
        login,
        name,
        num,
        keyIn,
        input,
        inputStatus,
        password,
        phone_number,
        search,
        saveFace,
        countDown,
        sendphoto,
        takephoto,
        setSaveFace,
        setSearch,
        setInputStatus,
        setInput,
        setLogin,
        setName,
        setNum,
        setKeyIn,
        setReset,
      }}
      {...props}
    />
  );
};

const useNMLab = () => useContext(NMLabContext);
export { NMLabProvider, useNMLab };
