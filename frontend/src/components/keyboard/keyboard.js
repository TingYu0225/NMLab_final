import React, { useRef, useState } from "react";
import Keyboard from "react-simple-keyboard";
import "react-simple-keyboard/build/css/index.css";
import "./keyboard.css";

export default function Kb() {
  const [layoutName, setLayoutName] = useState("default");
  const [input, setInput] = useState("");
  const mainKeyboardRef = useRef(null);
  const numPadKeyboardRef = useRef(null);
  const onChange = (input) => {
    setInput(input);
    if (mainKeyboardRef.current) mainKeyboardRef.current.setInput(input);
    if (numPadKeyboardRef.current) numPadKeyboardRef.current.setInput(input);
  };
  const onKeyPress = (button) => {
    console.log("Button pressed", button);

    if (button === "{shift}") handleShift();
  };
  const handleShift = () => {
    setLayoutName((prevLayoutName) => (prevLayoutName === "default" ? "shift" : "default"));
  };

  const onChangeInput = (event) => {
    const input = event.target.value;
    setInput(input);
    if (mainKeyboardRef.current) mainKeyboardRef.current.setInput(input);
    if (numPadKeyboardRef.current) numPadKeyboardRef.current.setInput(input);
  };
  const keyboardNumPadOptions = {
    layout: {
      default: ["{numpad7} {numpad8} {numpad9}", "{numpad4} {numpad5} {numpad6}", "{numpad1} {numpad2} {numpad3}", "{numpad0}"],
    },
  };
  return (
    <div class="kb">
      <input value={input} placeholder={"Tap on the virtual keyboard to start"} onChange={onChangeInput} />
      <div>
        <Keyboard
          theme={"hg-theme-default hg-layout-default myTheme"}
          keyboardRef={(r) => (mainKeyboardRef.current = r)}
          onChange={onChange}
          onKeyPress={onKeyPress}
          layoutName={layoutName}
          layout={{
            default: ["q w e r t y u i o p {bksp}", "a s d f g h j k l {enter}", "{shift} z x c v b n m , . {shift}", "{space}"],
            shift: ["Q W E R T Y U I O P {bksp}", "A S D F G H J K L {enter}", "{shift} Z X C V B N M , . {shift}", "{space}"],
          }}
          display={{
            "{shift}": "⇧",
            "{enter}": "return",
            "{bksp}": "⌫",
            "{space}": " ",
            "{back}": "⇦",
          }}
        />
      </div>
      <div className="numPad">
        <Keyboard theme={"hg-theme-default hg-layout-default myTheme"} onChange={onChange} onKeyPress={onKeyPress} keyboardRef={(r) => (numPadKeyboardRef.current = r)} baseClass={"simple-keyboard-numpad"} {...keyboardNumPadOptions} />
      </div>
    </div>
  );
}
