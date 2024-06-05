import axios from "axios";
const instance = axios.create({ baseURL: "http://localhost:4000/api/guess" });
const startGame = async () => {
  const {
    data: { msg },
  } = await instance.post("/start");
  return msg;
};
const guess = async (number) => {
  try {
    const {
      data: { msg1, msg2, msg3, whowin },
    } = await instance.get("/guess", { params: { number } });
    return { msg1, msg2, msg3, whowin };
  } catch (error) {
    return {
      msg1: "Error: " + number + " is not a valid number (1 - 100)",
      msg2: "",
      msg3: "",
      whowin: "",
    };
  }
};
const restart = async () => {
  const {
    data: { msg },
  } = await instance.post("/restart");
  return msg;
};
export { startGame, guess, restart };
