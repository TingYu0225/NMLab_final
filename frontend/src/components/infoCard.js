import * as React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import CameraAltIcon from "@mui/icons-material/CameraAlt";
import { TextField } from "@mui/material";
import { Box } from "@mui/joy";
import { useNMLab } from "../containers/hooks/useNMLab";
import DoneOutlineIcon from "@mui/icons-material/DoneOutline";
import LoadingButton from "@mui/lab/LoadingButton";
export default function InfoCard(props) {
  const { test, setName, click } = props;
  const { keyIn, setKeyIn, phone_number, name, password, saveFace, takephoto } =
    useNMLab();

  const textFieldRef = React.useRef(null);
  React.useEffect(() => {
    textFieldRef.current.focus();
  }, []);
  console.log("info", saveFace);
  const status = () => {
    switch (saveFace) {
      case "true":
        return (
          <Button variant="contained" endIcon={<DoneOutlineIcon />} disabled={true}>
            <Typography fontSize="20px" component="div">
              Face Recorded
            </Typography>
          </Button>
        );
      case "false":
        return (
          <Button variant="contained" endIcon={<CameraAltIcon />} onClick={takephoto}>
            <Typography fontSize="20px" component="div">
              Record Face
            </Typography>
          </Button>
        );
      case "pending":
        return (
          <LoadingButton loading variant="outlined" endIcon={<CameraAltIcon />}>
            <Typography fontSize="20px" component="div">
              Record Face
            </Typography>
          </LoadingButton>
        );
      default:
        return (
          <Button variant="contained" endIcon={<CameraAltIcon />}>
            <Typography fontSize="20px" component="div">
              Face Recorded
            </Typography>
          </Button>
        );
    }
  }; //autofocus={keyIn ? "true" : "false"}
  return (
    <Card sx={{ maxWidth: 360 }}>
      <Box
        sx={{ height: 70, mt: 5 }}
        display="flex"
        alignItems="center"
        justifyContent="center"
        flexWrap="wrap"
      >
        <Typography variant="h5" component="div">
          Sign up to StartUp
        </Typography>
      </Box>
      <TextField
        id="filled-search"
        variant="filled"
        label="Name"
        type="Name"
        onClick={() => {
          click("name");
        }}
        defaultValue={name}
        value={name}
        inputRef={textFieldRef}
      />

      <Box
        sx={{ m: 3, mb: 0, fontSize: "1rem" }}
        display="flex"
        alignItems="center"
        justifyContent="center"
        flexWrap="wrap"
      >
        {status()}
      </Box>
      {/* <TextField
        id="standard-password-input"
        label="Password"
        type="pass"
        variant="standard"
        onClick={() => click("password")}
        value={password}
      /> 
      <TextField
        id="standard-phone_number-input"
        label="Phone number"
        type="Phone number"
        variant="standard"
        onClick={() => click("phone_number")}
        value={phone_number}
      />*/}
      <CardContent>
        <Box
          sx={{ height: 50, mb: 2, mt: 0 }}
          display="flex"
          alignItems="center"
          justifyContent="center"
          flexWrap="wrap"
        >
          <Button
            variant="outlined"
            disabled={saveFace == "true" ? (name != "" ? false : true) : true}
          >
            <Typography fontSize="20px" component="div">
              Sign up
            </Typography>
          </Button>
        </Box>
        <Typography variant="body2" color="text.secondary">
          By signing up you agree to the <u>Terms & Conditions</u>
        </Typography>
      </CardContent>
    </Card>
  );
}
