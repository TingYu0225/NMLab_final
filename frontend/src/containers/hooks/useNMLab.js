import { useContext, createContext, useState, useEffect } from "react";
const NMLabContext = createContext({
  login: false,
  name: "",
  num: 0,
  keyIn: false,
  input: "",
  inputStatus: "",
  phone_number: "",
  password: "",
  search: "",
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
        setInputStatus,
        setInput,
        setLogin,
        setName,
        setNum,
        setKeyIn,
      }}
      {...props}
    />
  );
};

const useNMLab = () => useContext(NMLabContext);
export { NMLabProvider, useNMLab };
