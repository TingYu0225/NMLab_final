import { useContext, createContext, useState, useEffect } from "react";
const NMLabContext = createContext({
  login: false,
  name: "",
  num: 0,
  keyIn: false,
});
const NMLabProvider = (props) => {
  const [login, setLogin] = useState(false);
  const [name, setName] = useState("");
  const [num, setNum] = useState(0);
  const [keyIn, setKeyIn] = useState(false);

  useEffect(() => {}, []);

  return (
    <NMLabContext.Provider
      value={{
        login,
        name,
        num,
        keyIn,
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
