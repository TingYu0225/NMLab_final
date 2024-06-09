import React, { useEffect, useRef, useState } from "react";
import Keyboard from "react-simple-keyboard";
import "react-simple-keyboard/build/css/index.css";
import "./keyboard.css";
import Box from "@mui/material/Box";
import { useNMLab } from "../../containers/hooks/useNMLab";
export default function Kb() {
  const [layoutName, setLayoutName] = useState("default");
  const mainKeyboardRef = useRef(null);
  const numPadKeyboardRef = useRef(null);
  const { keyIn, setKeyIn, input, setInput } = useNMLab();
  useEffect(() => {
    mainKeyboardRef.current.setInput(input);
    numPadKeyboardRef.current.setInput(input);
  }, [input]);
  const onChange = (input) => {
    console.log("Input changed", input);
    setInput(input);
  };
  const onKeyPress = (button) => {
    console.log("Button pressed", button);

    if (button === "{shift}") handleShift();
    if (button === "{enter}") setKeyIn(false);
  };
  const handleShift = () => {
    setLayoutName((prevLayoutName) =>
      prevLayoutName === "default" ? "shift" : "default"
    );
  };

  const keyboardNumPadOptions = {
    layout: {
      default: [
        "{numpad7} {numpad8} {numpad9}",
        "{numpad4} {numpad5} {numpad6}",
        "{numpad1} {numpad2} {numpad3}",
        "{numpad0}",
      ],
    },
  };

  //<input value={input} placeholder={"Tap on the virtual keyboard to start"} onChange={onChangeInput} />
  return (
    <Box
      sx={{
        width: "100%",
        position: "fixed",
        bottom: "0",
      }}
    >
      <div class="kb">
        <Box
          sx={{
            width: "90%",
            margin: "0",
          }}
        >
          <Keyboard
            theme={"hg-theme-default hg-layout-default mainTheme"}
            keyboardRef={(r) => (mainKeyboardRef.current = r)}
            onChange={onChange}
            onKeyPress={onKeyPress}
            layoutName={layoutName}
            layout={{
              default: [
                "q w e r t y u i o p {bksp}",
                "a s d f g h j k l {enter}",
                "{shift} z x c v b n m , . {shift}",
                "{space}",
              ],
              shift: [
                "Q W E R T Y U I O P {bksp}",
                "A S D F G H J K L {enter}",
                "{shift} Z X C V B N M , . {shift}",
                "{space}",
              ],
            }}
            display={{
              "{shift}": "⇧",
              "{enter}": "return",
              "{bksp}": "⌫",
              "{space}": " ",
              "{back}": "⇦",
            }}
            buttonTheme={[
              {
                class: "hg-height",
                buttons:
                  "q w e r t y u i o p {bksp} a s d f g h j k l {enter} {shift} z x c v b n m , . {shift} {space} Q W E R T Y U I O P {bksp} A S D F G H J K L {enter} {shift} Z X C V B N M , . {shift} {space}",
              },
            ]}
          />
        </Box>
        <Box
          sx={{
            width: "20%",
          }}
        >
          <Keyboard
            theme={"hg-theme-default hg-layout-default numTheme"}
            onChange={onChange}
            onKeyPress={onKeyPress}
            keyboardRef={(r) => (numPadKeyboardRef.current = r)}
            baseClass={"simple-keyboard-numpad"}
            {...keyboardNumPadOptions}
            buttonTheme={[
              {
                class: "hg-height",
                buttons:
                  "{numpad7} {numpad8} {numpad9} {numpad4} {numpad5} {numpad6} {numpad1} {numpad2} {numpad3} {numpad0}",
              },
            ]}
          />
        </Box>
      </div>
    </Box>
  );
}
